"""
Core Voice Analysis Functions
Main module for analyzing voice samples - designed to be called from ChatterboxTTS GUI or standalone.
"""

import numpy as np
from pathlib import Path
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
import warnings
warnings.filterwarnings('ignore')

try:
    import librosa
    import soundfile as sf
    import parselmouth
    from scipy import stats
    DEPENDENCIES_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Missing dependencies for voice analysis: {e}")
    DEPENDENCIES_AVAILABLE = False

@dataclass
class VoiceAnalysisResult:
    """Container for voice analysis results"""
    # File info
    filename: str
    duration: float
    sample_rate: int
    channels: int
    
    # Audio health scores (0-100)
    audio_quality_score: float
    noise_score: float
    dynamic_range_score: float
    clipping_score: float
    
    # Voice quality scores (0-100)  
    pitch_stability_score: float
    voice_quality_score: float
    speaking_rate_score: float
    consistency_score: float
    sibilance_score: float
    
    # Overall TTS suitability (0-100)
    overall_score: float
    suitability_rating: str  # "Excellent", "Good", "Fair", "Poor"
    
    # Detailed metrics
    metrics: Dict
    recommendations: List[str]
    
    # Analysis success
    success: bool
    error_message: Optional[str] = None

def analyze_voice_sample(file_path: str, detailed: bool = True) -> VoiceAnalysisResult:
    """
    Analyze a voice sample for TTS suitability.
    
    Args:
        file_path: Path to audio file
        detailed: Whether to perform detailed Praat analysis
        
    Returns:
        VoiceAnalysisResult with scores and recommendations
    """
    if not DEPENDENCIES_AVAILABLE:
        return VoiceAnalysisResult(
            filename=Path(file_path).name,
            duration=0, sample_rate=0, channels=0,
            audio_quality_score=0, noise_score=0, dynamic_range_score=0, clipping_score=0,
            pitch_stability_score=0, voice_quality_score=0, speaking_rate_score=0, consistency_score=0,
            overall_score=0, suitability_rating="Error",
            metrics={}, recommendations=["Install required dependencies"],
            success=False, error_message="Missing required libraries"
        )
    
    try:
        # Load audio file
        audio_data, sr = librosa.load(file_path, sr=None)
        file_info = sf.info(file_path)
        
        # Basic file analysis
        filename = Path(file_path).name
        duration = len(audio_data) / sr
        
        print(f"Analyzing: {filename}")
        print(f"Duration: {duration:.2f}s, Sample Rate: {sr}Hz")
        
        # Initialize metrics dictionary
        metrics = {}
        recommendations = []
        
        # Audio Health Analysis
        audio_scores = _analyze_audio_health(audio_data, sr, metrics, recommendations)
        
        # Voice Quality Analysis (Praat-based)
        voice_scores = _analyze_voice_quality(file_path, metrics, recommendations) if detailed else _basic_voice_analysis(audio_data, sr, metrics)
        
        # Calculate overall score
        overall_score = _calculate_overall_score(audio_scores, voice_scores)
        suitability_rating = _get_suitability_rating(overall_score)
        
        # Add general recommendations based on scores
        _add_general_recommendations(audio_scores, voice_scores, recommendations)
        
        return VoiceAnalysisResult(
            filename=filename,
            duration=duration,
            sample_rate=sr,
            channels=file_info.channels,
            audio_quality_score=audio_scores['audio_quality'],
            noise_score=audio_scores['noise'],
            dynamic_range_score=audio_scores['dynamic_range'],
            clipping_score=audio_scores['clipping'],
            pitch_stability_score=voice_scores['pitch_stability'],
            voice_quality_score=voice_scores['voice_quality'],
            speaking_rate_score=voice_scores['speaking_rate'],
            consistency_score=voice_scores['consistency'],
            sibilance_score=voice_scores['sibilance'],
            overall_score=overall_score,
            suitability_rating=suitability_rating,
            metrics=metrics,
            recommendations=recommendations,
            success=True
        )
        
    except Exception as e:
        return VoiceAnalysisResult(
            filename=Path(file_path).name if file_path else "Unknown",
            duration=0, sample_rate=0, channels=0,
            audio_quality_score=0, noise_score=0, dynamic_range_score=0, clipping_score=0,
            pitch_stability_score=0, voice_quality_score=0, speaking_rate_score=0, consistency_score=0,
            sibilance_score=0,
            overall_score=0, suitability_rating="Error",
            metrics={}, recommendations=[f"Analysis failed: {str(e)}"],
            success=False, error_message=str(e)
        )

