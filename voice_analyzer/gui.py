"""
Standalone GUI for Voice Sample Analyzer
Clean interface for analyzing voice samples with file picker and results display.
"""

import sys
import os
from pathlib import Path
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout,
                            QWidget, QPushButton, QLabel, QFileDialog, QTextEdit,
                            QProgressBar, QScrollArea, QGroupBox, QGridLayout,
                            QSplitter, QTabWidget, QListWidget, QListWidgetItem,
                            QMessageBox, QCheckBox, QSpinBox)
from PyQt5.QtCore import QThread, pyqtSignal, Qt, QTimer
from PyQt5.QtGui import QFont, QPixmap
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from voice_analyzer.analyzer import analyze_voice_sample, analyze_multiple_samples, VoiceAnalysisResult
from voice_analyzer.visualizer import create_analysis_plots, create_comparison_plot, create_summary_report
from voice_analyzer.audio_processor import process_voice_sample

class AnalysisThread(QThread):
    """Background thread for voice analysis"""
    progress = pyqtSignal(str)  # Progress message
    result = pyqtSignal(object)  # Analysis result
    finished = pyqtSignal()
    error = pyqtSignal(str)
    
    def __init__(self, file_paths, detailed=True):
        super().__init__()
        self.file_paths = file_paths if isinstance(file_paths, list) else [file_paths]
        self.detailed = detailed
        
    def run(self):
        try:
            results = []
            for i, file_path in enumerate(self.file_paths):
                self.progress.emit(f"Analyzing {Path(file_path).name} ({i+1}/{len(self.file_paths)})...")
                result = analyze_voice_sample(file_path, self.detailed)
                results.append(result)
                self.result.emit(result)
            
            self.progress.emit("Analysis complete!")
            self.finished.emit()
            
        except Exception as e:
            self.error.emit(str(e))

class AudioProcessingThread(QThread):
    """Background thread for audio processing"""
    progress = pyqtSignal(str)  # Progress message
    finished = pyqtSignal(dict)  # Processing results
    error = pyqtSignal(str)
    
    def __init__(self, input_path, output_path, selected_fixes, preserve_characteristics, quality_level):
        super().__init__()
        self.input_path = input_path
        self.output_path = output_path
        self.selected_fixes = selected_fixes
        self.preserve_characteristics = preserve_characteristics
        self.quality_level = quality_level
        
    def run(self):
        try:
            def progress_callback(message):
                self.progress.emit(message)
            
            results = process_voice_sample(
                self.input_path,
                self.output_path, 
                self.selected_fixes,
                self.preserve_characteristics,
                self.quality_level,
                progress_callback
            )
            
            self.finished.emit(results)
            
        except Exception as e:
            self.error.emit(str(e))

class ScoreWidget(QWidget):
    """Widget to display a single score with color coding"""
    def __init__(self, label, score, max_score=100):
        super().__init__()
        self.setupUI(label, score, max_score)
        
    def setupUI(self, label, score, max_score):
        layout = QVBoxLayout(self)
        
        # Score label
        score_label = QLabel(f"{score:.1f}")
        score_label.setAlignment(Qt.AlignCenter)
        score_label.setFont(QFont("Arial", 16, QFont.Bold))
        
        # Color coding
        if score >= 75:
            color = "green"
        elif score >= 50:
            color = "orange"  
        else:
            color = "red"
            
        score_label.setStyleSheet(f"color: {color}; padding: 5px;")
        
        # Category label
        category_label = QLabel(label)
        category_label.setAlignment(Qt.AlignCenter)
        category_label.setFont(QFont("Arial", 10))
        category_label.setWordWrap(True)
        
        layout.addWidget(score_label)
        layout.addWidget(category_label)
        
        # Add border
        self.setStyleSheet("QWidget { border: 1px solid #ccc; border-radius: 5px; margin: 2px; }")

