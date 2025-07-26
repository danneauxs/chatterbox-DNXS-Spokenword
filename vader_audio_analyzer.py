#!/usr/bin/env python3
"""
VADER Audio Comparison Analyzer
Objectively compares two audiobooks to detect VADER sentiment analysis effects
"""

import librosa
import numpy as np
import matplotlib.pyplot as plt
import soundfile as sf
from pathlib import Path
import json
from datetime import datetime
import argparse

def load_audio_safely(file_path):
    """Load audio file with error handling (supports WAV, M4B, MP3, FLAC, etc.)"""
    try:
        print(f"📂 Loading: {Path(file_path).name}")
        file_ext = Path(file_path).suffix.lower()
        
        if file_ext in ['.m4b', '.m4a', '.aac']:
            print(f"   🔄 Converting {file_ext} to audio data...")
        
        # librosa can handle most formats including M4B
        y, sr = librosa.load(file_path, sr=None)
        duration = len(y) / sr
        print(f"   ✅ Loaded: {duration:.1f}s at {sr}Hz")
        return y, sr
    except Exception as e:
        print(f"   ❌ Error loading {file_path}: {e}")
        print(f"   💡 Make sure ffmpeg is installed for M4B support")
        return None, None

def analyze_audio_features(y, sr, label="Audio"):
    """Extract comprehensive audio features"""
    print(f"🔬 Analyzing {label} features...")
    
    # Basic stats
    duration = len(y) / sr
    rms_energy = librosa.feature.rms(y=y)[0]
    
    # Pitch analysis (F0)
    f0, voiced_flag, voiced_probs = librosa.pyin(y, fmin=librosa.note_to_hz('C2'), fmax=librosa.note_to_hz('C7'))
    f0_clean = f0[~np.isnan(f0)]  # Remove NaN values
    
    # Spectral features
    spectral_centroids = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
    spectral_rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)[0]
    spectral_bandwidth = librosa.feature.spectral_bandwidth(y=y, sr=sr)[0]
    
    # Tempo and rhythm
    tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
    
    # Dynamic range
    db_levels = librosa.amplitude_to_db(np.abs(y))
    dynamic_range = np.max(db_levels) - np.min(db_levels)
    
    # MFCC (voice characteristics)
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    
    # Zero crossing rate (voice activity)
    zcr = librosa.feature.zero_crossing_rate(y)[0]
    
    return {
        'duration': duration,
        'sample_rate': sr,
        'rms_energy': {
            'mean': float(np.mean(rms_energy)),
            'std': float(np.std(rms_energy)),
            'min': float(np.min(rms_energy)),
            'max': float(np.max(rms_energy))
        },
        'pitch_f0': {
            'mean': float(np.mean(f0_clean)) if len(f0_clean) > 0 else 0,
            'std': float(np.std(f0_clean)) if len(f0_clean) > 0 else 0,
            'min': float(np.min(f0_clean)) if len(f0_clean) > 0 else 0,
            'max': float(np.max(f0_clean)) if len(f0_clean) > 0 else 0,
            'voiced_ratio': float(np.mean(voiced_flag))
        },
        'spectral_features': {
            'centroid_mean': float(np.mean(spectral_centroids)),
            'centroid_std': float(np.std(spectral_centroids)),
            'rolloff_mean': float(np.mean(spectral_rolloff)),
            'rolloff_std': float(np.std(spectral_rolloff)),
            'bandwidth_mean': float(np.mean(spectral_bandwidth)),
            'bandwidth_std': float(np.std(spectral_bandwidth))
        },
        'tempo': float(tempo),
        'dynamic_range_db': float(dynamic_range),
        'mfcc_means': [float(x) for x in np.mean(mfccs, axis=1)],
        'zero_crossing_rate': {
            'mean': float(np.mean(zcr)),
            'std': float(np.std(zcr))
        }
    }