def _analyze_audio_health(audio_data: np.ndarray, sr: int, metrics: Dict, recommendations: List[str]) -> Dict[str, float]:
    """Analyze basic audio health metrics"""
    scores = {}
    
    # Clipping detection
    clipping_ratio = np.sum(np.abs(audio_data) > 0.99) / len(audio_data)
    metrics['clipping_ratio'] = clipping_ratio
    scores['clipping'] = max(0, 100 - (clipping_ratio * 10000))  # Penalize heavily
    
    if clipping_ratio > 0.001:
        recommendations.append(f"Audio has {clipping_ratio*100:.2f}% clipping - reduce input gain")
    
    # Dynamic range
    rms = np.sqrt(np.mean(audio_data**2))
    peak = np.max(np.abs(audio_data))
    dynamic_range_db = 20 * np.log10(peak / (rms + 1e-10))
    metrics['dynamic_range_db'] = dynamic_range_db
    metrics['rms_level'] = rms
    metrics['peak_level'] = peak
    
    # Score dynamic range (good range is 10-25 dB)
    if 10 <= dynamic_range_db <= 25:
        scores['dynamic_range'] = 100
    elif dynamic_range_db < 10:
        scores['dynamic_range'] = max(0, dynamic_range_db * 10)
        recommendations.append("Audio is too compressed - increase dynamic range")
    else:
        scores['dynamic_range'] = max(0, 100 - (dynamic_range_db - 25) * 2)
        recommendations.append("Audio has excessive dynamic range - may need light compression")
    
    # Noise analysis (using quieter segments)
    frame_length = int(0.025 * sr)  # 25ms frames
    hop_length = int(0.01 * sr)     # 10ms hop
    
    # Calculate RMS for each frame
    frames = librosa.util.frame(audio_data, frame_length=frame_length, hop_length=hop_length)
    frame_rms = np.sqrt(np.mean(frames**2, axis=0))
    
    # Assume bottom 20% of frames represent noise floor
    noise_floor = np.percentile(frame_rms, 20)
    signal_level = np.percentile(frame_rms, 80)
    
    snr_db = 20 * np.log10((signal_level + 1e-10) / (noise_floor + 1e-10))
    metrics['snr_db'] = snr_db
    metrics['noise_floor'] = noise_floor
    
    # Score SNR (good SNR is > 40dB)
    if snr_db >= 40:
        scores['noise'] = 100
    elif snr_db >= 20:
        scores['noise'] = 50 + (snr_db - 20) * 2.5
    else:
        scores['noise'] = max(0, snr_db * 2.5)
        recommendations.append(f"Low SNR ({snr_db:.1f}dB) - record in quieter environment")
    
    # Overall audio quality (frequency response, spectral characteristics)
    spectral_centroid = librosa.feature.spectral_centroid(y=audio_data, sr=sr)[0]
    spectral_rolloff = librosa.feature.spectral_rolloff(y=audio_data, sr=sr)[0]
    
    avg_centroid = np.mean(spectral_centroid)
    avg_rolloff = np.mean(spectral_rolloff)
    
    metrics['spectral_centroid_hz'] = avg_centroid
    metrics['spectral_rolloff_hz'] = avg_rolloff
    
    # Score based on spectral characteristics (voice typically 1-4kHz centroid)
    if 1000 <= avg_centroid <= 4000:
        scores['audio_quality'] = 100
    else:
        deviation = min(abs(avg_centroid - 1000), abs(avg_centroid - 4000))
        scores['audio_quality'] = max(20, 100 - deviation / 50)
        
        if avg_centroid < 1000:
            recommendations.append("Audio sounds muffled - check for low-pass filtering")
        else:
            recommendations.append("Audio sounds harsh/bright - check for excessive high frequencies")
    
    return scores

