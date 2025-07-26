#!/usr/bin/env python3
"""
ChatterboxTTS GUI Interface
A proper GUI wrapper for the main_launcher.py functionality
"""

import sys
import os
import subprocess
import threading
from pathlib import Path
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout,
                            QGridLayout, QWidget, QPushButton, QLabel, QLineEdit,
                            QSpinBox, QDoubleSpinBox, QComboBox, QTextEdit,
                            QFileDialog, QProgressBar, QGroupBox, QCheckBox,
                            QMessageBox, QSplitter, QFrame, QListWidget, QTabWidget,
                            QFormLayout, QSlider, QSpacerItem, QSizePolicy)
from PyQt5.QtCore import QThread, pyqtSignal, QTimer, pyqtSlot, Qt
from PyQt5.QtGui import QFont, QPixmap, QIcon

# Import the existing modules
from config.config import *
from interface import main as interface_main
from modules.resume_handler import find_incomplete_books
from tools.combine_only import run_combine_only_mode
from wrapper.chunk_tool import run_chunk_repair_tool
from utils.generate_from_json import main as generate_from_json_main


class ProcessThread(QThread):
    """Thread to run background processes without blocking GUI"""
    output_signal = pyqtSignal(str)
    finished_signal = pyqtSignal(bool, str)

    def __init__(self, target_function, *args, **kwargs):
        super().__init__()
        self.target_function = target_function
        self.args = args
        self.kwargs = kwargs

    def run(self):
        try:
            result = self.target_function(*self.args, **self.kwargs)
            self.finished_signal.emit(True, "Process completed successfully")
        except Exception as e:
            self.finished_signal.emit(False, str(e))


class ChatterboxMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ChatterboxTTS - Audiobook Generator")
        self.setGeometry(100, 100, 1200, 800)
        
        # Central widget with tabs
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        
        # Create tab widget
        self.tab_widget = QTabWidget()
        layout.addWidget(self.tab_widget)
        
        # Create tabs for each main menu option
        self.create_convert_book_tab()
        self.create_resume_tab()
        self.create_combine_tab()
        self.create_prepare_text_tab()
        self.create_test_chunking_tab()
        self.create_repair_tool_tab()
        self.create_json_generate_tab()
        
        # Output area at bottom
        self.create_output_area(layout)
        
        # Status bar
        self.statusBar().showMessage("Ready")

    def create_convert_book_tab(self):
        """Tab 1: Convert a book (GenTTS) - Main functionality"""
        tab = QWidget()
        self.tab_widget.addTab(tab, "1. Convert Book")
        
        layout = QVBoxLayout(tab)
        
        # Book Selection Group
        book_group = QGroupBox("📚 Book Selection")
        book_layout = QFormLayout(book_group)
        
        self.book_path_edit = QLineEdit()
        self.book_path_edit.setPlaceholderText("Select book folder...")
        book_browse_btn = QPushButton("Browse...")
        book_browse_btn.clicked.connect(self.browse_book_folder)
        
        book_row = QHBoxLayout()
        book_row.addWidget(self.book_path_edit)
        book_row.addWidget(book_browse_btn)
        book_layout.addRow("Book Folder:", book_row)
        
        # Text file selection (populated after book selection)
        self.text_file_combo = QComboBox()
        book_layout.addRow("Text File:", self.text_file_combo)
        
        layout.addWidget(book_group)
        
        # Voice Selection Group
        voice_group = QGroupBox("🎤 Voice Selection")
        voice_layout = QFormLayout(voice_group)
        
        self.voice_path_edit = QLineEdit()
        self.voice_path_edit.setPlaceholderText("Select voice sample...")
        voice_browse_btn = QPushButton("Browse...")
        voice_browse_btn.clicked.connect(self.browse_voice_file)
        
        voice_row = QHBoxLayout()
        voice_row.addWidget(self.voice_path_edit)
        voice_row.addWidget(voice_browse_btn)
        voice_layout.addRow("Voice Sample:", voice_row)
        
        layout.addWidget(voice_group)
        
        # VADER Settings Group
        vader_group = QGroupBox("🎭 VADER Sentiment Analysis")
        vader_layout = QVBoxLayout(vader_group)
        
        self.vader_checkbox = QCheckBox("Use VADER sentiment analysis to adjust TTS params per chunk")
        self.vader_checkbox.setChecked(True)
        vader_layout.addWidget(self.vader_checkbox)
        
        vader_info = QLabel("VADER dynamically adjusts TTS parameters based on emotional content of each chunk")
        vader_info.setStyleSheet("color: #666; font-style: italic;")
        vader_layout.addWidget(vader_info)
        
        layout.addWidget(vader_group)
        
        # TTS Parameters Group
        tts_group = QGroupBox("⚙️ TTS Parameters")
        tts_layout = QFormLayout(tts_group)
        
        # Exaggeration
        self.exaggeration_spin = QDoubleSpinBox()
        self.exaggeration_spin.setRange(0.0, 2.0)
        self.exaggeration_spin.setSingleStep(0.1)
        self.exaggeration_spin.setValue(DEFAULT_EXAGGERATION)
        self.exaggeration_spin.setDecimals(2)
        tts_layout.addRow("Exaggeration:", self.exaggeration_spin)
        
        # CFG Weight
        self.cfg_weight_spin = QDoubleSpinBox()
        self.cfg_weight_spin.setRange(0.0, 1.0)
        self.cfg_weight_spin.setSingleStep(0.1)
        self.cfg_weight_spin.setValue(DEFAULT_CFG_WEIGHT)
        self.cfg_weight_spin.setDecimals(2)
        tts_layout.addRow("CFG Weight:", self.cfg_weight_spin)
        
        # Temperature
        self.temperature_spin = QDoubleSpinBox()
        self.temperature_spin.setRange(0.0, 1.0)
        self.temperature_spin.setSingleStep(0.1)
        self.temperature_spin.setValue(DEFAULT_TEMPERATURE)
        self.temperature_spin.setDecimals(2)
        tts_layout.addRow("Temperature:", self.temperature_spin)
        
        layout.addWidget(tts_group)
        
        # Advanced Sampling Group
        sampling_group = QGroupBox("🔬 Advanced Sampling Parameters")
        sampling_layout = QFormLayout(sampling_group)
        
        # Min-P
        self.min_p_spin = QDoubleSpinBox()
        self.min_p_spin.setRange(0.0, 0.5)
        self.min_p_spin.setSingleStep(0.01)
        self.min_p_spin.setValue(0.05)  # DEFAULT_MIN_P
        self.min_p_spin.setDecimals(3)
        sampling_layout.addRow("Min-P (0.0 disables):", self.min_p_spin)
        
        # Top-P
        self.top_p_spin = QDoubleSpinBox()
        self.top_p_spin.setRange(0.5, 1.0)
        self.top_p_spin.setSingleStep(0.1)
        self.top_p_spin.setValue(1.0)  # DEFAULT_TOP_P
        self.top_p_spin.setDecimals(2)
        sampling_layout.addRow("Top-P (1.0 disables):", self.top_p_spin)
        
        # Repetition Penalty
        self.repetition_penalty_spin = QDoubleSpinBox()
        self.repetition_penalty_spin.setRange(1.0, 3.0)
        self.repetition_penalty_spin.setSingleStep(0.1)
        self.repetition_penalty_spin.setValue(1.2)  # DEFAULT_REPETITION_PENALTY
        self.repetition_penalty_spin.setDecimals(1)
        sampling_layout.addRow("Repetition Penalty:", self.repetition_penalty_spin)
        
        layout.addWidget(sampling_group)
        
        # Batch Processing Group
        batch_group = QGroupBox("📦 Batch Processing")
        batch_layout = QVBoxLayout(batch_group)
        
        self.add_to_batch_checkbox = QCheckBox("Add this book to batch queue")
        batch_layout.addWidget(self.add_to_batch_checkbox)
        
        batch_info = QLabel("Enable to queue multiple books for processing")
        batch_info.setStyleSheet("color: #666; font-style: italic;")
        batch_layout.addWidget(batch_info)
        
        layout.addWidget(batch_group)
        
        # Action Buttons
        button_layout = QHBoxLayout()
        
        self.convert_btn = QPushButton("🚀 Start Conversion")
        self.convert_btn.setStyleSheet("QPushButton { background-color: #4CAF50; color: white; font-weight: bold; padding: 10px; }")
        self.convert_btn.clicked.connect(self.start_conversion)
        
        button_layout.addWidget(self.convert_btn)
        button_layout.addStretch()
        
        layout.addLayout(button_layout)
        layout.addStretch()

    def create_resume_tab(self):
        """Tab 2: Resume from specific chunk"""
        tab = QWidget()
        self.tab_widget.addTab(tab, "2. Resume Processing")
        
        layout = QVBoxLayout(tab)
        
        info_label = QLabel("🔄 Resume interrupted book processing from a specific chunk")
        info_label.setStyleSheet("font-weight: bold; color: #2196F3; padding: 10px;")
        layout.addWidget(info_label)
        
        # Incomplete books list
        incomplete_group = QGroupBox("📋 Incomplete Books")
        incomplete_layout = QVBoxLayout(incomplete_group)
        
        self.incomplete_books_list = QListWidget()
        incomplete_layout.addWidget(self.incomplete_books_list)
        
        refresh_btn = QPushButton("🔄 Refresh List")
        refresh_btn.clicked.connect(self.refresh_incomplete_books)
        incomplete_layout.addWidget(refresh_btn)
        
        layout.addWidget(incomplete_group)
        
        # Resume button
        resume_btn = QPushButton("▶️ Resume Selected Book")
        resume_btn.setStyleSheet("QPushButton { background-color: #FF9800; color: white; font-weight: bold; padding: 10px; }")
        resume_btn.clicked.connect(self.resume_processing)
        layout.addWidget(resume_btn)
        
        layout.addStretch()

    def create_combine_tab(self):
        """Tab 3: Combine audio chunks"""
        tab = QWidget()
        self.tab_widget.addTab(tab, "3. Combine Audio")
        
        layout = QVBoxLayout(tab)
        
        info_label = QLabel("🎵 Combine processed audio chunks into final audiobook")
        info_label.setStyleSheet("font-weight: bold; color: #9C27B0; padding: 10px;")
        layout.addWidget(info_label)
        
        # Book selection for combining
        combine_group = QGroupBox("📚 Select Book to Combine")
        combine_layout = QFormLayout(combine_group)
        
        self.combine_book_edit = QLineEdit()
        self.combine_book_edit.setPlaceholderText("Select book folder with audio chunks...")
        combine_browse_btn = QPushButton("Browse...")
        combine_browse_btn.clicked.connect(self.browse_combine_book)
        
        combine_row = QHBoxLayout()
        combine_row.addWidget(self.combine_book_edit)
        combine_row.addWidget(combine_browse_btn)
        combine_layout.addRow("Book Folder:", combine_row)
        
        layout.addWidget(combine_group)
        
        # Combine button
        combine_btn = QPushButton("🔗 Combine Audio Chunks")
        combine_btn.setStyleSheet("QPushButton { background-color: #9C27B0; color: white; font-weight: bold; padding: 10px; }")
        combine_btn.clicked.connect(self.combine_audio)
        layout.addWidget(combine_btn)
        
        layout.addStretch()

    def create_prepare_text_tab(self):
        """Tab 4: Prepare text file for chunking"""
        tab = QWidget()
        self.tab_widget.addTab(tab, "4. Prepare Text")
        
        layout = QVBoxLayout(tab)
        
        info_label = QLabel("📝 Prepare and chunk text files for processing")
        info_label.setStyleSheet("font-weight: bold; color: #607D8B; padding: 10px;")
        layout.addWidget(info_label)
        
        # Text file selection
        prepare_group = QGroupBox("📄 Text File Selection")
        prepare_layout = QFormLayout(prepare_group)
        
        self.prepare_text_edit = QLineEdit()
        self.prepare_text_edit.setPlaceholderText("Select text file to prepare...")
        prepare_browse_btn = QPushButton("Browse...")
        prepare_browse_btn.clicked.connect(self.browse_prepare_text)
        
        prepare_row = QHBoxLayout()
        prepare_row.addWidget(self.prepare_text_edit)
        prepare_row.addWidget(prepare_browse_btn)
        prepare_layout.addRow("Text File:", prepare_row)
        
        layout.addWidget(prepare_group)
        
        # Prepare button
        prepare_btn = QPushButton("📝 Prepare Text for Chunking")
        prepare_btn.setStyleSheet("QPushButton { background-color: #607D8B; color: white; font-weight: bold; padding: 10px; }")
        prepare_btn.clicked.connect(self.prepare_text)
        layout.addWidget(prepare_btn)
        
        layout.addStretch()

    def create_test_chunking_tab(self):
        """Tab 5: Test chunking logic"""
        tab = QWidget()
        self.tab_widget.addTab(tab, "5. Test Chunking")
        
        layout = QVBoxLayout(tab)
        
        info_label = QLabel("🧪 Test and verify text chunking logic")
        info_label.setStyleSheet("font-weight: bold; color: #FF5722; padding: 10px;")
        layout.addWidget(info_label)
        
        # Test parameters
        test_group = QGroupBox("⚙️ Chunking Parameters")
        test_layout = QFormLayout(test_group)
        
        self.test_text_edit = QTextEdit()
        self.test_text_edit.setPlaceholderText("Enter test text (or leave blank for default)...")
        self.test_text_edit.setMaximumHeight(100)
        test_layout.addRow("Test Text:", self.test_text_edit)
        
        self.max_words_spin = QSpinBox()
        self.max_words_spin.setRange(1, 200)
        self.max_words_spin.setValue(30)
        test_layout.addRow("Max Words per Chunk:", self.max_words_spin)
        
        self.min_words_spin = QSpinBox()
        self.min_words_spin.setRange(1, 50)
        self.min_words_spin.setValue(4)
        test_layout.addRow("Min Words per Chunk:", self.min_words_spin)
        
        layout.addWidget(test_group)
        
        # Test button
        test_btn = QPushButton("🧪 Run Chunking Test")
        test_btn.setStyleSheet("QPushButton { background-color: #FF5722; color: white; font-weight: bold; padding: 10px; }")
        test_btn.clicked.connect(self.test_chunking)
        layout.addWidget(test_btn)
        
        layout.addStretch()

    def create_repair_tool_tab(self):
        """Tab 6: Chunk repair tool"""
        tab = QWidget()
        self.tab_widget.addTab(tab, "6. Repair Tool")
        
        layout = QVBoxLayout(tab)
        
        info_label = QLabel("🔧 Launch chunk repair and revision tool")
        info_label.setStyleSheet("font-weight: bold; color: #795548; padding: 10px;")
        layout.addWidget(info_label)
        
        description = QLabel("The repair tool allows you to:\n• Fix corrupted audio chunks\n• Regenerate specific chunks\n• Adjust chunk boundaries\n• Review and edit chunk content")
        description.setStyleSheet("color: #666; padding: 20px;")
        layout.addWidget(description)
        
        # Launch button
        repair_btn = QPushButton("🔧 Launch Chunk Repair Tool")
        repair_btn.setStyleSheet("QPushButton { background-color: #795548; color: white; font-weight: bold; padding: 10px; }")
        repair_btn.clicked.connect(self.launch_repair_tool)
        layout.addWidget(repair_btn)
        
        layout.addStretch()

    def create_json_generate_tab(self):
        """Tab 7: Generate from JSON"""
        tab = QWidget()
        self.tab_widget.addTab(tab, "7. Generate from JSON")
        
        layout = QVBoxLayout(tab)
        
        info_label = QLabel("📄 Generate audio from edited JSON files")
        info_label.setStyleSheet("font-weight: bold; color: #E91E63; padding: 10px;")
        layout.addWidget(info_label)
        
        # JSON file selection
        json_group = QGroupBox("📄 JSON File Selection")
        json_layout = QFormLayout(json_group)
        
        self.json_file_edit = QLineEdit()
        self.json_file_edit.setPlaceholderText("Select JSON file...")
        json_browse_btn = QPushButton("Browse...")
        json_browse_btn.clicked.connect(self.browse_json_file)
        
        json_row = QHBoxLayout()
        json_row.addWidget(self.json_file_edit)
        json_row.addWidget(json_browse_btn)
        json_layout.addRow("JSON File:", json_row)
        
        layout.addWidget(json_group)
        
        # Generate button
        json_btn = QPushButton("🎵 Generate Audio from JSON")
        json_btn.setStyleSheet("QPushButton { background-color: #E91E63; color: white; font-weight: bold; padding: 10px; }")
        json_btn.clicked.connect(self.generate_from_json)
        layout.addWidget(json_btn)
        
        layout.addStretch()

    def create_output_area(self, layout):
        """Create output/log area at bottom"""
        output_group = QGroupBox("📝 Output Log")
        output_layout = QVBoxLayout(output_group)
        
        self.output_text = QTextEdit()
        self.output_text.setMaximumHeight(200)
        self.output_text.setStyleSheet("font-family: monospace; background-color: #f5f5f5;")
        output_layout.addWidget(self.output_text)
        
        # Clear button
        clear_btn = QPushButton("Clear Log")
        clear_btn.clicked.connect(self.output_text.clear)
        output_layout.addWidget(clear_btn)
        
        layout.addWidget(output_group)

    # Browse Methods
    def browse_book_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Book Folder")
        if folder:
            self.book_path_edit.setText(folder)
            self.populate_text_files(folder)

    def populate_text_files(self, folder_path):
        """Populate text file combo box when book folder is selected"""
        self.text_file_combo.clear()
        folder = Path(folder_path)
        txt_files = list(folder.glob("*.txt"))
        for txt_file in txt_files:
            self.text_file_combo.addItem(txt_file.name, str(txt_file))

    def browse_voice_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Voice Sample", "", 
            "Audio Files (*.wav *.mp3 *.flac *.m4a);;All Files (*)"
        )
        if file_path:
            self.voice_path_edit.setText(file_path)

    def browse_combine_book(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Book Folder to Combine")
        if folder:
            self.combine_book_edit.setText(folder)

    def browse_prepare_text(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Text File to Prepare", "", 
            "Text Files (*.txt);;All Files (*)"
        )
        if file_path:
            self.prepare_text_edit.setText(file_path)

    def browse_json_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select JSON File", "", 
            "JSON Files (*.json);;All Files (*)"
        )
        if file_path:
            self.json_file_edit.setText(file_path)

    # Action Methods
    def start_conversion(self):
        """Start book conversion process"""
        # Validate inputs
        if not self.book_path_edit.text():
            QMessageBox.warning(self, "Error", "Please select a book folder")
            return
        
        if not self.voice_path_edit.text():
            QMessageBox.warning(self, "Error", "Please select a voice sample")
            return
        
        if self.text_file_combo.currentData() is None:
            QMessageBox.warning(self, "Error", "Please select a text file")
            return
        
        # Collect parameters
        book_path = Path(self.book_path_edit.text())
        voice_path = Path(self.voice_path_edit.text())
        text_file_path = Path(self.text_file_combo.currentData())
        use_vader = self.vader_checkbox.isChecked()
        
        tts_params = {
            'exaggeration': self.exaggeration_spin.value(),
            'cfg_weight': self.cfg_weight_spin.value(),
            'temperature': self.temperature_spin.value(),
            'min_p': self.min_p_spin.value(),
            'top_p': self.top_p_spin.value(),
            'repetition_penalty': self.repetition_penalty_spin.value(),
            'use_vader': use_vader
        }
        
        self.log_output(f"Starting conversion for: {book_path.name}")
        self.log_output(f"Voice: {voice_path.name}")
        self.log_output(f"Text file: {text_file_path.name}")
        self.log_output(f"VADER enabled: {use_vader}")
        self.log_output(f"TTS params: {tts_params}")
        
        # Disable the button during processing
        self.convert_btn.setEnabled(False)
        self.convert_btn.setText("🔄 Processing...")
        
        # Start processing in background thread
        self.process_thread = ProcessThread(
            self.run_book_conversion, 
            book_path, text_file_path, voice_path, tts_params
        )
        self.process_thread.output_signal.connect(self.log_output)
        self.process_thread.finished_signal.connect(self.on_conversion_finished)
        self.process_thread.start()

    def refresh_incomplete_books(self):
        """Refresh list of incomplete books"""
        self.incomplete_books_list.clear()
        try:
            incomplete_books = find_incomplete_books()
            for book in incomplete_books:
                self.incomplete_books_list.addItem(str(book))
            self.log_output(f"Found {len(incomplete_books)} incomplete books")
        except Exception as e:
            self.log_output(f"Error finding incomplete books: {e}")

    def resume_processing(self):
        """Resume processing selected book"""
        current_item = self.incomplete_books_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "Error", "Please select a book to resume")
            return
        
        book_path = current_item.text()
        self.log_output(f"Resuming processing for: {book_path}")
        
        try:
            from modules.resume_handler import resume_book_from_chunk
            # Start resume in background
            self.process_thread = ProcessThread(resume_book_from_chunk, 0)
            self.process_thread.output_signal.connect(self.log_output)
            self.process_thread.finished_signal.connect(lambda s, m: self.log_output("Resume completed" if s else f"Resume failed: {m}"))
            self.process_thread.start()
        except Exception as e:
            self.log_output(f"Error starting resume: {e}")

    def combine_audio(self):
        """Combine audio chunks"""
        if not self.combine_book_edit.text():
            QMessageBox.warning(self, "Error", "Please select a book folder")
            return
        
        book_path = self.combine_book_edit.text()
        self.log_output(f"Combining audio for: {Path(book_path).name}")
        
        try:
            # Start combine in background
            self.process_thread = ProcessThread(run_combine_only_mode)
            self.process_thread.output_signal.connect(self.log_output)
            self.process_thread.finished_signal.connect(lambda s, m: self.log_output("Combine completed" if s else f"Combine failed: {m}"))
            self.process_thread.start()
        except Exception as e:
            self.log_output(f"Error starting combine: {e}")

    def prepare_text(self):
        """Prepare text for chunking"""
        if not self.prepare_text_edit.text():
            QMessageBox.warning(self, "Error", "Please select a text file")
            return
        
        text_path = self.prepare_text_edit.text()
        self.log_output(f"Preparing text: {Path(text_path).name}")
        # TODO: Integrate with text preparation functionality
        QMessageBox.information(self, "Started", "Text preparation started - check output log")

    def test_chunking(self):
        """Test chunking logic"""
        test_text = self.test_text_edit.toPlainText().strip()
        max_words = self.max_words_spin.value()
        min_words = self.min_words_spin.value()
        
        self.log_output(f"Testing chunking - Max: {max_words}, Min: {min_words}")
        if test_text:
            self.log_output(f"Custom text: {test_text[:50]}...")
        else:
            self.log_output("Using default test text")
        
        try:
            from modules.text_processor import test_chunking
            # Run test in background
            self.process_thread = ProcessThread(
                test_chunking, 
                test_text if test_text else None, 
                max_words, 
                min_words
            )
            self.process_thread.output_signal.connect(self.log_output)
            self.process_thread.finished_signal.connect(lambda s, m: self.log_output("Test completed" if s else f"Test failed: {m}"))
            self.process_thread.start()
        except Exception as e:
            self.log_output(f"Error running test: {e}")

    def launch_repair_tool(self):
        """Launch chunk repair tool"""
        self.log_output("Launching chunk repair tool...")
        # TODO: Integrate with repair tool functionality
        QMessageBox.information(self, "Started", "Repair tool launched - check output log")

    def generate_from_json(self):
        """Generate audio from JSON"""
        if not self.json_file_edit.text():
            QMessageBox.warning(self, "Error", "Please select a JSON file")
            return
        
        json_path = self.json_file_edit.text()
        self.log_output(f"Generating audio from: {Path(json_path).name}")
        # TODO: Integrate with JSON generation functionality
        QMessageBox.information(self, "Started", "JSON generation started - check output log")

    def run_book_conversion(self, book_path, text_file_path, voice_path, tts_params):
        """Run the actual book conversion process"""
        from modules.batch_processor import pipeline_book_processing
        from interface import ensure_voice_sample_compatibility
        
        try:
            # Ensure voice compatibility 
            compatible_voice = ensure_voice_sample_compatibility(voice_path)
            
            # Create book config matching the interface.py format
            book_config = {
                'book_dir': book_path,
                'voice_path': compatible_voice,
                'tts_params': tts_params
            }
            
            # Run the processing pipeline
            result = pipeline_book_processing([book_config])
            
            return result
            
        except Exception as e:
            raise Exception(f"Conversion failed: {str(e)}")

    def on_conversion_finished(self, success, message):
        """Handle conversion completion"""
        # Re-enable the button
        self.convert_btn.setEnabled(True)
        self.convert_btn.setText("🚀 Start Conversion")
        
        if success:
            self.log_output("✅ Conversion completed successfully!")
            QMessageBox.information(self, "Success", "Book conversion completed successfully!")
        else:
            self.log_output(f"❌ Conversion failed: {message}")
            QMessageBox.critical(self, "Error", f"Conversion failed:\n{message}")

    def log_output(self, message):
        """Add message to output log"""
        from datetime import datetime
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.output_text.append(f"[{timestamp}] {message}")
        self.output_text.ensureCursorVisible()


def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Modern look
    
    window = ChatterboxMainWindow()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()