def compare_features(features1, features2, label1="With VADER", label2="Without VADER"):
    """Compare two feature sets and calculate differences"""
    print(f"📊 Comparing {label1} vs {label2}...")
    
    comparison = {
        'analysis_date': datetime.now().isoformat(),
        'labels': {'file1': label1, 'file2': label2},
        'differences': {}
    }
    
    # Duration difference
    duration_diff = abs(features1['duration'] - features2['duration'])
    comparison['differences']['duration_diff_seconds'] = float(duration_diff)
    
    # RMS Energy differences
    rms1, rms2 = features1['rms_energy'], features2['rms_energy']
    comparison['differences']['rms_energy'] = {
        'mean_diff': float(abs(rms1['mean'] - rms2['mean'])),
        'std_diff': float(abs(rms1['std'] - rms2['std'])),
        'dynamic_range_diff': float(abs((rms1['max'] - rms1['min']) - (rms2['max'] - rms2['min'])))
    }
    
    # Pitch differences
    f01, f02 = features1['pitch_f0'], features2['pitch_f0']
    comparison['differences']['pitch_f0'] = {
        'mean_diff_hz': float(abs(f01['mean'] - f02['mean'])),
        'std_diff': float(abs(f01['std'] - f02['std'])),
        'range_diff': float(abs((f01['max'] - f01['min']) - (f02['max'] - f02['min']))),
        'voiced_ratio_diff': float(abs(f01['voiced_ratio'] - f02['voiced_ratio']))
    }
    
    # Spectral differences
    spec1, spec2 = features1['spectral_features'], features2['spectral_features']
    comparison['differences']['spectral'] = {
        'centroid_mean_diff': float(abs(spec1['centroid_mean'] - spec2['centroid_mean'])),
        'centroid_std_diff': float(abs(spec1['centroid_std'] - spec2['centroid_std'])),
        'rolloff_mean_diff': float(abs(spec1['rolloff_mean'] - spec2['rolloff_mean'])),
        'bandwidth_mean_diff': float(abs(spec1['bandwidth_mean'] - spec2['bandwidth_mean']))
    }
    
    # Tempo difference
    comparison['differences']['tempo_diff_bpm'] = float(abs(features1['tempo'] - features2['tempo']))
    
    # Dynamic range difference
    comparison['differences']['dynamic_range_diff_db'] = float(abs(features1['dynamic_range_db'] - features2['dynamic_range_db']))
    
    # MFCC differences (voice characteristics)
    mfcc_diffs = [abs(a - b) for a, b in zip(features1['mfcc_means'], features2['mfcc_means'])]
    comparison['differences']['mfcc_total_diff'] = float(sum(mfcc_diffs))
    
    # Zero crossing rate difference
    zcr1, zcr2 = features1['zero_crossing_rate'], features2['zero_crossing_rate']
    comparison['differences']['zcr_mean_diff'] = float(abs(zcr1['mean'] - zcr2['mean']))
    
    return comparison