def _analyze_voice_quality(file_path: str, metrics: Dict, recommendations: List[str]) -> Dict[str, float]:
    """Analyze voice quality using Praat (parselmouth)"""
    scores = {}
    
    try:
        # Load with Praat
        sound = parselmouth.Sound(file_path)
        
        # Pitch analysis
        pitch = sound.to_pitch(time_step=0.01, pitch_floor=75, pitch_ceiling=600)
        pitch_values = pitch.selected_array['frequency']
        pitch_values = pitch_values[pitch_values != 0]  # Remove unvoiced frames
        
        if len(pitch_values) > 0:
            f0_mean = np.mean(pitch_values)
            f0_std = np.std(pitch_values)
            f0_cv = f0_std / f0_mean if f0_mean > 0 else 1
            
            metrics['f0_mean_hz'] = f0_mean
            metrics['f0_std_hz'] = f0_std
            metrics['f0_coefficient_variation'] = f0_cv
            
            # Score pitch stability (CV < 0.1 is very stable)
            if f0_cv <= 0.1:
                scores['pitch_stability'] = 100
            elif f0_cv <= 0.2:
                scores['pitch_stability'] = 100 - (f0_cv - 0.1) * 500
            else:
                scores['pitch_stability'] = max(0, 50 - (f0_cv - 0.2) * 250)
                recommendations.append("Pitch varies significantly - practice consistent speaking")
                
        else:
            scores['pitch_stability'] = 0
            recommendations.append("Could not detect pitch - check if audio contains speech")
        
        # Voice quality measures
        try:
            # Harmonics-to-noise ratio
            harmonicity = sound.to_harmonicity(time_step=0.01, minimum_pitch=75)
            hnr_values = harmonicity.values[harmonicity.values != -200]  # Remove undefined
            
            if len(hnr_values) > 0:
                hnr_mean = np.mean(hnr_values)
                metrics['hnr_db'] = hnr_mean
                
                # Score HNR (> 15dB is good)
                if hnr_mean >= 15:
                    scores['voice_quality'] = 100
                elif hnr_mean >= 10:
                    scores['voice_quality'] = 50 + (hnr_mean - 10) * 10
                else:
                    scores['voice_quality'] = max(0, hnr_mean * 5)
                    recommendations.append(f"Low voice quality (HNR: {hnr_mean:.1f}dB) - may be breathy/hoarse")
            else:
                scores['voice_quality'] = 50
                
        except:
            scores['voice_quality'] = 50
        
        # Speaking rate analysis
        intensity = sound.to_intensity(time_step=0.01)
        intensity_values = intensity.values[0]
        
        # Simple speaking rate estimation based on intensity peaks
        from scipy.signal import find_peaks
        peaks, _ = find_peaks(intensity_values, height=np.percentile(intensity_values, 60))
        speaking_rate = len(peaks) / sound.duration
        
        metrics['speaking_rate_hz'] = speaking_rate
        
        # Score speaking rate (2-6 Hz is normal)
        if 2 <= speaking_rate <= 6:
            scores['speaking_rate'] = 100
        else:
            deviation = min(abs(speaking_rate - 2), abs(speaking_rate - 6))
            scores['speaking_rate'] = max(20, 100 - deviation * 20)
            
            if speaking_rate < 2:
                recommendations.append("Speaking rate is very slow - consider speaking slightly faster")
            else:
                recommendations.append("Speaking rate is very fast - consider speaking slightly slower")
        
        # Consistency (intensity variation)
        intensity_std = np.std(intensity_values)
        metrics['intensity_std_db'] = intensity_std
        
        # Score consistency (lower std is more consistent)
        if intensity_std <= 5:
            scores['consistency'] = 100
        elif intensity_std <= 10:
            scores['consistency'] = 100 - (intensity_std - 5) * 10
        else:
            scores['consistency'] = max(0, 50 - (intensity_std - 10) * 5)
            recommendations.append("Volume varies significantly - practice consistent speaking volume")
        
        # Sibilance analysis
        sibilance_score, sibilance_level = _analyze_sibilance(sound, metrics)
        scores['sibilance'] = sibilance_score
        
        if sibilance_score < 70:
            recommendations.append(f"High sibilance detected ({sibilance_level:.1f}dB) - consider de-essing")
            
    except Exception as e:
        print(f"Praat analysis failed: {e}")
        # Fallback to basic analysis
        return _basic_voice_analysis_fallback(metrics)
    
    return scores

def _basic_voice_analysis(audio_data: np.ndarray, sr: int, metrics: Dict) -> Dict[str, float]:
    """Basic voice analysis without Praat"""
    scores = {}
    
    # Simple pitch estimation using librosa
    f0 = librosa.yin(audio_data, fmin=80, fmax=400, sr=sr)
    f0_clean = f0[f0 > 0]
    
    if len(f0_clean) > 0:
        f0_mean = np.mean(f0_clean)
        f0_std = np.std(f0_clean)
        metrics['f0_mean_hz'] = f0_mean
        metrics['f0_std_hz'] = f0_std
        scores['pitch_stability'] = max(0, 100 - f0_std * 2)
    else:
        scores['pitch_stability'] = 50
    
    # Zero crossing rate (voice quality indicator)
    zcr = librosa.feature.zero_crossing_rate(audio_data)[0]
    avg_zcr = np.mean(zcr)
    metrics['zero_crossing_rate'] = avg_zcr
    
    # Score based on typical voice ZCR
    if 0.02 <= avg_zcr <= 0.15:
        scores['voice_quality'] = 100
    else:
        scores['voice_quality'] = max(0, 100 - abs(avg_zcr - 0.08) * 1000)
    
    # Tempo/rhythm analysis
    tempo, _ = librosa.beat.beat_track(y=audio_data, sr=sr)
    metrics['estimated_tempo'] = tempo
    scores['speaking_rate'] = 80  # Default score for basic analysis
    
    # RMS consistency
    rms = librosa.feature.rms(y=audio_data)[0]
    rms_cv = np.std(rms) / np.mean(rms) if np.mean(rms) > 0 else 1
    metrics['rms_coefficient_variation'] = rms_cv
    scores['consistency'] = max(0, 100 - rms_cv * 200)
    
    # Add basic sibilance analysis for fallback
    scores['sibilance'] = 75  # Default score when no detailed analysis
    
    return scores

