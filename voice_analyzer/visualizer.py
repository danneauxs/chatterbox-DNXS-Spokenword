"""
Visualization Functions for Voice Analysis
Creates plots and visual reports for voice sample analysis results.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from pathlib import Path
from typing import List, Optional
import warnings
warnings.filterwarnings('ignore')

try:
    import librosa
    import librosa.display
    import parselmouth
    DEPENDENCIES_AVAILABLE = True
except ImportError:
    DEPENDENCIES_AVAILABLE = False

from voice_analyzer.analyzer import VoiceAnalysisResult

def create_analysis_plots(file_path: str, result: VoiceAnalysisResult, save_path: Optional[str] = None) -> plt.Figure:
    """
    Create comprehensive analysis plots for a voice sample.
    
    Args:
        file_path: Path to the audio file
        result: Analysis results
        save_path: Optional path to save the plot
        
    Returns:
        matplotlib Figure object
    """
    if not DEPENDENCIES_AVAILABLE:
        fig, ax = plt.subplots(1, 1, figsize=(10, 6))
        ax.text(0.5, 0.5, 'Missing dependencies for visualization', 
                ha='center', va='center', fontsize=16)
        ax.set_title('Visualization Error')
        return fig
    
    # Load audio for visualization
    try:
        audio_data, sr = librosa.load(file_path, sr=None)
    except Exception as e:
        fig, ax = plt.subplots(1, 1, figsize=(10, 6))
        ax.text(0.5, 0.5, f'Error loading audio: {e}', 
                ha='center', va='center', fontsize=12)
        ax.set_title('Audio Loading Error')
        return fig
    
    # Create subplot layout
    fig = plt.figure(figsize=(16, 12))
    fig.suptitle(f'Voice Analysis: {result.filename}', fontsize=16, fontweight='bold')
    
    # 1. Waveform
    ax1 = plt.subplot(3, 3, 1)
    time_axis = np.linspace(0, len(audio_data) / sr, len(audio_data))
    ax1.plot(time_axis, audio_data, alpha=0.7, color='blue')
    ax1.set_title('Waveform')
    ax1.set_xlabel('Time (s)')
    ax1.set_ylabel('Amplitude')
    ax1.grid(True, alpha=0.3)
    
    # 2. Spectrogram
    ax2 = plt.subplot(3, 3, 2)
    D = librosa.stft(audio_data)
    S_db = librosa.amplitude_to_db(np.abs(D), ref=np.max)
    img = librosa.display.specshow(S_db, x_axis='time', y_axis='hz', sr=sr, ax=ax2)
    ax2.set_title('Spectrogram')
    plt.colorbar(img, ax=ax2, format='%+2.0f dB')
    
    # 3. Pitch tracking (if available)
    ax3 = plt.subplot(3, 3, 3)
    if 'f0_mean_hz' in result.metrics:
        try:
            sound = parselmouth.Sound(file_path)
            pitch = sound.to_pitch(time_step=0.01)
            pitch_values = pitch.selected_array['frequency']
            time_values = pitch.xs()
            
            # Plot pitch
            voiced_mask = pitch_values > 0
            ax3.plot(time_values[voiced_mask], pitch_values[voiced_mask], 'b-', alpha=0.7)
            ax3.axhline(y=result.metrics['f0_mean_hz'], color='r', linestyle='--', 
                       label=f"Mean: {result.metrics['f0_mean_hz']:.1f} Hz")
            ax3.set_title('Pitch Tracking')
            ax3.set_xlabel('Time (s)')
            ax3.set_ylabel('F0 (Hz)')
            ax3.legend()
        except:
            ax3.text(0.5, 0.5, 'Pitch analysis\nnot available', 
                    ha='center', va='center', transform=ax3.transAxes)
            ax3.set_title('Pitch Tracking')
    else:
        ax3.text(0.5, 0.5, 'Basic analysis mode\nPitch tracking unavailable', 
                ha='center', va='center', transform=ax3.transAxes)
        ax3.set_title('Pitch Tracking')
    ax3.grid(True, alpha=0.3)
    
    # 4. Spectral features
    ax4 = plt.subplot(3, 3, 4)
    spectral_centroids = librosa.feature.spectral_centroid(y=audio_data, sr=sr)[0]
    spectral_rolloff = librosa.feature.spectral_rolloff(y=audio_data, sr=sr)[0]
    frames = range(len(spectral_centroids))
    t = librosa.frames_to_time(frames, sr=sr)
    
    ax4.plot(t, spectral_centroids, label='Spectral Centroid', alpha=0.7)
    ax4.plot(t, spectral_rolloff, label='Spectral Rolloff', alpha=0.7)
    ax4.set_title('Spectral Features')
    ax4.set_xlabel('Time (s)')
    ax4.set_ylabel('Hz')
    ax4.legend()
    ax4.grid(True, alpha=0.3)
    
    # 5. Dynamic range analysis
    ax5 = plt.subplot(3, 3, 5)
    rms = librosa.feature.rms(y=audio_data, frame_length=2048, hop_length=512)[0]
    rms_time = librosa.frames_to_time(range(len(rms)), sr=sr)
    rms_db = 20 * np.log10(rms + 1e-10)
    
    ax5.plot(rms_time, rms_db, color='green', alpha=0.7)
    ax5.axhline(y=20*np.log10(result.metrics.get('rms_level', 0.1) + 1e-10), 
               color='r', linestyle='--', label='Average RMS')
    ax5.set_title('RMS Level (dB)')
    ax5.set_xlabel('Time (s)')
    ax5.set_ylabel('dB')
    ax5.legend()
    ax5.grid(True, alpha=0.3)
    
    # 6. Score visualization
    ax6 = plt.subplot(3, 3, 6)
    categories = ['Audio\nQuality', 'Noise', 'Dynamic\nRange', 'Clipping', 
                 'Pitch\nStability', 'Voice\nQuality', 'Speaking\nRate', 'Consistency']
    scores = [result.audio_quality_score, result.noise_score, result.dynamic_range_score,
             result.clipping_score, result.pitch_stability_score, result.voice_quality_score,
             result.speaking_rate_score, result.consistency_score]
    
    colors = ['red' if s < 50 else 'orange' if s < 75 else 'green' for s in scores]
    bars = ax6.bar(categories, scores, color=colors, alpha=0.7)
    ax6.set_title('Quality Scores')
    ax6.set_ylabel('Score')
    ax6.set_ylim(0, 100)
    ax6.axhline(y=50, color='red', linestyle='--', alpha=0.5)
    ax6.axhline(y=75, color='orange', linestyle='--', alpha=0.5)
    plt.setp(ax6.get_xticklabels(), rotation=45, ha='right')
    
    # Add score values on bars
    for bar, score in zip(bars, scores):
        height = bar.get_height()
        ax6.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{score:.0f}', ha='center', va='bottom', fontsize=8)
    
    # 7. Overall score gauge
    ax7 = plt.subplot(3, 3, 7)
    _create_score_gauge(ax7, result.overall_score, result.suitability_rating)
    
    # 8. Frequency response
    ax8 = plt.subplot(3, 3, 8)
    fft = np.fft.fft(audio_data)
    magnitude = np.abs(fft)
    freqs = np.fft.fftfreq(len(fft), 1/sr)
    
    # Only plot positive frequencies up to Nyquist
    positive_freqs = freqs[:len(freqs)//2]
    positive_magnitude = magnitude[:len(magnitude)//2]
    
    ax8.semilogx(positive_freqs[1:], 20*np.log10(positive_magnitude[1:] + 1e-10))
    ax8.set_title('Frequency Response')
    ax8.set_xlabel('Frequency (Hz)')
    ax8.set_ylabel('Magnitude (dB)')
    ax8.grid(True, alpha=0.3)
    ax8.set_xlim(20, sr//2)
    
    # 9. Recommendations box
    ax9 = plt.subplot(3, 3, 9)
    ax9.axis('off')
    recommendations_text = '\n'.join([f"• {rec}" for rec in result.recommendations[:6]])
    if len(result.recommendations) > 6:
        recommendations_text += f"\n... and {len(result.recommendations) - 6} more"
    
    ax9.text(0.05, 0.95, 'Recommendations:', fontweight='bold', 
            transform=ax9.transAxes, va='top')
    ax9.text(0.05, 0.85, recommendations_text, transform=ax9.transAxes, 
            va='top', fontsize=9, wrap=True)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"Analysis plot saved to: {save_path}")
    
    return fig

def _create_score_gauge(ax, score: float, rating: str):
    """Create a gauge-style visualization for overall score"""
    # Clear the axis
    ax.clear()
    ax.set_xlim(-1.1, 1.1)
    ax.set_ylim(-1.1, 1.1)
    ax.set_aspect('equal')
    ax.axis('off')
    
    # Create gauge background
    theta = np.linspace(0, np.pi, 100)
    x_outer = 1.0 * np.cos(theta)
    y_outer = 1.0 * np.sin(theta)
    x_inner = 0.7 * np.cos(theta)
    y_inner = 0.7 * np.sin(theta)
    
    # Color segments
    segments = [(0, 50, 'red'), (50, 75, 'orange'), (75, 100, 'green')]
    
    for start, end, color in segments:
        start_angle = np.pi * (1 - start/100)
        end_angle = np.pi * (1 - end/100)
        segment_theta = np.linspace(start_angle, end_angle, 20)
        
        segment_x_outer = 1.0 * np.cos(segment_theta)
        segment_y_outer = 1.0 * np.sin(segment_theta)
        segment_x_inner = 0.7 * np.cos(segment_theta)
        segment_y_inner = 0.7 * np.sin(segment_theta)
        
        # Create polygon for segment
        segment_x = np.concatenate([segment_x_outer, segment_x_inner[::-1]])
        segment_y = np.concatenate([segment_y_outer, segment_y_inner[::-1]])
        
        ax.fill(segment_x, segment_y, color=color, alpha=0.3)
    
    # Add gauge outline
    ax.plot(x_outer, y_outer, 'k-', linewidth=2)
    ax.plot(x_inner, y_inner, 'k-', linewidth=2)
    ax.plot([x_outer[0], x_inner[0]], [y_outer[0], y_inner[0]], 'k-', linewidth=2)
    ax.plot([x_outer[-1], x_inner[-1]], [y_outer[-1], y_inner[-1]], 'k-', linewidth=2)
    
    # Add needle
    needle_angle = np.pi * (1 - score/100)
    needle_x = 0.9 * np.cos(needle_angle)
    needle_y = 0.9 * np.sin(needle_angle)
    ax.plot([0, needle_x], [0, needle_y], 'k-', linewidth=3)
    ax.plot(0, 0, 'ko', markersize=8)
    
    # Add score text
    ax.text(0, -0.3, f'{score:.1f}', ha='center', va='center', fontsize=20, fontweight='bold')
    ax.text(0, -0.5, rating, ha='center', va='center', fontsize=14)
    ax.text(0, 1.2, 'Overall Score', ha='center', va='center', fontsize=12, fontweight='bold')
    
    # Add scale labels
    for score_val, label_x in [(0, -1), (25, -0.7), (50, 0), (75, 0.7), (100, 1)]:
        angle = np.pi * (1 - score_val/100)
        label_y = 1.15 * np.sin(angle)
        label_x_pos = 1.15 * np.cos(angle)
        ax.text(label_x_pos, label_y, str(score_val), ha='center', va='center', fontsize=10)

def create_comparison_plot(results: List[VoiceAnalysisResult], save_path: Optional[str] = None) -> plt.Figure:
    """Create comparison plot for multiple voice samples"""
    if not results:
        fig, ax = plt.subplots(1, 1, figsize=(10, 6))
        ax.text(0.5, 0.5, 'No results to compare', ha='center', va='center', fontsize=16)
        return fig
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))
    fig.suptitle('Voice Sample Comparison', fontsize=16, fontweight='bold')
    
    # Prepare data
    filenames = [r.filename for r in results]
    overall_scores = [r.overall_score for r in results]
    
    # 1. Overall scores comparison
    colors = ['red' if s < 50 else 'orange' if s < 75 else 'green' for s in overall_scores]
    bars1 = ax1.bar(range(len(filenames)), overall_scores, color=colors, alpha=0.7)
    ax1.set_title('Overall TTS Suitability Scores')
    ax1.set_ylabel('Score')
    ax1.set_ylim(0, 100)
    ax1.set_xticks(range(len(filenames)))
    ax1.set_xticklabels([f[:20] + '...' if len(f) > 20 else f for f in filenames], rotation=45, ha='right')
    ax1.axhline(y=50, color='red', linestyle='--', alpha=0.5)
    ax1.axhline(y=75, color='orange', linestyle='--', alpha=0.5)
    ax1.grid(True, alpha=0.3)
    
    # Add score values on bars
    for bar, score in zip(bars1, overall_scores):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{score:.0f}', ha='center', va='bottom', fontsize=10)
    
    # 2. Detailed scores comparison (radar/spider chart would be ideal, but using grouped bars)
    categories = ['Audio Qual.', 'Noise', 'Dyn. Range', 'Clipping', 
                 'Pitch Stab.', 'Voice Qual.', 'Speaking Rate', 'Consistency']
    
    x = np.arange(len(categories))
    width = 0.8 / len(results)
    
    for i, result in enumerate(results):
        scores = [result.audio_quality_score, result.noise_score, result.dynamic_range_score,
                 result.clipping_score, result.pitch_stability_score, result.voice_quality_score,
                 result.speaking_rate_score, result.consistency_score]
        
        ax2.bar(x + i * width, scores, width, label=result.filename[:15], alpha=0.7)
    
    ax2.set_title('Detailed Score Comparison')
    ax2.set_ylabel('Score')
    ax2.set_ylim(0, 100)
    ax2.set_xticks(x + width * (len(results) - 1) / 2)
    ax2.set_xticklabels(categories, rotation=45, ha='right')
    ax2.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
        print(f"Comparison plot saved to: {save_path}")
    
    return fig

def create_summary_report(result: VoiceAnalysisResult, save_path: Optional[str] = None) -> str:
    """Create a text summary report"""
    report = f"""
