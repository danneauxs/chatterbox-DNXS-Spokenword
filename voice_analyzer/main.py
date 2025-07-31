#!/usr/bin/env python3
"""
Voice Sample Analyzer - Main Entry Point
Standalone launcher for the voice analysis tool.
"""

import sys
import argparse
from pathlib import Path

def main():
    """Main entry point with command line options"""
    parser = argparse.ArgumentParser(
        description="Voice Sample Analyzer for TTS Suitability Assessment",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                          # Launch GUI
  python main.py --cli voice.wav          # CLI analysis of single file
  python main.py --cli voice1.wav voice2.wav  # CLI analysis of multiple files
  python main.py --batch /path/to/voices/ # Batch analyze directory
        """
    )
    
    parser.add_argument('files', nargs='*', help='Voice sample files to analyze')
    parser.add_argument('--cli', action='store_true', help='Run in command-line mode')
    parser.add_argument('--batch', metavar='DIR', help='Batch analyze all audio files in directory')
    parser.add_argument('--detailed', action='store_true', default=True, help='Enable detailed Praat analysis (default)')
    parser.add_argument('--basic', action='store_true', help='Use basic analysis only (faster, no Praat)')
    parser.add_argument('--output', '-o', metavar='DIR', help='Output directory for reports and plots')
    parser.add_argument('--format', choices=['text', 'json', 'csv'], default='text', help='Output format for CLI mode')
    
    args = parser.parse_args()
    
    # Determine analysis mode
    detailed_analysis = args.detailed and not args.basic
    
    if args.cli or args.batch or args.files:
        # Command-line mode
        run_cli_mode(args, detailed_analysis)
    else:
        # GUI mode (default)
        run_gui_mode()

def run_gui_mode():
    """Launch the GUI application"""
    try:
        # Add current directory to path for imports
        import os
        sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        
        from voice_analyzer.gui import main as gui_main
        print("🎤 Launching Voice Sample Analyzer GUI...")
        gui_main()
    except ImportError as e:
        print(f"❌ Error launching GUI: {e}")
        print("Make sure all dependencies are installed:")
        print("pip install -r voice_analyzer/requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"❌ GUI error: {e}")
        sys.exit(1)

def run_cli_mode(args, detailed_analysis):
    """Run in command-line mode"""
    try:
        # Add current directory to path for imports
        import os
        sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        
        from voice_analyzer.analyzer import analyze_voice_sample, analyze_multiple_samples
        from voice_analyzer.visualizer import create_summary_report, create_analysis_plots
        import json
        import csv
        
        # Collect files to analyze
        files_to_analyze = []
        
        if args.batch:
            # Batch mode - analyze directory
            batch_dir = Path(args.batch)
            if not batch_dir.exists():
                print(f"❌ Directory not found: {batch_dir}")
                sys.exit(1)
                
            audio_extensions = {'.wav', '.mp3', '.flac', '.m4a', '.ogg', '.aiff', '.au'}
            for ext in audio_extensions:
                files_to_analyze.extend(batch_dir.glob(f"*{ext}"))
                files_to_analyze.extend(batch_dir.glob(f"*{ext.upper()}"))
                
            if not files_to_analyze:
                print(f"❌ No audio files found in: {batch_dir}")
                sys.exit(1)
                
            print(f"📁 Found {len(files_to_analyze)} audio files in {batch_dir}")
            
        elif args.files:
            # Individual files
            for file_path in args.files:
                path = Path(file_path)
                if path.exists():
                    files_to_analyze.append(path)
                else:
                    print(f"⚠️ File not found: {file_path}")
                    
        if not files_to_analyze:
            print("❌ No valid files to analyze")
            sys.exit(1)
            
        # Setup output directory
        output_dir = Path(args.output) if args.output else Path.cwd() / "voice_analysis_results"
        output_dir.mkdir(exist_ok=True)
        
        print(f"🔍 Analyzing {len(files_to_analyze)} voice sample(s)...")
        print(f"📊 Analysis mode: {'Detailed (Praat + librosa)' if detailed_analysis else 'Basic (librosa only)'}")
        print(f"📁 Output directory: {output_dir}")
        print()
        
        # Analyze files
        results = []
        for i, file_path in enumerate(files_to_analyze, 1):
            print(f"[{i}/{len(files_to_analyze)}] Analyzing: {file_path.name}")
            
            try:
                result = analyze_voice_sample(str(file_path), detailed_analysis)
                results.append(result)
                
                if result.success:
                    print(f"   ✅ Score: {result.overall_score:.1f}/100 ({result.suitability_rating})")
                else:
                    print(f"   ❌ Failed: {result.error_message}")
                    
            except Exception as e:
                print(f"   ❌ Error: {e}")
                
        print(f"\n🎉 Analysis complete! Processed {len(results)} files.")
        
        # Generate outputs
        successful_results = [r for r in results if r.success]
        if successful_results:
            generate_cli_outputs(successful_results, output_dir, args.format)
        else:
            print("❌ No successful analyses to report")
            
    except ImportError as e:
        print(f"❌ Missing dependencies: {e}")
        print("Install required packages:")
        print("pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"❌ CLI error: {e}")
        sys.exit(1)

def generate_cli_outputs(results, output_dir, format_type):
    """Generate output files for CLI results"""
    print(f"\n📝 Generating {format_type.upper()} reports...")
    
    try:
        if format_type == 'text':
            generate_text_reports(results, output_dir)
        elif format_type == 'json':
            generate_json_report(results, output_dir)
        elif format_type == 'csv':
            generate_csv_report(results, output_dir)
            
        print(f"✅ Reports saved to: {output_dir}")
        
    except Exception as e:
        print(f"❌ Error generating reports: {e}")

def generate_text_reports(results, output_dir):
    """Generate individual text reports"""
    from voice_analyzer.visualizer import create_summary_report
    
    for result in results:
        if result.success:
            report_path = output_dir / f"{Path(result.filename).stem}_analysis.txt"
            create_summary_report(result, str(report_path))
            
    # Generate summary report
    summary_path = output_dir / "analysis_summary.txt"
    with open(summary_path, 'w', encoding='utf-8') as f:
        f.write("Voice Sample Analysis Summary\n")
        f.write("=" * 50 + "\n\n")
        
        for result in results:
            if result.success:
                f.write(f"File: {result.filename}\n")
                f.write(f"Overall Score: {result.overall_score:.1f}/100 ({result.suitability_rating})\n")
                f.write(f"Duration: {result.duration:.2f}s, Sample Rate: {result.sample_rate}Hz\n")
                f.write(f"Top Issues: {', '.join(result.recommendations[:3])}\n")
                f.write("-" * 40 + "\n")

def generate_json_report(results, output_dir):
    """Generate JSON report"""
    import json
    
    json_data = {
        "analysis_summary": {
            "total_samples": len(results),
            "successful_analyses": len([r for r in results if r.success]),
            "average_score": sum(r.overall_score for r in results if r.success) / len([r for r in results if r.success]) if results else 0
        },
        "results": []
    }
    
    for result in results:
        result_data = {
            "filename": result.filename,
            "success": result.success,
            "overall_score": result.overall_score,
            "suitability_rating": result.suitability_rating,
            "duration": result.duration,
            "sample_rate": result.sample_rate,
            "channels": result.channels,
            "scores": {
                "audio_quality": result.audio_quality_score,
                "noise": result.noise_score,
                "dynamic_range": result.dynamic_range_score,
                "clipping": result.clipping_score,
                "pitch_stability": result.pitch_stability_score,
                "voice_quality": result.voice_quality_score,
                "speaking_rate": result.speaking_rate_score,
                "consistency": result.consistency_score
            },
            "metrics": result.metrics,
            "recommendations": result.recommendations
        }
        
        if not result.success:
            result_data["error"] = result.error_message
            
        json_data["results"].append(result_data)
    
    json_path = output_dir / "analysis_results.json"
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=2, ensure_ascii=False)

def generate_csv_report(results, output_dir):
    """Generate CSV report"""
    import csv
    
    csv_path = output_dir / "analysis_results.csv"
    
    fieldnames = [
        'filename', 'success', 'overall_score', 'suitability_rating',
        'duration', 'sample_rate', 'channels',
        'audio_quality_score', 'noise_score', 'dynamic_range_score', 'clipping_score',
        'pitch_stability_score', 'voice_quality_score', 'speaking_rate_score', 'consistency_score',
        'f0_mean_hz', 'snr_db', 'spectral_centroid_hz', 'primary_recommendation'
    ]
    
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        
        for result in results:
            row = {
                'filename': result.filename,
                'success': result.success,
                'overall_score': result.overall_score,
                'suitability_rating': result.suitability_rating,
                'duration': result.duration,
                'sample_rate': result.sample_rate,
                'channels': result.channels,
                'audio_quality_score': result.audio_quality_score,
                'noise_score': result.noise_score,
                'dynamic_range_score': result.dynamic_range_score,
                'clipping_score': result.clipping_score,
                'pitch_stability_score': result.pitch_stability_score,
                'voice_quality_score': result.voice_quality_score,
                'speaking_rate_score': result.speaking_rate_score,
                'consistency_score': result.consistency_score,
                'f0_mean_hz': result.metrics.get('f0_mean_hz', ''),
                'snr_db': result.metrics.get('snr_db', ''),
                'spectral_centroid_hz': result.metrics.get('spectral_centroid_hz', ''),
                'primary_recommendation': result.recommendations[0] if result.recommendations else ''
            }
            writer.writerow(row)

if __name__ == "__main__":
    main()