def _analyze_sibilance(sound, metrics: Dict) -> Tuple[float, float]:
    """Analyze sibilance content using Praat"""
    try:
        # Get the audio data
        audio_array = sound.values.T.flatten()
        sample_rate = int(sound.sampling_frequency)
        
        # Focus on sibilance frequency range (4-10kHz)
        # Create bandpass filter for sibilance detection
        from scipy import signal
        nyquist = sample_rate / 2
        low_freq = 4000 / nyquist
        high_freq = min(10000 / nyquist, 0.95)
        
        # Bandpass filter to isolate sibilance frequencies
        b, a = signal.butter(4, [low_freq, high_freq], btype='band')
        sibilance_signal = signal.filtfilt(b, a, audio_array)
        
        # Calculate RMS level of sibilance content
        sibilance_rms = np.sqrt(np.mean(sibilance_signal**2))
        sibilance_db = 20 * np.log10(sibilance_rms + 1e-10)
        
        # Store in metrics
        metrics['sibilance_level_db'] = sibilance_db
        metrics['sibilance_rms'] = sibilance_rms
        
        # Score sibilance (lower sibilance levels get higher scores)
        # Typical range: -60dB to -20dB for sibilance content
        if sibilance_db <= -40:
            score = 100  # Very low sibilance
        elif sibilance_db <= -30:
            score = 100 - (sibilance_db + 40) * 5  # Gradual decrease
        elif sibilance_db <= -20:
            score = 50 - (sibilance_db + 30) * 3   # Steeper decrease
        else:
            score = max(0, 20 - (sibilance_db + 20))  # Very harsh sibilance
        
        return score, sibilance_db
        
    except Exception as e:
        print(f"Sibilance analysis failed: {e}")
        return 75.0, -35.0  # Default values

def _basic_voice_analysis_fallback(metrics: Dict) -> Dict[str, float]:
    """Fallback scores when Praat analysis fails"""
    return {
        'pitch_stability': 50,
        'voice_quality': 50, 
        'speaking_rate': 50,
        'consistency': 50,
        'sibilance': 75
    }

def _calculate_overall_score(audio_scores: Dict[str, float], voice_scores: Dict[str, float]) -> float:
    """Calculate weighted overall score"""
    # Weights for different aspects
    weights = {
        'audio_quality': 0.14,
        'noise': 0.14,
        'dynamic_range': 0.09,
        'clipping': 0.09,
        'pitch_stability': 0.18,
        'voice_quality': 0.14,
        'speaking_rate': 0.09,
        'consistency': 0.05,
        'sibilance': 0.08  # New sibilance weight
    }
    
    all_scores = {**audio_scores, **voice_scores}
    weighted_sum = sum(score * weights.get(metric, 0) for metric, score in all_scores.items())
    
    return min(100, max(0, weighted_sum))

def _get_suitability_rating(score: float) -> str:
    """Convert numerical score to rating"""
    if score >= 85:
        return "Excellent"
    elif score >= 70:
        return "Good"  
    elif score >= 55:
        return "Fair"
    else:
        return "Poor"

def _add_general_recommendations(audio_scores: Dict, voice_scores: Dict, recommendations: List[str]):
    """Add general recommendations based on scores"""
    overall_audio = np.mean(list(audio_scores.values()))
    overall_voice = np.mean(list(voice_scores.values()))
    
    if overall_audio < 60:
        recommendations.append("Consider improving recording setup - use better microphone/room treatment")
    
    if overall_voice < 60:
        recommendations.append("Practice consistent speaking pace and tone for better TTS results")
    
    if len(recommendations) == 0:
        recommendations.append("Voice sample shows good quality for TTS use!")

# Utility function for batch analysis
def analyze_multiple_samples(file_paths: List[str], detailed: bool = True) -> List[VoiceAnalysisResult]:
    """Analyze multiple voice samples"""
    results = []
    for file_path in file_paths:
        print(f"\nAnalyzing: {Path(file_path).name}")
        result = analyze_voice_sample(file_path, detailed)
        results.append(result)
    return results