Voice Sample Analysis Report
{'=' * 50}

File: {result.filename}
Duration: {result.duration:.2f} seconds
Sample Rate: {result.sample_rate} Hz
Channels: {result.channels}

Overall Assessment
{'=' * 20}
Overall Score: {result.overall_score:.1f}/100
Suitability Rating: {result.suitability_rating}

Detailed Scores
{'=' * 15}
Audio Quality: {result.audio_quality_score:.1f}/100
Noise Level: {result.noise_score:.1f}/100
Dynamic Range: {result.dynamic_range_score:.1f}/100
Clipping: {result.clipping_score:.1f}/100
Pitch Stability: {result.pitch_stability_score:.1f}/100
Voice Quality: {result.voice_quality_score:.1f}/100
Speaking Rate: {result.speaking_rate_score:.1f}/100
Consistency: {result.consistency_score:.1f}/100

Technical Metrics
{'=' * 17}
"""
    
    for key, value in result.metrics.items():
        if isinstance(value, float):
            report += f"{key}: {value:.3f}\n"
        else:
            report += f"{key}: {value}\n"
    
    report += f"""
Recommendations
{'=' * 15}
"""
    for i, rec in enumerate(result.recommendations, 1):
        report += f"{i}. {rec}\n"
    
    if save_path:
        with open(save_path, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"Summary report saved to: {save_path}")
    
    return report