class VoiceAnalyzerGUI(QMainWindow):
    """Main GUI for voice sample analyzer"""
    
    def __init__(self):
        super().__init__()
        self.results = []
        self.current_result = None
        self.analysis_thread = None
        self.processing_thread = None
        self.setupUI()
        
    def setupUI(self):
        self.setWindowTitle("Voice Sample Analyzer for TTS")
        self.setGeometry(100, 100, 1400, 900)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QHBoxLayout(central_widget)
        
        # Left panel - File selection and controls
        left_panel = QWidget()
        left_panel.setMaximumWidth(300)
        left_layout = QVBoxLayout(left_panel)
        
        # File selection group
        file_group = QGroupBox("Voice Sample Selection")
        file_layout = QVBoxLayout(file_group)
        
        self.file_list = QListWidget()
        self.file_list.itemClicked.connect(self.on_file_selected)
        self.file_list.currentItemChanged.connect(self.on_file_selection_changed)
        file_layout.addWidget(self.file_list)
        
        # File buttons
        file_buttons = QHBoxLayout()
        self.add_file_btn = QPushButton("Add File")
        self.add_file_btn.clicked.connect(self.add_file)
        self.remove_file_btn = QPushButton("Remove")
        self.remove_file_btn.clicked.connect(self.remove_file)
        self.clear_files_btn = QPushButton("Clear All")
        self.clear_files_btn.clicked.connect(self.clear_files)
        
        file_buttons.addWidget(self.add_file_btn)
        file_buttons.addWidget(self.remove_file_btn)
        file_buttons.addWidget(self.clear_files_btn)
        file_layout.addLayout(file_buttons)
        
        left_layout.addWidget(file_group)
        
        # Analysis options
        options_group = QGroupBox("Analysis Options")
        options_layout = QVBoxLayout(options_group)
        
        self.detailed_analysis_cb = QCheckBox("Detailed Praat Analysis")
        self.detailed_analysis_cb.setChecked(True)
        self.detailed_analysis_cb.setToolTip("Enable advanced voice quality analysis using Praat")
        options_layout.addWidget(self.detailed_analysis_cb)
        
        left_layout.addWidget(options_group)
        
        # Analysis controls
        controls_group = QGroupBox("Analysis Controls")
        controls_layout = QVBoxLayout(controls_group)
        
        self.analyze_btn = QPushButton("🔍 Analyze Selected")
        self.analyze_btn.clicked.connect(self.analyze_selected)
        self.analyze_btn.setStyleSheet("QPushButton { font-size: 14px; padding: 8px; }")
        
        self.analyze_all_btn = QPushButton("🔍 Analyze All")
        self.analyze_all_btn.clicked.connect(self.analyze_all)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        
        self.status_label = QLabel("Ready")
        self.status_label.setStyleSheet("padding: 5px;")
        
        controls_layout.addWidget(self.analyze_btn)
        controls_layout.addWidget(self.analyze_all_btn)
        controls_layout.addWidget(self.progress_bar)
        controls_layout.addWidget(self.status_label)
        
        left_layout.addWidget(controls_group)
        
        # Export controls
        export_group = QGroupBox("Export Results")
        export_layout = QVBoxLayout(export_group)
        
        self.export_plot_btn = QPushButton("Save Plot")
        self.export_plot_btn.clicked.connect(self.export_plot)
        self.export_plot_btn.setEnabled(False)
        
        self.export_report_btn = QPushButton("Save Report")
        self.export_report_btn.clicked.connect(self.export_report)
        self.export_report_btn.setEnabled(False)
        
        export_layout.addWidget(self.export_plot_btn)
        export_layout.addWidget(self.export_report_btn)
        
        left_layout.addWidget(export_group)
        left_layout.addStretch()
        
        # Right panel - Results display
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        
        # Tab widget for different views
        self.tab_widget = QTabWidget()
        
        # Scores tab
        self.scores_tab = QWidget()
        self.setup_scores_tab()
        self.tab_widget.addTab(self.scores_tab, "Scores")
        
        # Visualization tab
        self.viz_tab = QWidget()
        self.setup_visualization_tab()
        self.tab_widget.addTab(self.viz_tab, "Analysis Plots")
        
        # Recommendations tab
        self.recommendations_tab = QWidget()
        self.setup_recommendations_tab()
        self.tab_widget.addTab(self.recommendations_tab, "Recommendations")
        
        # Comparison tab
        self.comparison_tab = QWidget()
        self.setup_comparison_tab()
        self.tab_widget.addTab(self.comparison_tab, "Compare Samples")
        
        # Auto-Fix tab
        self.autofix_tab = QWidget()
        self.setup_autofix_tab()
        self.tab_widget.addTab(self.autofix_tab, "Auto-Fix")
        
        right_layout.addWidget(self.tab_widget)
        
        # Add panels to main layout
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setSizes([300, 1100])
        
        main_layout.addWidget(splitter)
        
        # Status bar
        self.statusBar().showMessage("Ready - Add voice samples to begin analysis")
        
    def setup_scores_tab(self):
        """Setup the scores display tab"""
        layout = QVBoxLayout(self.scores_tab)
        
        # Overall score display
        self.overall_score_label = QLabel("No analysis results")
        self.overall_score_label.setAlignment(Qt.AlignCenter)
        self.overall_score_label.setFont(QFont("Arial", 18, QFont.Bold))
        self.overall_score_label.setStyleSheet("padding: 20px; border: 2px solid #ccc; border-radius: 10px; margin: 10px;")
        layout.addWidget(self.overall_score_label)
        
        # Detailed scores grid
        self.scores_grid = QGridLayout()
        self.scores_widget = QWidget()
        self.scores_widget.setLayout(self.scores_grid)
        
        scroll_area = QScrollArea()
        scroll_area.setWidget(self.scores_widget)
        scroll_area.setWidgetResizable(True)
        layout.addWidget(scroll_area)
        
    def setup_visualization_tab(self):
        """Setup the visualization tab with matplotlib"""
        layout = QVBoxLayout(self.viz_tab)
        
        # Matplotlib figure
        self.figure = Figure(figsize=(12, 8))
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)
        
        # Initially show placeholder
        ax = self.figure.add_subplot(111)
        ax.text(0.5, 0.5, 'Select a voice sample and run analysis\nto see detailed plots', 
                ha='center', va='center', fontsize=16, transform=ax.transAxes)
        ax.set_title('Voice Analysis Plots')
        self.canvas.draw()
        
    def setup_recommendations_tab(self):
        """Setup the recommendations tab"""
        layout = QVBoxLayout(self.recommendations_tab)
        
        self.recommendations_text = QTextEdit()
        self.recommendations_text.setReadOnly(True)
        self.recommendations_text.setFont(QFont("Consolas", 11))
        self.recommendations_text.setText("No recommendations available - run analysis first")
        
        layout.addWidget(self.recommendations_text)
        
    def setup_comparison_tab(self):
        """Setup the comparison tab"""
        layout = QVBoxLayout(self.comparison_tab)
        
        # Comparison matplotlib figure
        self.comparison_figure = Figure(figsize=(12, 8))
        self.comparison_canvas = FigureCanvas(self.comparison_figure)
        layout.addWidget(self.comparison_canvas)
        
        # Initially show placeholder
        ax = self.comparison_figure.add_subplot(111)
        ax.text(0.5, 0.5, 'Analyze multiple voice samples\nto see comparison plots', 
                ha='center', va='center', fontsize=16, transform=ax.transAxes)
        ax.set_title('Sample Comparison')
        self.comparison_canvas.draw()
        
    def setup_autofix_tab(self):
        """Setup the auto-fix tab with checkboxes for audio processing fixes"""
        layout = QVBoxLayout(self.autofix_tab)
        
        # Title and instructions
        title_label = QLabel("Automated Audio Processing Fixes")
        title_label.setFont(QFont("Arial", 14, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        instructions = QLabel("Select the fixes to apply to your voice sample. Each fix will only run when checked.")
        instructions.setWordWrap(True)
        instructions.setStyleSheet("color: #666; padding: 10px;")
        layout.addWidget(instructions)
        
        # Scroll area for fix options
        scroll_area = QScrollArea()
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        
        # Audio Quality Fixes Group
        audio_group = QGroupBox("Audio Quality Fixes")
        audio_layout = QVBoxLayout(audio_group)
        
        self.fix_clipping_cb = QCheckBox("Fix Clipping (0.22% detected)")
        self.fix_clipping_cb.setToolTip("Repair digital clipping using interpolation and soft limiting")
        audio_layout.addWidget(self.fix_clipping_cb)
        
        self.normalize_volume_cb = QCheckBox("Normalize Volume Consistency")
        self.normalize_volume_cb.setToolTip("Apply dynamic range compression to even out volume levels")
        audio_layout.addWidget(self.normalize_volume_cb)
        
        self.reduce_noise_cb = QCheckBox("Reduce Background Noise")
        self.reduce_noise_cb.setToolTip("Apply spectral noise reduction to improve SNR")
        audio_layout.addWidget(self.reduce_noise_cb)
        
        self.optimize_dynamic_range_cb = QCheckBox("Optimize Dynamic Range")
        self.optimize_dynamic_range_cb.setToolTip("Enhance dynamic range for better TTS compatibility")
        audio_layout.addWidget(self.optimize_dynamic_range_cb)
        
        scroll_layout.addWidget(audio_group)
        
        # Voice Enhancement Group
        voice_group = QGroupBox("Voice Enhancement")
        voice_layout = QVBoxLayout(voice_group)
        
        self.apply_tts_eq_cb = QCheckBox("Apply TTS-Optimized EQ")
        self.apply_tts_eq_cb.setToolTip("Apply frequency shaping optimized for TTS training")
        voice_layout.addWidget(self.apply_tts_eq_cb)
        
        self.normalize_lufs_cb = QCheckBox("Normalize to -16 LUFS")
        self.normalize_lufs_cb.setToolTip("Normalize loudness to broadcast standard (-16 LUFS)")
        voice_layout.addWidget(self.normalize_lufs_cb)
        
        self.enhance_clarity_cb = QCheckBox("Enhance Voice Clarity")
        self.enhance_clarity_cb.setToolTip("Apply subtle enhancement to improve voice definition")
        voice_layout.addWidget(self.enhance_clarity_cb)
        
        self.slow_speaking_rate_cb = QCheckBox("Slow Down Speaking Rate")
        self.slow_speaking_rate_cb.setToolTip("Reduce speaking tempo for better TTS compatibility and clarity")
        voice_layout.addWidget(self.slow_speaking_rate_cb)
        
        scroll_layout.addWidget(voice_group)
        
        # Advanced Processing Group
        advanced_group = QGroupBox("Advanced Processing")
        advanced_layout = QVBoxLayout(advanced_group)
        
        self.remove_dc_offset_cb = QCheckBox("Remove DC Offset")
        self.remove_dc_offset_cb.setToolTip("Remove any DC bias from the audio signal")
        advanced_layout.addWidget(self.remove_dc_offset_cb)
        
        self.normalize_sample_rate_cb = QCheckBox("Normalize Sample Rate to 24kHz")
        self.normalize_sample_rate_cb.setToolTip("Resample audio to optimal rate for TTS processing")
        advanced_layout.addWidget(self.normalize_sample_rate_cb)
        
        self.trim_silence_cb = QCheckBox("Trim Start/End Silence")
        self.trim_silence_cb.setToolTip("Remove excessive silence from beginning and end")
        advanced_layout.addWidget(self.trim_silence_cb)
        
        scroll_layout.addWidget(advanced_group)
        
        # Processing Controls
        controls_group = QGroupBox("Processing Controls")
        controls_layout = QVBoxLayout(controls_group)
        
        # Output quality setting
        quality_layout = QHBoxLayout()
        quality_layout.addWidget(QLabel("Output Quality:"))
        self.quality_spin = QSpinBox()
        self.quality_spin.setRange(1, 10)
        self.quality_spin.setValue(8)
        self.quality_spin.setToolTip("Processing quality (1=fast, 10=best quality)")
        quality_layout.addWidget(self.quality_spin)
        quality_layout.addStretch()
        controls_layout.addLayout(quality_layout)
        
        # Preserve characteristics checkbox
        self.preserve_characteristics_cb = QCheckBox("Preserve Natural Voice Characteristics")
        self.preserve_characteristics_cb.setChecked(True)
        self.preserve_characteristics_cb.setToolTip("Maintain pitch variation and breathing that makes TTS sound human")
        controls_layout.addWidget(self.preserve_characteristics_cb)
        
        scroll_layout.addWidget(controls_group)
        
        # Action buttons
        button_layout = QHBoxLayout()
        
        self.select_all_btn = QPushButton("Select All")
        self.select_all_btn.clicked.connect(self.select_all_fixes)
        button_layout.addWidget(self.select_all_btn)
        
        self.select_recommended_btn = QPushButton("Select Recommended")
        self.select_recommended_btn.clicked.connect(self.select_recommended_fixes)
        button_layout.addWidget(self.select_recommended_btn)
        
        self.clear_all_btn = QPushButton("Clear All")
        self.clear_all_btn.clicked.connect(self.clear_all_fixes)
        button_layout.addWidget(self.clear_all_btn)
        
        button_layout.addStretch()
        
        self.apply_fixes_btn = QPushButton("🔧 Apply Selected Fixes")
        self.apply_fixes_btn.clicked.connect(self.apply_audio_fixes)
        self.apply_fixes_btn.setStyleSheet("QPushButton { font-size: 14px; padding: 8px; background-color: #4CAF50; color: white; }")
        self.apply_fixes_btn.setEnabled(False)
        button_layout.addWidget(self.apply_fixes_btn)
        
        scroll_layout.addLayout(button_layout)
        
        # Progress and status
        self.fix_progress_bar = QProgressBar()
        self.fix_progress_bar.setVisible(False)
        scroll_layout.addWidget(self.fix_progress_bar)
        
        self.fix_status_label = QLabel("Select a voice sample and analysis result to enable fixes")
        self.fix_status_label.setStyleSheet("padding: 5px; color: #666;")
        scroll_layout.addWidget(self.fix_status_label)
        
        scroll_widget.setLayout(scroll_layout)
        scroll_area.setWidget(scroll_widget)
        scroll_area.setWidgetResizable(True)
        layout.addWidget(scroll_area)
        
        # Connect checkboxes to update function
        checkboxes = [
            self.fix_clipping_cb, self.normalize_volume_cb, self.reduce_noise_cb,
            self.optimize_dynamic_range_cb, self.apply_tts_eq_cb, self.normalize_lufs_cb,
            self.enhance_clarity_cb, self.slow_speaking_rate_cb, self.remove_dc_offset_cb, 
            self.normalize_sample_rate_cb, self.trim_silence_cb
        ]
        
        for cb in checkboxes:
            cb.stateChanged.connect(self.update_fix_ui_state)
            
    def select_all_fixes(self):
        """Select all fix checkboxes"""
        checkboxes = [
            self.fix_clipping_cb, self.normalize_volume_cb, self.reduce_noise_cb,
            self.optimize_dynamic_range_cb, self.apply_tts_eq_cb, self.normalize_lufs_cb,
            self.enhance_clarity_cb, self.slow_speaking_rate_cb, self.remove_dc_offset_cb, 
            self.normalize_sample_rate_cb, self.trim_silence_cb
        ]
        for cb in checkboxes:
            cb.setChecked(True)
            
    def select_recommended_fixes(self):
        """Select recommended fixes based on current analysis"""
        # Clear all first
        self.clear_all_fixes()
        
        if not self.current_result:
            return
            
        # Select fixes based on analysis scores
        if self.current_result.clipping_score < 90:
            self.fix_clipping_cb.setChecked(True)
            
        if self.current_result.noise_score < 75:
            self.reduce_noise_cb.setChecked(True)
            
        if self.current_result.dynamic_range_score < 70:
            self.optimize_dynamic_range_cb.setChecked(True)
            
        if self.current_result.consistency_score < 75:
            self.normalize_volume_cb.setChecked(True)
            
        if self.current_result.audio_quality_score < 80:
            self.apply_tts_eq_cb.setChecked(True)
            
        if self.current_result.speaking_rate_score < 75:
            self.slow_speaking_rate_cb.setChecked(True)
            
        # Always recommend these basic fixes
        self.remove_dc_offset_cb.setChecked(True)
        self.normalize_lufs_cb.setChecked(True)
        
    def clear_all_fixes(self):
        """Clear all fix checkboxes"""
        checkboxes = [
            self.fix_clipping_cb, self.normalize_volume_cb, self.reduce_noise_cb,
            self.optimize_dynamic_range_cb, self.apply_tts_eq_cb, self.normalize_lufs_cb,
            self.enhance_clarity_cb, self.slow_speaking_rate_cb, self.remove_dc_offset_cb, 
            self.normalize_sample_rate_cb, self.trim_silence_cb
        ]
        for cb in checkboxes:
            cb.setChecked(False)
            
    def update_fix_ui_state(self):
        """Update the fix UI state based on selections"""
        # Check if any fixes are selected
        checkboxes = [
            self.fix_clipping_cb, self.normalize_volume_cb, self.reduce_noise_cb,
            self.optimize_dynamic_range_cb, self.apply_tts_eq_cb, self.normalize_lufs_cb,
            self.enhance_clarity_cb, self.slow_speaking_rate_cb, self.remove_dc_offset_cb, 
            self.normalize_sample_rate_cb, self.trim_silence_cb
        ]
        
        any_selected = any(cb.isChecked() for cb in checkboxes)
        has_current_file = self.current_result is not None
        
        self.apply_fixes_btn.setEnabled(any_selected and has_current_file)
        
        if any_selected and has_current_file:
            selected_count = sum(1 for cb in checkboxes if cb.isChecked())
            self.fix_status_label.setText(f"Ready to apply {selected_count} fixes to {self.current_result.filename}")
        elif not has_current_file:
            self.fix_status_label.setText("Select and analyze a voice sample to enable fixes")
        else:
            self.fix_status_label.setText("Select fixes to apply")
            
    def apply_audio_fixes(self):
        """Apply selected audio fixes to the current voice sample"""
        if not self.current_result:
            QMessageBox.warning(self, "No Sample", "Please select and analyze a voice sample first.")
            return
            
        # Get the current file path
        current_item = self.file_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "No Selection", "Please select a voice sample from the list.")
            return
            
        input_file_path = current_item.data(Qt.UserRole)
        
        # Ask user for output file location
        from pathlib import Path
        input_path = Path(input_file_path)
        default_output = input_path.parent / f"{input_path.stem}_fixed{input_path.suffix}"
        
        output_file_path, _ = QFileDialog.getSaveFileName(
            self, "Save Fixed Audio File", 
            str(default_output),
            "Audio Files (*.wav *.mp3 *.flac);;All Files (*)"
        )
        
        if not output_file_path:
            return
            
        # Collect selected fixes
        selected_fixes = []
        if self.fix_clipping_cb.isChecked():
            selected_fixes.append("fix_clipping")
        if self.normalize_volume_cb.isChecked():
            selected_fixes.append("normalize_volume")
        if self.reduce_noise_cb.isChecked():
            selected_fixes.append("reduce_noise")
        if self.optimize_dynamic_range_cb.isChecked():
            selected_fixes.append("optimize_dynamic_range")
        if self.apply_tts_eq_cb.isChecked():
            selected_fixes.append("apply_tts_eq")
        if self.normalize_lufs_cb.isChecked():
            selected_fixes.append("normalize_lufs")
        if self.enhance_clarity_cb.isChecked():
            selected_fixes.append("enhance_clarity")
        if self.slow_speaking_rate_cb.isChecked():
            selected_fixes.append("slow_speaking_rate")
        if self.remove_dc_offset_cb.isChecked():
            selected_fixes.append("remove_dc_offset")
        if self.normalize_sample_rate_cb.isChecked():
            selected_fixes.append("normalize_sample_rate")
        if self.trim_silence_cb.isChecked():
            selected_fixes.append("trim_silence")
            
        if not selected_fixes:
            QMessageBox.information(self, "No Fixes Selected", "Please select at least one fix to apply.")
            return
            
        # Show confirmation dialog
        fix_count = len(selected_fixes)
        quality_level = self.quality_spin.value()
        preserve_characteristics = self.preserve_characteristics_cb.isChecked()
        
        msg = f"Apply {fix_count} audio fixes to:\n{Path(input_file_path).name}\n\n"
        msg += f"Quality Level: {quality_level}/10\n"
        msg += f"Preserve Natural Characteristics: {'Yes' if preserve_characteristics else 'No'}\n\n"
        msg += f"Output: {Path(output_file_path).name}"
        
        reply = QMessageBox.question(self, "Confirm Audio Processing", msg,
                                   QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            self.start_audio_processing(input_file_path, output_file_path, selected_fixes, 
                                      preserve_characteristics, quality_level)
    
    def start_audio_processing(self, input_path, output_path, selected_fixes, preserve_characteristics, quality_level):
        """Start audio processing in background thread"""
        if self.processing_thread and self.processing_thread.isRunning():
            QMessageBox.information(self, "Processing Running", "Please wait for current processing to complete.")
            return
            
        self.processing_thread = AudioProcessingThread(
            input_path, output_path, selected_fixes, preserve_characteristics, quality_level
        )
        
        self.processing_thread.progress.connect(self.update_processing_progress)
        self.processing_thread.finished.connect(self.processing_finished)
        self.processing_thread.error.connect(self.processing_error)
        
        # Update UI for processing state
        self.fix_progress_bar.setVisible(True)
        self.fix_progress_bar.setRange(0, 0)  # Indeterminate
        self.apply_fixes_btn.setEnabled(False)
        self.fix_status_label.setText("Processing audio...")
        
        # Disable other controls during processing
        self.analyze_btn.setEnabled(False)
        self.analyze_all_btn.setEnabled(False)
        
        self.processing_thread.start()
    
    def update_processing_progress(self, message):
        """Update processing progress display"""
        self.fix_status_label.setText(message)
        self.statusBar().showMessage(f"Audio Processing: {message}")
    
    def processing_finished(self, results):
        """Handle processing completion"""
        self.fix_progress_bar.setVisible(False)
        self.apply_fixes_btn.setEnabled(True)
        self.analyze_btn.setEnabled(True)
        self.analyze_all_btn.setEnabled(True)
        
        if results['success']:
            fixes_count = len(results['fixes_applied'])
            duration_change = results['final_duration'] - results['original_duration']
            
            # Show detailed results
            message = f"✅ Audio processing complete!\n\n"
            message += f"Applied {fixes_count} fixes successfully\n"
            message += f"Original duration: {results['original_duration']:.2f}s\n"
            message += f"Final duration: {results['final_duration']:.2f}s\n"
            message += f"Duration change: {duration_change:+.2f}s\n"
            message += f"Sample rate: {results['original_sample_rate']}Hz → {results['final_sample_rate']}Hz\n\n"
            message += f"Output saved to:\n{Path(results['output_path']).name}"
            
            # Add some interesting statistics
            if 'statistics' in results and results['statistics']:
                message += "\n\nProcessing Statistics:\n"
                for fix_name, stats in results['statistics'].items():
                    if isinstance(stats, dict):
                        for key, value in stats.items():
                            if isinstance(value, float) and abs(value) > 0.001:
                                message += f"• {fix_name}: {key} = {value:.3f}\n"
            
            QMessageBox.information(self, "Processing Complete", message)
            self.fix_status_label.setText(f"Processing complete! {fixes_count} fixes applied successfully.")
            
            # Ask if user wants to analyze the processed file
            reply = QMessageBox.question(
                self, "Analyze Processed File", 
                "Would you like to add and analyze the processed file to compare results?",
                QMessageBox.Yes | QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                # Add processed file to the list
                processed_path = results['output_path']
                item = QListWidgetItem(Path(processed_path).name)
                item.setData(Qt.UserRole, processed_path)
                item.setToolTip(processed_path)
                self.file_list.addItem(item)
                
                # Select and analyze it
                self.file_list.setCurrentItem(item)
                self.analyze_selected()
        else:
            QMessageBox.critical(self, "Processing Failed", 
                               f"Audio processing failed:\n{results.get('error', 'Unknown error')}")
            self.fix_status_label.setText("Processing failed - see error message")
    
    def processing_error(self, error_message):
        """Handle processing error"""
        self.fix_progress_bar.setVisible(False)
        self.apply_fixes_btn.setEnabled(True)
        self.analyze_btn.setEnabled(True)
        self.analyze_all_btn.setEnabled(True)
        
        QMessageBox.critical(self, "Processing Error", f"Audio processing error:\n{error_message}")
        self.fix_status_label.setText("Processing failed")
        
    def add_file(self):
        """Add voice sample file"""
        file_paths, _ = QFileDialog.getOpenFileNames(
            self, "Select Voice Samples", "",
            "Audio Files (*.wav *.mp3 *.flac *.m4a *.ogg);;All Files (*)"
        )
        
        for file_path in file_paths:
            if file_path:
                item = QListWidgetItem(Path(file_path).name)
                item.setData(Qt.UserRole, file_path)
                item.setToolTip(file_path)
                self.file_list.addItem(item)
        
        self.update_ui_state()
        
    def remove_file(self):
        """Remove selected file"""
        current_item = self.file_list.currentItem()
        current_row = self.file_list.currentRow()
        
        if current_row >= 0 and current_item:
            # Get the file name to remove from results
            file_path = current_item.data(Qt.UserRole)
            file_name = Path(file_path).name
            
            # Remove from file list
            self.file_list.takeItem(current_row)
            
            # Remove corresponding result if exists
            self.results = [r for r in self.results if r.filename != file_name]
            
            # Clear current result if it was the removed file
            if self.current_result and self.current_result.filename == file_name:
                self.current_result = None
                self.clear_displays()
                
        self.update_ui_state()
        
    def clear_files(self):
        """Clear all files"""
        self.file_list.clear()
        self.results.clear()
        self.current_result = None
        self.update_ui_state()
        self.clear_displays()
        
    def on_file_selected(self, item):
        """Handle file selection"""
        if item:
            file_path = item.data(Qt.UserRole)
            # Find corresponding result
            file_name = Path(file_path).name
            for result in self.results:
                if result.filename == file_name:
                    self.current_result = result
                    self.update_result_display(result)
                    break
        self.update_ui_state()
        
    def on_file_selection_changed(self, current_item, previous_item):
        """Handle file selection change (including keyboard navigation)"""
        if current_item:
            self.on_file_selected(current_item)
        else:
            self.update_ui_state()
        
    def analyze_selected(self):
        """Analyze selected file"""
        current_item = self.file_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "No Selection", "Please select a voice sample to analyze.")
            return
            
        file_path = current_item.data(Qt.UserRole)
        self.start_analysis([file_path])
        
    def analyze_all(self):
        """Analyze all files"""
        if self.file_list.count() == 0:
            QMessageBox.warning(self, "No Files", "Please add voice samples to analyze.")
            return
            
        file_paths = []
        for i in range(self.file_list.count()):
            item = self.file_list.item(i)
            file_paths.append(item.data(Qt.UserRole))
            
        self.start_analysis(file_paths)
        
    def start_analysis(self, file_paths):
        """Start analysis in background thread"""
        if self.analysis_thread and self.analysis_thread.isRunning():
            QMessageBox.information(self, "Analysis Running", "Please wait for current analysis to complete.")
            return
            
        self.analysis_thread = AnalysisThread(file_paths, self.detailed_analysis_cb.isChecked())
        self.analysis_thread.progress.connect(self.update_progress)
        self.analysis_thread.result.connect(self.add_result)
        self.analysis_thread.finished.connect(self.analysis_finished)
        self.analysis_thread.error.connect(self.analysis_error)
        
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)  # Indeterminate
        self.analyze_btn.setEnabled(False)
        self.analyze_all_btn.setEnabled(False)
        
        self.analysis_thread.start()
        
    def update_progress(self, message):
        """Update progress display"""
        self.status_label.setText(message)
        self.statusBar().showMessage(message)
        
    def add_result(self, result):
        """Add analysis result"""
        # Update existing result or add new
        existing_index = -1
        for i, existing_result in enumerate(self.results):
            if existing_result.filename == result.filename:
                existing_index = i
                break
                
        if existing_index >= 0:
            self.results[existing_index] = result
        else:
            self.results.append(result)
            
        # Update display if this is the current selection
        current_item = self.file_list.currentItem()
        if current_item and Path(current_item.data(Qt.UserRole)).name == result.filename:
            self.current_result = result
            self.update_result_display(result)
            
    def analysis_finished(self):
        """Handle analysis completion"""
        self.progress_bar.setVisible(False)
        self.analyze_btn.setEnabled(True)
        self.analyze_all_btn.setEnabled(True)
        self.status_label.setText("Analysis complete")
        self.statusBar().showMessage("Analysis complete - select a sample to view results")
        
        # Update comparison plot if multiple results
        if len(self.results) > 1:
            self.update_comparison_plot()
            
        self.update_ui_state()
        
    def analysis_error(self, error_message):
        """Handle analysis error"""
        self.progress_bar.setVisible(False)
        self.analyze_btn.setEnabled(True) 
        self.analyze_all_btn.setEnabled(True)
        self.status_label.setText("Analysis failed")
        QMessageBox.critical(self, "Analysis Error", f"Analysis failed:\n{error_message}")
        
    def update_result_display(self, result):
        """Update the display with analysis result"""
        if not result.success:
            self.overall_score_label.setText(f"Analysis Failed: {result.error_message}")
            return
            
        # Update overall score
        color = "green" if result.overall_score >= 75 else "orange" if result.overall_score >= 50 else "red"
        self.overall_score_label.setText(f"{result.filename}\nOverall Score: {result.overall_score:.1f}/100\n{result.suitability_rating}")
        self.overall_score_label.setStyleSheet(f"padding: 20px; border: 2px solid {color}; border-radius: 10px; margin: 10px; color: {color};")
        
        # Update detailed scores grid
        self.clear_scores_grid()
        
        scores_data = [
            ("Audio Quality", result.audio_quality_score),
            ("Noise Level", result.noise_score),
            ("Dynamic Range", result.dynamic_range_score),
            ("Clipping", result.clipping_score),
            ("Pitch Stability", result.pitch_stability_score),
            ("Voice Quality", result.voice_quality_score),
            ("Speaking Rate", result.speaking_rate_score),
            ("Consistency", result.consistency_score)
        ]
        
        for i, (label, score) in enumerate(scores_data):
            row = i // 4
            col = i % 4
            score_widget = ScoreWidget(label, score)
            self.scores_grid.addWidget(score_widget, row, col)
            
        # Update recommendations
        recommendations_text = f"Analysis Results for: {result.filename}\n"
        recommendations_text += "=" * 60 + "\n\n"
        recommendations_text += f"Duration: {result.duration:.2f} seconds\n"
        recommendations_text += f"Sample Rate: {result.sample_rate} Hz\n"
        recommendations_text += f"Channels: {result.channels}\n\n"
        recommendations_text += "Recommendations:\n"
        recommendations_text += "-" * 20 + "\n"
        
        for i, rec in enumerate(result.recommendations, 1):
            recommendations_text += f"{i}. {rec}\n"
            
        if result.metrics:
            recommendations_text += "\nTechnical Metrics:\n"
            recommendations_text += "-" * 20 + "\n"
            for key, value in result.metrics.items():
                if isinstance(value, float):
                    recommendations_text += f"{key}: {value:.3f}\n"
                else:
                    recommendations_text += f"{key}: {value}\n"
                    
        self.recommendations_text.setText(recommendations_text)
        
        # Update visualization
        self.update_visualization(result)
        
        # Update auto-fix UI state
        self.update_fix_ui_state()
        
    def clear_scores_grid(self):
        """Clear the scores grid"""
        while self.scores_grid.count():
            child = self.scores_grid.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
                
    def update_visualization(self, result):
        """Update the visualization plots"""
        if not result.success:
            return
            
        # Find the file path for this result
        file_path = None
        for i in range(self.file_list.count()):
            item = self.file_list.item(i)
            if Path(item.data(Qt.UserRole)).name == result.filename:
                file_path = item.data(Qt.UserRole)
                break
                
        if not file_path:
            return
            
        try:
            self.figure.clear()
            create_analysis_plots(file_path, result)
            # Copy the plots to our figure
            # This is a bit complex, so for now just show a simple plot
            ax = self.figure.add_subplot(111)
            
            # Create a simple summary plot
            categories = ['Audio\nQuality', 'Noise', 'Dynamic\nRange', 'Clipping', 
                         'Pitch\nStability', 'Voice\nQuality', 'Speaking\nRate', 'Consistency']
            scores = [result.audio_quality_score, result.noise_score, result.dynamic_range_score,
                     result.clipping_score, result.pitch_stability_score, result.voice_quality_score,
                     result.speaking_rate_score, result.consistency_score]
            
            colors = ['red' if s < 50 else 'orange' if s < 75 else 'green' for s in scores]
            bars = ax.bar(categories, scores, color=colors, alpha=0.7)
            
            ax.set_title(f'Quality Scores - {result.filename}', fontsize=14, fontweight='bold')
            ax.set_ylabel('Score')
            ax.set_ylim(0, 100)
            ax.axhline(y=50, color='red', linestyle='--', alpha=0.5)
            ax.axhline(y=75, color='orange', linestyle='--', alpha=0.5)
            plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
            
            # Add score values on bars
            for bar, score in zip(bars, scores):
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height + 1,
                        f'{score:.0f}', ha='center', va='bottom', fontsize=10)
                        
            self.figure.tight_layout()
            self.canvas.draw()
            
        except Exception as e:
            ax = self.figure.add_subplot(111)
            ax.text(0.5, 0.5, f'Visualization error:\n{str(e)}', 
                    ha='center', va='center', transform=ax.transAxes)
            self.canvas.draw()
            
    def update_comparison_plot(self):
        """Update comparison plot"""
        if len(self.results) < 2:
            return
            
        try:
            self.comparison_figure.clear()
            
            # Create comparison plot
            ax1 = self.comparison_figure.add_subplot(2, 1, 1)
            ax2 = self.comparison_figure.add_subplot(2, 1, 2)
            
            # Overall scores
            filenames = [r.filename[:15] + '...' if len(r.filename) > 15 else r.filename for r in self.results]
            overall_scores = [r.overall_score for r in self.results]
            
            colors = ['red' if s < 50 else 'orange' if s < 75 else 'green' for s in overall_scores]
            bars1 = ax1.bar(range(len(filenames)), overall_scores, color=colors, alpha=0.7)
            ax1.set_title('Overall TTS Suitability Scores')
            ax1.set_ylabel('Score')
            ax1.set_ylim(0, 100)
            ax1.set_xticks(range(len(filenames)))
            ax1.set_xticklabels(filenames, rotation=45, ha='right')
            ax1.axhline(y=50, color='red', linestyle='--', alpha=0.5)
            ax1.axhline(y=75, color='orange', linestyle='--', alpha=0.5)
            ax1.grid(True, alpha=0.3)
            
            # Add score values
            for bar, score in zip(bars1, overall_scores):
                height = bar.get_height()
                ax1.text(bar.get_x() + bar.get_width()/2., height + 1,
                        f'{score:.0f}', ha='center', va='bottom', fontsize=9)
            
            # Detailed comparison (just show a few key metrics)
            import numpy as np
            categories = ['Audio Qual.', 'Noise', 'Pitch Stab.', 'Voice Qual.']
            x = np.arange(len(categories))
            width = 0.8 / len(self.results)
            
            for i, result in enumerate(self.results):
                scores = [result.audio_quality_score, result.noise_score, 
                         result.pitch_stability_score, result.voice_quality_score]
                ax2.bar(x + i * width, scores, width, label=filenames[i], alpha=0.7)
            
            ax2.set_title('Key Quality Metrics Comparison')
            ax2.set_ylabel('Score')
            ax2.set_ylim(0, 100)
            ax2.set_xticks(x + width * (len(self.results) - 1) / 2)
            ax2.set_xticklabels(categories)
            ax2.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
            ax2.grid(True, alpha=0.3)
            
            self.comparison_figure.tight_layout()
            self.comparison_canvas.draw()
            
        except Exception as e:
            ax = self.comparison_figure.add_subplot(111)
            ax.text(0.5, 0.5, f'Comparison error:\n{str(e)}', 
                    ha='center', va='center', transform=ax.transAxes)
            self.comparison_canvas.draw()
            
    def update_ui_state(self):
        """Update UI element states"""
        has_files = self.file_list.count() > 0
        has_results = len(self.results) > 0
        
        self.analyze_btn.setEnabled(has_files and self.file_list.currentItem() is not None)
        self.analyze_all_btn.setEnabled(has_files)
        self.remove_file_btn.setEnabled(self.file_list.currentItem() is not None)
        self.clear_files_btn.setEnabled(has_files)
        self.export_plot_btn.setEnabled(has_results and self.current_result is not None)
        self.export_report_btn.setEnabled(has_results and self.current_result is not None)
        
    def clear_displays(self):
        """Clear all result displays"""
        self.overall_score_label.setText("No analysis results")
        self.overall_score_label.setStyleSheet("padding: 20px; border: 2px solid #ccc; border-radius: 10px; margin: 10px;")
        
        self.clear_scores_grid()
        self.recommendations_text.setText("No recommendations available - run analysis first")
        
        # Clear plots
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.text(0.5, 0.5, 'Select a voice sample and run analysis\nto see detailed plots', 
                ha='center', va='center', fontsize=16, transform=ax.transAxes)
        ax.set_title('Voice Analysis Plots')
        self.canvas.draw()
        
        self.comparison_figure.clear()
        ax = self.comparison_figure.add_subplot(111)
        ax.text(0.5, 0.5, 'Analyze multiple voice samples\nto see comparison plots', 
                ha='center', va='center', fontsize=16, transform=ax.transAxes)
        ax.set_title('Sample Comparison')
        self.comparison_canvas.draw()
        
    def export_plot(self):
        """Export current analysis plot"""
        if not self.current_result:
            return
            
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save Analysis Plot", 
            f"{self.current_result.filename}_analysis.png",
            "PNG Files (*.png);;PDF Files (*.pdf);;All Files (*)"
        )
        
        if file_path:
            try:
                self.figure.savefig(file_path, dpi=150, bbox_inches='tight')
                QMessageBox.information(self, "Export Success", f"Plot saved to:\n{file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Export Error", f"Failed to save plot:\n{str(e)}")
                
    def export_report(self):
        """Export current analysis report"""
        if not self.current_result:
            return
            
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save Analysis Report", 
            f"{self.current_result.filename}_report.txt",
            "Text Files (*.txt);;All Files (*)"
        )
        
        if file_path:
            try:
                report = create_summary_report(self.current_result)
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(report)
                QMessageBox.information(self, "Export Success", f"Report saved to:\n{file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Export Error", f"Failed to save report:\n{str(e)}")

def main():
    """Run the standalone voice analyzer GUI"""
    app = QApplication(sys.argv)
    app.setApplicationName("Voice Sample Analyzer")
    
    # Set application style
    app.setStyle('Fusion')
    
    window = VoiceAnalyzerGUI()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()