def generate_comparison_report(comparison, features1, features2):
    """Generate human-readable comparison report"""
    print("\n" + "="*60)
    print("🎯 VADER AUDIO COMPARISON REPORT")
    print("="*60)
    
    diffs = comparison['differences']
    
    # Overall assessment
    print("\n📋 SUMMARY:")
    
    # Check for significant differences
    significant_changes = []
    
    if diffs['rms_energy']['mean_diff'] > 0.01:
        significant_changes.append(f"Energy difference: {diffs['rms_energy']['mean_diff']:.4f}")
    
    if diffs['pitch_f0']['mean_diff_hz'] > 2.0:  # 2Hz difference
        significant_changes.append(f"Pitch difference: {diffs['pitch_f0']['mean_diff_hz']:.1f}Hz")
    
    if diffs['pitch_f0']['std_diff'] > 5.0:  # Pitch variation difference
        significant_changes.append(f"Pitch variation difference: {diffs['pitch_f0']['std_diff']:.1f}Hz")
    
    if diffs['spectral']['centroid_mean_diff'] > 100:  # Spectral brightness
        significant_changes.append(f"Spectral brightness difference: {diffs['spectral']['centroid_mean_diff']:.0f}Hz")
    
    if diffs['dynamic_range_diff_db'] > 1.0:  # Dynamic range
        significant_changes.append(f"Dynamic range difference: {diffs['dynamic_range_diff_db']:.1f}dB")
    
    if diffs['mfcc_total_diff'] > 1.0:  # Voice characteristics
        significant_changes.append(f"Voice characteristic difference: {diffs['mfcc_total_diff']:.2f}")
    
    print(f"\n🎭 VADER IMPACT ASSESSMENT:")
    if significant_changes:
        print("✅ SIGNIFICANT DIFFERENCES DETECTED:")
        for change in significant_changes:
            print(f"   • {change}")
        print(f"\n🎯 VERDICT: VADER is making measurable changes to the audio!")
    else:
        print("❌ NO SIGNIFICANT DIFFERENCES DETECTED")
        print("🎯 VERDICT: VADER may not be making audible changes")
        print("💡 Possible reasons:")
        print("   • VADER sensitivity settings too low")
        print("   • Voice model not responsive to parameter changes")
        print("   • Text content has low emotional variation")
    
    # Detailed breakdown
    print(f"\n📊 DETAILED ANALYSIS:")
    print(f"Duration difference: {diffs['duration_diff_seconds']:.2f} seconds")
    print(f"Average energy difference: {diffs['rms_energy']['mean_diff']:.4f}")
    print(f"Pitch variation difference: {diffs['pitch_f0']['std_diff']:.1f}Hz")
    print(f"Spectral brightness difference: {diffs['spectral']['centroid_mean_diff']:.0f}Hz")
    print(f"Dynamic range difference: {diffs['dynamic_range_diff_db']:.1f}dB")
    print(f"Tempo difference: {diffs['tempo_diff_bpm']:.1f} BPM")
    
    return len(significant_changes) > 0

