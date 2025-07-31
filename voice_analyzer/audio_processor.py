"""
Audio Processing Functions for Voice Sample Auto-Fix
Implements actual audio processing fixes for TTS optimization.
"""

import numpy as np
import librosa
import soundfile as sf
from pathlib import Path
from typing import List, Dict, Any, Optional
import warnings
warnings.filterwarnings('ignore')

try:
    from scipy import signal
    from scipy.ndimage import median_filter
    SCIPY_AVAILABLE = True
except ImportError:
    SCIPY_AVAILABLE = False

class AudioProcessor:
    """Audio processing engine for voice sample fixes"""
    
    def __init__(self, preserve_characteristics: bool = True, quality_level: int = 8):
        self.preserve_characteristics = preserve_characteristics
        self.quality_level = quality_level
        self.target_sample_rate = 24000  # Optimal for TTS
        
    def process_audio(self, input_path: str, output_path: str, 
                     selected_fixes: List[str], progress_callback=None) -> Dict[str, Any]:
        """
        Apply selected audio fixes to the input file
        
        Args:
            input_path: Path to input audio file
            output_path: Path for output file
            selected_fixes: List of fix names to apply
            progress_callback: Optional callback for progress updates
            
        Returns:
            Dictionary with processing results and statistics
        """
        try:
            if progress_callback:
                progress_callback("Loading audio file...")
            
            # Load audio
            audio_data, sample_rate = librosa.load(input_path, sr=None)
            original_length = len(audio_data)
            original_sr = sample_rate
            
            results = {
                'success': True,
                'original_duration': len(audio_data) / sample_rate,
                'original_sample_rate': sample_rate,
                'fixes_applied': [],
                'statistics': {}
            }
            
            # Apply fixes in optimal order
            fix_order = [
                'remove_dc_offset',
                'trim_silence', 
                'fix_clipping',
                'reduce_noise',
                'normalize_volume',
                'optimize_dynamic_range',
                'enhance_clarity',
                'slow_speaking_rate',
                'apply_tts_eq',
                'normalize_sample_rate',
                'normalize_lufs',
                'reduce_sibilance'  # Moved to end - after all normalization
            ]
            
            total_fixes = len([f for f in fix_order if f in selected_fixes])
            current_fix = 0
            
            for fix_name in fix_order:
                if fix_name not in selected_fixes:
                    continue
                    
                current_fix += 1
                if progress_callback:
                    progress_callback(f"Applying {fix_name.replace('_', ' ').title()} ({current_fix}/{total_fixes})...")
                
                try:
                    if fix_name == 'remove_dc_offset':
                        audio_data, stats = self._remove_dc_offset(audio_data)
                    elif fix_name == 'trim_silence':
                        audio_data, stats = self._trim_silence(audio_data, sample_rate)
                    elif fix_name == 'fix_clipping':
                        audio_data, stats = self._fix_clipping(audio_data)
                    elif fix_name == 'reduce_noise':
                        audio_data, stats = self._reduce_noise(audio_data, sample_rate)
                    elif fix_name == 'normalize_volume':
                        audio_data, stats = self._normalize_volume(audio_data)
                    elif fix_name == 'optimize_dynamic_range':
                        audio_data, stats = self._optimize_dynamic_range(audio_data)
                    elif fix_name == 'enhance_clarity':
                        audio_data, stats = self._enhance_clarity(audio_data, sample_rate)
                    elif fix_name == 'reduce_sibilance':
                        audio_data, stats = self._reduce_sibilance(audio_data, sample_rate)
                    elif fix_name == 'slow_speaking_rate':
                        audio_data, stats = self._slow_speaking_rate(audio_data, sample_rate)
                    elif fix_name == 'apply_tts_eq':
                        audio_data, stats = self._apply_tts_eq(audio_data, sample_rate)
                    elif fix_name == 'normalize_sample_rate':
                        audio_data, sample_rate, stats = self._normalize_sample_rate(audio_data, sample_rate)
                    elif fix_name == 'normalize_lufs':
                        audio_data, stats = self._normalize_lufs(audio_data, sample_rate)
                    
                    results['fixes_applied'].append(fix_name)
                    results['statistics'][fix_name] = stats
                    
                except Exception as e:
                    print(f"Warning: Failed to apply {fix_name}: {e}")
                    continue
            
            if progress_callback:
                progress_callback("Saving processed audio...")
            
            # Save processed audio
            sf.write(output_path, audio_data, sample_rate, subtype='PCM_24')
            
            results.update({
                'final_duration': len(audio_data) / sample_rate,
                'final_sample_rate': sample_rate,
                'output_path': output_path
            })
            
            return results
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'fixes_applied': [],
                'statistics': {}
            }
    
    def _remove_dc_offset(self, audio: np.ndarray) -> tuple:
        """Remove DC offset from audio signal"""
        dc_offset = np.mean(audio)
        audio_fixed = audio - dc_offset
        
        stats = {
            'dc_offset_removed': float(dc_offset),
            'rms_change': float(np.sqrt(np.mean(audio_fixed**2)) / np.sqrt(np.mean(audio**2)))
        }
        
        return audio_fixed, stats
    
    def _trim_silence(self, audio: np.ndarray, sample_rate: int) -> tuple:
        """Trim silence from start and end"""
        # Use librosa's trim function
        audio_trimmed, trim_indices = librosa.effects.trim(
            audio, 
            top_db=30 if self.preserve_characteristics else 40,
            frame_length=2048,
            hop_length=512
        )
        
        start_trim = trim_indices[0] / sample_rate
        end_trim = (len(audio) - trim_indices[1]) / sample_rate
        
        stats = {
            'start_trimmed_seconds': float(start_trim),
            'end_trimmed_seconds': float(end_trim),
            'total_trimmed_seconds': float(start_trim + end_trim)
        }
        
        return audio_trimmed, stats
    
    def _fix_clipping(self, audio: np.ndarray) -> tuple:
        """Fix clipping using interpolation and soft limiting"""
        # Detect clipping
        clip_threshold = 0.95
        clipped_samples = np.abs(audio) >= clip_threshold
        clip_percentage = np.sum(clipped_samples) / len(audio) * 100
        
        if clip_percentage < 0.01:  # Less than 0.01% clipping
            return audio, {'clipping_detected': False, 'clip_percentage': float(clip_percentage)}
        
        audio_fixed = audio.copy()
        
        # Simple clipping repair using median filtering
        if np.sum(clipped_samples) > 0:
            # Apply median filter to clipped regions
            for i in np.where(clipped_samples)[0]:
                start = max(0, i - 5)
                end = min(len(audio_fixed), i + 6)
                if end - start > 3:
                    audio_fixed[i] = np.median(audio_fixed[start:end])
        
        # Apply soft limiting to prevent future clipping
        audio_fixed = np.tanh(audio_fixed * 0.9) * 0.95
        
        stats = {
            'clipping_detected': True,
            'clip_percentage_before': float(clip_percentage),
            'clip_percentage_after': float(np.sum(np.abs(audio_fixed) >= clip_threshold) / len(audio_fixed) * 100),
            'samples_repaired': int(np.sum(clipped_samples))
        }
        
        return audio_fixed, stats
    
    def _reduce_noise(self, audio: np.ndarray, sample_rate: int) -> tuple:
        """Reduce background noise using spectral subtraction"""
        # Simple spectral noise reduction
        # Estimate noise from first 0.5 seconds (assumed to be quieter)
        noise_duration = min(int(0.5 * sample_rate), len(audio) // 4)
        noise_sample = audio[:noise_duration]
        
        # Compute noise spectrum
        noise_fft = np.fft.fft(noise_sample)
        noise_magnitude = np.abs(noise_fft)
        noise_floor = np.mean(noise_magnitude)
        
        # Apply spectral subtraction in chunks
        chunk_size = 2048
        audio_denoised = np.zeros_like(audio)
        
        for i in range(0, len(audio) - chunk_size, chunk_size // 2):
            chunk = audio[i:i + chunk_size]
            if len(chunk) < chunk_size:
                chunk = np.pad(chunk, (0, chunk_size - len(chunk)))
            
            # FFT
            chunk_fft = np.fft.fft(chunk)
            chunk_magnitude = np.abs(chunk_fft)
            chunk_phase = np.angle(chunk_fft)
            
            # Noise reduction
            noise_reduction_factor = 0.3 if self.preserve_characteristics else 0.5
            reduction_mask = np.maximum(
                chunk_magnitude - noise_reduction_factor * noise_floor,
                0.1 * chunk_magnitude
            )
            
            # Reconstruct
            cleaned_fft = reduction_mask * np.exp(1j * chunk_phase)
            cleaned_chunk = np.real(np.fft.ifft(cleaned_fft))
            
            # Overlap-add
            end_idx = min(i + chunk_size, len(audio_denoised))
            audio_denoised[i:end_idx] += cleaned_chunk[:end_idx - i]
        
        # Normalize
        if np.max(np.abs(audio_denoised)) > 0:
            audio_denoised = audio_denoised / np.max(np.abs(audio_denoised)) * np.max(np.abs(audio))
        
        stats = {
            'noise_floor_estimated': float(noise_floor),
            'snr_improvement_db': float(20 * np.log10(np.std(audio_denoised) / np.std(audio - audio_denoised + 1e-10)))
        }
        
        return audio_denoised, stats
    
    def _normalize_volume(self, audio: np.ndarray) -> tuple:
        """Normalize volume consistency using dynamic range compression"""
        # Calculate RMS in overlapping windows
        window_size = 2048
        hop_size = 512
        rms_values = []
        
        for i in range(0, len(audio) - window_size, hop_size):
            window = audio[i:i + window_size]
            rms = np.sqrt(np.mean(window**2))
            rms_values.append(rms)
        
        rms_values = np.array(rms_values)
        target_rms = np.median(rms_values)
        
        # Apply gentle compression
        compression_ratio = 0.3 if self.preserve_characteristics else 0.5
        audio_compressed = np.zeros_like(audio)
        
        for i, rms in enumerate(rms_values):
            start_idx = i * hop_size
            end_idx = min(start_idx + window_size, len(audio))
            
            if rms > target_rms:
                # Compress loud parts
                gain = target_rms / rms
                gain = 1.0 + compression_ratio * (gain - 1.0)
            else:
                # Boost quiet parts (gentler)
                gain = target_rms / (rms + 1e-10)
                gain = 1.0 + 0.5 * compression_ratio * (gain - 1.0)
                gain = min(gain, 2.0)  # Limit boost
            
            audio_compressed[start_idx:end_idx] = audio[start_idx:end_idx] * gain
        
        stats = {
            'original_rms_std': float(np.std(rms_values)),
            'compressed_rms_std': float(np.std(rms_values * 0.5)),  # Approximate
            'compression_ratio': compression_ratio
        }
        
        return audio_compressed, stats
    
    def _optimize_dynamic_range(self, audio: np.ndarray) -> tuple:
        """Optimize dynamic range for TTS"""
        # Gentle expansion of dynamic range
        # Calculate percentiles
        p1, p99 = np.percentile(np.abs(audio), [1, 99])
        
        if p99 > p1:
            # Apply gentle expansion
            expansion_factor = 1.2 if self.preserve_characteristics else 1.5
            audio_expanded = np.sign(audio) * np.power(np.abs(audio) / p99, 1.0 / expansion_factor) * p99
            
            # Prevent clipping
            max_val = np.max(np.abs(audio_expanded))
            if max_val > 0.95:
                audio_expanded = audio_expanded * 0.95 / max_val
        else:
            audio_expanded = audio
        
        stats = {
            'original_dynamic_range_db': float(20 * np.log10(p99 / (p1 + 1e-10))),
            'optimized_dynamic_range_db': float(20 * np.log10(np.percentile(np.abs(audio_expanded), 99) / 
                                                           (np.percentile(np.abs(audio_expanded), 1) + 1e-10))),
            'expansion_factor': expansion_factor if p99 > p1 else 1.0
        }
        
        return audio_expanded, stats
    
    def _enhance_clarity(self, audio: np.ndarray, sample_rate: int) -> tuple:
        """Enhance voice clarity with subtle processing"""
        if not SCIPY_AVAILABLE:
            return audio, {'enhancement': 'scipy_not_available'}
        
        # Gentle high-frequency enhancement (presence boost)
        nyquist = sample_rate / 2
        enhancement_freq = 3000  # Hz
        enhancement_gain = 1.5 if self.preserve_characteristics else 2.0
        
        # Create a gentle high-shelf filter
        b, a = signal.butter(2, enhancement_freq / nyquist, btype='high')
        enhanced_highs = signal.filtfilt(b, a, audio)
        
        # Mix with original (subtle enhancement)
        mix_ratio = 0.2 if self.preserve_characteristics else 0.3
        audio_enhanced = (1 - mix_ratio) * audio + mix_ratio * enhanced_highs
        
        # Prevent clipping
        max_val = np.max(np.abs(audio_enhanced))
        if max_val > 0.95:
            audio_enhanced = audio_enhanced * 0.95 / max_val
        
        stats = {
            'enhancement_frequency_hz': enhancement_freq,
            'enhancement_gain_db': float(20 * np.log10(enhancement_gain)),
            'mix_ratio': mix_ratio
        }
        
        return audio_enhanced, stats
    
    def _slow_speaking_rate(self, audio: np.ndarray, sample_rate: int) -> tuple:
        """Slow down speaking rate for better TTS compatibility"""
        # Calculate how much to slow down based on preserve_characteristics setting
        if self.preserve_characteristics:
            slowdown_factor = 1.15  # 15% slower - subtle change
        else:
            slowdown_factor = 1.25  # 25% slower - more noticeable
        
        try:
            # Use librosa's time stretching (phase vocoder)
            # This preserves pitch while changing tempo
            audio_slowed = librosa.effects.time_stretch(audio, rate=1.0/slowdown_factor)
            
            # Calculate actual slowdown achieved
            actual_factor = len(audio_slowed) / len(audio)
            
            stats = {
                'target_slowdown_factor': slowdown_factor,
                'actual_slowdown_factor': float(actual_factor),
                'original_duration_seconds': float(len(audio) / sample_rate),
                'new_duration_seconds': float(len(audio_slowed) / sample_rate),
                'tempo_change_percent': float((actual_factor - 1.0) * 100)
            }
            
        except Exception as e:
            # Fallback: simple linear interpolation if librosa time_stretch fails
            print(f"Warning: Advanced time stretching failed ({e}), using simple method")
            
            # Calculate new length
            new_length = int(len(audio) * slowdown_factor)
            
            # Create time indices for interpolation
            old_indices = np.arange(len(audio))
            new_indices = np.linspace(0, len(audio) - 1, new_length)
            
            # Interpolate
            audio_slowed = np.interp(new_indices, old_indices, audio)
            
            actual_factor = len(audio_slowed) / len(audio)
            
            stats = {
                'target_slowdown_factor': slowdown_factor,
                'actual_slowdown_factor': float(actual_factor),
                'original_duration_seconds': float(len(audio) / sample_rate),
                'new_duration_seconds': float(len(audio_slowed) / sample_rate),
                'tempo_change_percent': float((actual_factor - 1.0) * 100),
                'method': 'fallback_interpolation'
            }
        
        return audio_slowed, stats
    
    def _apply_tts_eq(self, audio: np.ndarray, sample_rate: int) -> tuple:
        """Apply TTS-optimized equalization"""
        if not SCIPY_AVAILABLE:
            return audio, {'eq': 'scipy_not_available'}
        
        nyquist = sample_rate / 2
        
        # TTS-optimized EQ curve
        # Gentle low-cut (remove rumble)
        low_cut_freq = 80
        b_low, a_low = signal.butter(2, low_cut_freq / nyquist, btype='high')
        audio_eq = signal.filtfilt(b_low, a_low, audio)
        
        # Slight midrange boost (speech clarity)
        if self.preserve_characteristics:
            mid_freq = 1500
            mid_gain = 1.2
        else:
            mid_freq = 2000
            mid_gain = 1.3
        
        # Simple midrange boost using peaking filter approximation
        mid_q = 0.7
        w0 = 2 * np.pi * mid_freq / sample_rate
        alpha = np.sin(w0) / (2 * mid_q)
        A = np.sqrt(mid_gain)
        
        # Peaking EQ coefficients
        b0 = 1 + alpha * A
        b1 = -2 * np.cos(w0)
        b2 = 1 - alpha * A
        a0 = 1 + alpha / A
        a1 = -2 * np.cos(w0)
        a2 = 1 - alpha / A
        
        b = np.array([b0, b1, b2]) / a0
        a = np.array([1, a1 / a0, a2 / a0])
        
        audio_eq = signal.filtfilt(b, a, audio_eq)
        
        # Gentle high-frequency roll-off (reduce harshness)
        high_cut_freq = 8000
        b_high, a_high = signal.butter(2, high_cut_freq / nyquist, btype='low')
        audio_eq = signal.filtfilt(b_high, a_high, audio_eq)
        
        stats = {
            'low_cut_hz': low_cut_freq,
            'mid_boost_hz': mid_freq,
            'mid_boost_gain_db': float(20 * np.log10(mid_gain)),
            'high_cut_hz': high_cut_freq
        }
        
        return audio_eq, stats
    
    def _normalize_sample_rate(self, audio: np.ndarray, current_sr: int) -> tuple:
        """Normalize sample rate to target rate"""
        if current_sr == self.target_sample_rate:
            stats = {'resampling': 'not_needed', 'target_sr': self.target_sample_rate}
            return audio, current_sr, stats
        
        # Resample using librosa
        audio_resampled = librosa.resample(audio, orig_sr=current_sr, target_sr=self.target_sample_rate)
        
        stats = {
            'original_sample_rate': current_sr,
            'target_sample_rate': self.target_sample_rate,
            'length_change_ratio': float(len(audio_resampled) / len(audio))
        }
        
        return audio_resampled, self.target_sample_rate, stats
    
    def _reduce_sibilance(self, audio: np.ndarray, sample_rate: int) -> tuple:
        """Split-band de-esser for reducing harsh sibilant sounds"""
        if not SCIPY_AVAILABLE:
            return audio, {'de_essing': 'scipy_not_available'}
        
        # De-essing parameters
        sibilance_freq_low = 4000   # Hz - lower bound of sibilance range
        sibilance_freq_high = 10000 # Hz - upper bound of sibilance range
        threshold_db = -20 if self.preserve_characteristics else -15  # Threshold for sibilance detection
        reduction_ratio = 3.0 if self.preserve_characteristics else 5.0  # How much to compress sibilants
        
        nyquist = sample_rate / 2
        
        # Analyze sibilance content before processing
        original_sibilance_level = self._analyze_sibilance_level(audio, sample_rate)
        
        # Create sibilance detection filter (bandpass)
        low_norm = sibilance_freq_low / nyquist
        high_norm = min(sibilance_freq_high / nyquist, 0.95)  # Ensure we don't exceed Nyquist
        
        try:
            # Bandpass filter to isolate sibilance frequencies
            b_bp, a_bp = signal.butter(4, [low_norm, high_norm], btype='band')
            sibilance_signal = signal.filtfilt(b_bp, a_bp, audio)
            
            # Calculate sibilance envelope (RMS in overlapping windows)
            window_size = int(sample_rate * 0.01)  # 10ms windows
            hop_size = window_size // 4
            sibilance_envelope = np.zeros_like(audio)
            
            for i in range(0, len(audio) - window_size, hop_size):
                window_end = min(i + window_size, len(audio))
                sibilance_rms = np.sqrt(np.mean(sibilance_signal[i:window_end]**2))
                sibilance_envelope[i:window_end] = np.maximum(sibilance_envelope[i:window_end], sibilance_rms)
            
            # Convert to dB and create compression curve
            sibilance_db = 20 * np.log10(sibilance_envelope + 1e-10)
            
            # Calculate gain reduction
            gain_reduction = np.ones_like(audio)
            above_threshold = sibilance_db > threshold_db
            
            if np.any(above_threshold):
                # Apply compression to sibilant frequencies only
                excess_db = sibilance_db[above_threshold] - threshold_db
                compressed_excess = excess_db / reduction_ratio
                gain_reduction_db = excess_db - compressed_excess
                gain_reduction[above_threshold] = 10**(-gain_reduction_db / 20)
                
                # Smooth gain reduction to avoid clicks
                gain_reduction = signal.savgol_filter(gain_reduction, 
                                                    window_length=min(101, len(gain_reduction)//2*2+1), 
                                                    polyorder=3)
            
            # Apply split-band processing
            # Split audio into sibilance and non-sibilance bands
            sibilance_band = signal.filtfilt(b_bp, a_bp, audio)
            
            # Create complementary filters for non-sibilance frequencies
            # Low band: everything below sibilance range
            b_lp, a_lp = signal.butter(4, low_norm, btype='low')
            low_band = signal.filtfilt(b_lp, a_lp, audio)
            
            # High band: everything above sibilance range  
            b_hp, a_hp = signal.butter(4, high_norm, btype='high')
            high_band = signal.filtfilt(b_hp, a_hp, audio)
            
            # Non-sibilance band is just low + high (don't subtract sibilance)
            non_sibilance_band = low_band + high_band
            
            # Apply gain reduction only to sibilance band
            processed_sibilance = sibilance_band * gain_reduction
            
            # Recombine bands
            audio_deessed = non_sibilance_band + processed_sibilance
            
            # Analyze processed sibilance level
            processed_sibilance_level = self._analyze_sibilance_level(audio_deessed, sample_rate)
            
            # Prevent clipping
            max_val = np.max(np.abs(audio_deessed))
            if max_val > 0.95:
                audio_deessed = audio_deessed * 0.95 / max_val
            
            stats = {
                'sibilance_freq_range_hz': f"{sibilance_freq_low}-{sibilance_freq_high}",
                'threshold_db': threshold_db,
                'reduction_ratio': reduction_ratio,
                'original_sibilance_level_db': float(original_sibilance_level),
                'processed_sibilance_level_db': float(processed_sibilance_level),
                'sibilance_reduction_db': float(original_sibilance_level - processed_sibilance_level),
                'processing_method': 'split_band'
            }
            
        except Exception as e:
            # Fallback to simple high-frequency limiting
            print(f"Advanced de-essing failed ({e}), using simple method")
            
            # Simple high-frequency compression fallback
            b_hp, a_hp = signal.butter(2, sibilance_freq_low / nyquist, btype='high')
            high_freq = signal.filtfilt(b_hp, a_hp, audio)
            
            # Apply gentle compression to high frequencies
            compressed_high = np.tanh(high_freq * 2.0) * 0.5
            
            # Subtract original high frequencies and add compressed ones
            audio_deessed = audio - high_freq + compressed_high
            
            processed_sibilance_level = self._analyze_sibilance_level(audio_deessed, sample_rate)
            
            stats = {
                'sibilance_freq_range_hz': f"{sibilance_freq_low}-{sibilance_freq_high}",
                'original_sibilance_level_db': float(original_sibilance_level),
                'processed_sibilance_level_db': float(processed_sibilance_level),
                'sibilance_reduction_db': float(original_sibilance_level - processed_sibilance_level),
                'processing_method': 'fallback_simple'
            }
        
        return audio_deessed, stats
    
    def _analyze_sibilance_level(self, audio: np.ndarray, sample_rate: int) -> float:
        """Analyze the sibilance content of audio signal"""
        if not SCIPY_AVAILABLE:
            return 0.0
            
        # Focus on sibilance frequency range (4-10kHz)
        nyquist = sample_rate / 2
        low_freq = 4000 / nyquist
        high_freq = min(10000 / nyquist, 0.95)
        
        try:
            # Bandpass filter for sibilance range
            b, a = signal.butter(4, [low_freq, high_freq], btype='band')
            sibilance_signal = signal.filtfilt(b, a, audio)
            
            # Calculate RMS level of sibilance content
            sibilance_rms = np.sqrt(np.mean(sibilance_signal**2))
            sibilance_db = 20 * np.log10(sibilance_rms + 1e-10)
            
            return sibilance_db
            
        except Exception:
            return 0.0
    
    def _normalize_lufs(self, audio: np.ndarray, sample_rate: int) -> tuple:
        """Normalize to -16 LUFS (broadcast standard)"""
        # Simple RMS-based loudness normalization (approximates LUFS)
        target_lufs = -16.0
        
        # Calculate current RMS level
        rms = np.sqrt(np.mean(audio**2))
        current_lufs_approx = 20 * np.log10(rms + 1e-10)
        
        # Calculate gain needed
        gain_db = target_lufs - current_lufs_approx
        gain_linear = 10**(gain_db / 20)
        
        # Apply gain with safety limiting
        audio_normalized = audio * gain_linear
        
        # Prevent clipping
        max_val = np.max(np.abs(audio_normalized))
        if max_val > 0.95:
            audio_normalized = audio_normalized * 0.95 / max_val
            actual_gain_db = 20 * np.log10(0.95 / max_val * gain_linear)
        else:
            actual_gain_db = gain_db
        
        stats = {
            'target_lufs': target_lufs,
            'estimated_original_lufs': float(current_lufs_approx),
            'gain_applied_db': float(actual_gain_db),
            'peak_after_normalization': float(np.max(np.abs(audio_normalized)))
        }
        
        return audio_normalized, stats

def process_voice_sample(input_path: str, output_path: str, selected_fixes: List[str],
                        preserve_characteristics: bool = True, quality_level: int = 8,
                        progress_callback=None) -> Dict[str, Any]:
    """
    Convenience function to process a voice sample with selected fixes
    
    Args:
        input_path: Path to input audio file
        output_path: Path for processed output file
        selected_fixes: List of fix names to apply
        preserve_characteristics: Whether to preserve natural voice characteristics
        quality_level: Processing quality (1-10)
        progress_callback: Optional progress callback function
        
    Returns:
        Processing results dictionary
    """
    processor = AudioProcessor(preserve_characteristics, quality_level)
    return processor.process_audio(input_path, output_path, selected_fixes, progress_callback)