def create_visualization(features1, features2, y1, y2, sr1, sr2, output_dir):
    """Create visual comparison plots"""
    print("📈 Creating visualization plots...")
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle('VADER Audio Comparison Analysis', fontsize=16, fontweight='bold')
    
    # Plot 1: Waveform comparison (first 30 seconds)
    duration_plot = min(30, len(y1)/sr1, len(y2)/sr2)
    samples_plot = int(duration_plot * sr1)
    
    time1 = np.linspace(0, duration_plot, samples_plot)
    time2 = np.linspace(0, duration_plot, int(duration_plot * sr2))
    
    axes[0,0].plot(time1, y1[:samples_plot], alpha=0.7, label='With VADER')
    axes[0,0].plot(time2, y2[:int(duration_plot * sr2)], alpha=0.7, label='Without VADER')
    axes[0,0].set_title('Waveform Comparison (First 30s)')
    axes[0,0].set_xlabel('Time (seconds)')
    axes[0,0].set_ylabel('Amplitude')
    axes[0,0].legend()
    axes[0,0].grid(True)
    
    # Plot 2: RMS Energy comparison
    rms1 = librosa.feature.rms(y=y1)[0]
    rms2 = librosa.feature.rms(y=y2)[0]
    
    time_frames1 = np.linspace(0, len(y1)/sr1, len(rms1))
    time_frames2 = np.linspace(0, len(y2)/sr2, len(rms2))
    
    axes[0,1].plot(time_frames1, rms1, alpha=0.7, label='With VADER')
    axes[0,1].plot(time_frames2, rms2, alpha=0.7, label='Without VADER') 
    axes[0,1].set_title('RMS Energy Over Time')
    axes[0,1].set_xlabel('Time (seconds)')
    axes[0,1].set_ylabel('RMS Energy')
    axes[0,1].legend()
    axes[0,1].grid(True)
    
    # Plot 3: Spectral Centroid comparison
    cent1 = librosa.feature.spectral_centroid(y=y1, sr=sr1)[0]
    cent2 = librosa.feature.spectral_centroid(y=y2, sr=sr2)[0]
    
    axes[1,0].plot(time_frames1, cent1, alpha=0.7, label='With VADER')
    axes[1,0].plot(time_frames2, cent2, alpha=0.7, label='Without VADER')
    axes[1,0].set_title('Spectral Centroid (Brightness)')
    axes[1,0].set_xlabel('Time (seconds)')
    axes[1,0].set_ylabel('Hz')
    axes[1,0].legend()
    axes[1,0].grid(True)
    
    # Plot 4: Feature comparison bar chart
    features = ['Energy\nMean', 'Pitch\nMean', 'Pitch\nVariation', 'Spectral\nBrightness', 'Dynamic\nRange']
    vader_values = [
        features1['rms_energy']['mean'],
        features1['pitch_f0']['mean'] / 100,  # Scale for visibility
        features1['pitch_f0']['std'] / 10,    # Scale for visibility  
        features1['spectral_features']['centroid_mean'] / 1000,  # Scale for visibility
        features1['dynamic_range_db'] / 10     # Scale for visibility
    ]
    no_vader_values = [
        features2['rms_energy']['mean'],
        features2['pitch_f0']['mean'] / 100,
        features2['pitch_f0']['std'] / 10,
        features2['spectral_features']['centroid_mean'] / 1000,
        features2['dynamic_range_db'] / 10
    ]
    
    x = np.arange(len(features))
    width = 0.35
    
    axes[1,1].bar(x - width/2, vader_values, width, label='With VADER', alpha=0.7)
    axes[1,1].bar(x + width/2, no_vader_values, width, label='Without VADER', alpha=0.7)
    axes[1,1].set_title('Feature Comparison (Scaled)')
    axes[1,1].set_xticks(x)
    axes[1,1].set_xticklabels(features)
    axes[1,1].legend()
    axes[1,1].grid(True, axis='y')
    
    plt.tight_layout()
    
    # Save plot
    plot_path = Path(output_dir) / "vader_comparison_plots.png"
    plt.savefig(plot_path, dpi=300, bbox_inches='tight')
    print(f"📊 Plots saved to: {plot_path}")
    
    return plot_path

def main():
    parser = argparse.ArgumentParser(description="Compare two audiobooks to detect VADER effects")
    parser.add_argument("file1", help="Audio file with VADER")
    parser.add_argument("file2", help="Audio file without VADER")
    parser.add_argument("--output", "-o", default=".", help="Output directory for results")
    
    args = parser.parse_args()
    
    print("🎯 VADER Audio Comparison Analyzer")
    print("==================================")
    
    # Load audio files
    y1, sr1 = load_audio_safely(args.file1)
    y2, sr2 = load_audio_safely(args.file2)
    
    if y1 is None or y2 is None:
        print("❌ Failed to load audio files!")
        return
    
    # Analyze features
    features1 = analyze_audio_features(y1, sr1, "WITH VADER")
    features2 = analyze_audio_features(y2, sr2, "WITHOUT VADER")
    
    # Compare features
    comparison = compare_features(features1, features2)
    
    # Generate report
    has_differences = generate_comparison_report(comparison, features1, features2)
    
    # Create visualizations
    output_dir = Path(args.output)
    output_dir.mkdir(exist_ok=True)
    
    plot_path = create_visualization(features1, features2, y1, y2, sr1, sr2, output_dir)
    
    # Save detailed results
    results = {
        'features_with_vader': features1,
        'features_without_vader': features2,
        'comparison': comparison,
        'has_significant_differences': has_differences
    }
    
    json_path = output_dir / "vader_analysis_results.json"
    with open(json_path, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n💾 Full results saved to: {json_path}")
    print(f"📊 Visualization saved to: {plot_path}")
    
    if has_differences:
        print(f"\n🎉 CONCLUSION: VADER is working! Measurable differences detected.")
    else:
        print(f"\n🔧 CONCLUSION: VADER effects not detected. Consider adjusting sensitivity.")

if __name__ == "__main__":
    main()