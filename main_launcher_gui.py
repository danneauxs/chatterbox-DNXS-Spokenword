#!/usr/bin/env python3
"""
GenTTS GUI Launcher
PyQt5 GUI for the ChatterboxTTS audiobook generation system
"""

import sys
import os
import logging
from pathlib import Path
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QGridLayout,
    QWidget, QPushButton, QLabel, QListWidget, QTextEdit, QSpinBox,
    QDoubleSpinBox, QCheckBox, QComboBox, QProgressBar, QMessageBox,
    QFileDialog, QGroupBox, QFrame, QScrollArea, QSplitter, QInputDialog
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt5.QtGui import QFont, QPixmap, QIcon

# Import the original functions with individual error handling
MODULES_AVAILABLE = {
    'text_processor': False,
    'vaderSentiment': False, 
    'chunk_loader': False,
    'chunk_tool': False,
    'resume_handler': False,
    'combine_only': False,
    'interface': False,
    'config': False,
    'tts_engine': False
}

# Try importing each module individually
try:
    from modules.text_processor import sentence_chunk_text, smart_punctuate, test_chunking, detect_content_boundaries
    MODULES_AVAILABLE['text_processor'] = True
except ImportError:
    print("Warning: text_processor module not available")

try:
    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
    MODULES_AVAILABLE['vaderSentiment'] = True
except ImportError:
    print("Note: vaderSentiment not available (sentiment analysis disabled)")

try:
    from wrapper.chunk_loader import save_chunks, load_chunks
    MODULES_AVAILABLE['chunk_loader'] = True
except ImportError:
    print("Warning: chunk_loader module not available")

try:
    from wrapper.chunk_tool import run_chunk_repair_tool
    MODULES_AVAILABLE['chunk_tool'] = True
except ImportError:
    print("Warning: chunk_tool module not available")

try:
    from modules.resume_handler import resume_book_from_chunk, find_incomplete_books
    MODULES_AVAILABLE['resume_handler'] = True
except ImportError:
    print("Warning: resume_handler module not available")

try:
    from tools.combine_only import run_combine_only_mode
    MODULES_AVAILABLE['combine_only'] = True
except ImportError:
    print("Warning: combine_only module not available")

try:
    from interface import main
    MODULES_AVAILABLE['interface'] = True
except ImportError:
    print("Warning: main interface module not available")

try:
    from config.config import *
    MODULES_AVAILABLE['config'] = True
except ImportError:
    print("Warning: config module not available - using defaults")
    # Define some defaults
    TEXT_INPUT_ROOT = "Text_Input"
    AUDIOBOOK_ROOT = Path("Audiobook")
    DEFAULT_EXAGGERATION = 1.0
    DEFAULT_CFG_WEIGHT = 5.0
    DEFAULT_TEMPERATURE = 0.7

try:
    from modules.tts_engine import generate_enriched_chunks
    MODULES_AVAILABLE['tts_engine'] = True
except ImportError:
    print("Warning: tts_engine module not available")


class TaskThread(QThread):
    """Background thread for running tasks without blocking the GUI."""
    finished = pyqtSignal(bool, str)  # success, message
    progress = pyqtSignal(str)  # status message
    
    def __init__(self, task_func, *args, **kwargs):
        super().__init__()
        self.task_func = task_func
        self.args = args
        self.kwargs = kwargs
    
    def run(self):
        try:
            result = self.task_func(*self.args, **self.kwargs)
            self.finished.emit(True, "Task completed successfully")
        except Exception as e:
            self.finished.emit(False, f"Task failed: {str(e)}")


class BookSelectionWidget(QWidget):
    """Widget for selecting books and text files."""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.refresh_books()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Title
        title = QLabel("📚 Select Book")
        title.setFont(QFont("Arial", 12, QFont.Bold))
        layout.addWidget(title)
        
        # Book list
        self.book_list = QListWidget()
        self.book_list.currentItemChanged.connect(self.on_book_selected)
        layout.addWidget(self.book_list)
        
        # Text file list
        file_label = QLabel("📄 Text Files:")
        layout.addWidget(file_label)
        
        self.file_list = QListWidget()
        layout.addWidget(self.file_list)
        
        # Refresh button
        refresh_btn = QPushButton("🔄 Refresh")
        refresh_btn.clicked.connect(self.refresh_books)
        layout.addWidget(refresh_btn)
    
    def refresh_books(self):
        """Refresh the list of available books."""
        self.book_list.clear()
        self.file_list.clear()
        
        try:
            text_input_dir = Path("Text_Input")
            if text_input_dir.exists():
                book_dirs = [d for d in text_input_dir.iterdir() if d.is_dir()]
                for book_dir in book_dirs:
                    txt_files = list(book_dir.glob("*.txt"))
                    item_text = f"{book_dir.name} ({len(txt_files)} files)"
                    self.book_list.addItem(item_text)
        except Exception as e:
            print(f"Error refreshing books: {e}")
    
    def on_book_selected(self, current, previous):
        """Handle book selection."""
        self.file_list.clear()
        
        if current:
            book_name = current.text().split(" (")[0]  # Extract book name
            try:
                book_dir = Path("Text_Input") / book_name
                txt_files = list(book_dir.glob("*.txt"))
                for txt_file in txt_files:
                    self.file_list.addItem(txt_file.name)
            except Exception as e:
                print(f"Error loading files for {book_name}: {e}")
    
    def get_selected_book_and_file(self):
        """Get the currently selected book and file."""
        current_book = self.book_list.currentItem()
        current_file = self.file_list.currentItem()
        
        if not current_book or not current_file:
            return None, None
        
        book_name = current_book.text().split(" (")[0]
        file_name = current_file.text()
        
        return book_name, file_name


class TTSParametersWidget(QWidget):
    """Widget for TTS parameter configuration."""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Title
        title = QLabel("⚙️ TTS Parameters")
        title.setFont(QFont("Arial", 12, QFont.Bold))
        layout.addWidget(title)
        
        # Parameter controls
        params_group = QGroupBox("Parameters")
        params_layout = QGridLayout(params_group)
        
        # Exaggeration
        params_layout.addWidget(QLabel("Exaggeration:"), 0, 0)
        self.exaggeration_spin = QDoubleSpinBox()
        self.exaggeration_spin.setRange(0.0, 2.0)
        self.exaggeration_spin.setSingleStep(0.1)
        self.exaggeration_spin.setValue(1.0)
        params_layout.addWidget(self.exaggeration_spin, 0, 1)
        
        # CFG Weight
        params_layout.addWidget(QLabel("CFG Weight:"), 1, 0)
        self.cfg_weight_spin = QDoubleSpinBox()
        self.cfg_weight_spin.setRange(0.0, 10.0)
        self.cfg_weight_spin.setSingleStep(0.1)
        self.cfg_weight_spin.setValue(5.0)
        params_layout.addWidget(self.cfg_weight_spin, 1, 1)
        
        # Temperature
        params_layout.addWidget(QLabel("Temperature:"), 2, 0)
        self.temperature_spin = QDoubleSpinBox()
        self.temperature_spin.setRange(0.0, 2.0)
        self.temperature_spin.setSingleStep(0.1)
        self.temperature_spin.setValue(0.7)
        params_layout.addWidget(self.temperature_spin, 2, 1)
        
        # VADER sentiment analysis
        self.use_vader_cb = QCheckBox("🎭 Use VADER sentiment analysis")
        self.use_vader_cb.setChecked(True)
        params_layout.addWidget(self.use_vader_cb, 3, 0, 1, 2)
        
        layout.addWidget(params_group)
        
        # Chunking parameters
        chunk_group = QGroupBox("Chunking Parameters")
        chunk_layout = QGridLayout(chunk_group)
        
        chunk_layout.addWidget(QLabel("Max words per chunk:"), 0, 0)
        self.max_words_spin = QSpinBox()
        self.max_words_spin.setRange(10, 100)
        self.max_words_spin.setValue(30)
        chunk_layout.addWidget(self.max_words_spin, 0, 1)
        
        chunk_layout.addWidget(QLabel("Min words per chunk:"), 1, 0)
        self.min_words_spin = QSpinBox()
        self.min_words_spin.setRange(1, 20)
        self.min_words_spin.setValue(4)
        chunk_layout.addWidget(self.min_words_spin, 1, 1)
        
        layout.addWidget(chunk_group)
    
    def get_tts_parameters(self):
        """Get the current TTS parameters."""
        return {
            'exaggeration': self.exaggeration_spin.value(),
            'cfg_weight': self.cfg_weight_spin.value(),
            'temperature': self.temperature_spin.value(),
            'use_vader': self.use_vader_cb.isChecked()
        }
    
    def get_chunking_parameters(self):
        """Get the current chunking parameters."""
        return {
            'max_words': self.max_words_spin.value(),
            'min_words': self.min_words_spin.value()
        }


class MainLauncherGUI(QMainWindow):
    """Main GUI window for the ChatterboxTTS launcher."""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.current_task_thread = None
    
    def init_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle("ChatterboxTTS - Audiobook Generator")
        self.setGeometry(100, 100, 1200, 800)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QHBoxLayout(central_widget)
        
        # Left panel - Controls
        left_panel = QWidget()
        left_panel.setMaximumWidth(400)
        left_layout = QVBoxLayout(left_panel)
        
        # Title
        title = QLabel("🎙️ ChatterboxTTS Launcher")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        left_layout.addWidget(title)
        
        # Action buttons
        actions_group = QGroupBox("Actions")
        actions_layout = QVBoxLayout(actions_group)
        
        # Primary actions
        self.convert_btn = QPushButton("🎵 Convert Book to Audiobook")
        self.convert_btn.clicked.connect(self.convert_book)
        self.convert_btn.setStyleSheet("QPushButton { background-color: #4CAF50; color: white; font-weight: bold; padding: 10px; }")
        self.convert_btn.setEnabled(MODULES_AVAILABLE['interface'])
        if not MODULES_AVAILABLE['interface']:
            self.convert_btn.setToolTip("Interface module not available")
        actions_layout.addWidget(self.convert_btn)
        
        self.prepare_btn = QPushButton("📝 Prepare Text for Chunking")
        self.prepare_btn.clicked.connect(self.prepare_chunks)
        self.prepare_btn.setEnabled(MODULES_AVAILABLE['tts_engine'])
        if not MODULES_AVAILABLE['tts_engine']:
            self.prepare_btn.setToolTip("TTS engine module not available")
        actions_layout.addWidget(self.prepare_btn)
        
        self.resume_btn = QPushButton("▶️ Resume from Chunk")
        self.resume_btn.clicked.connect(self.resume_book)
        self.resume_btn.setEnabled(MODULES_AVAILABLE['resume_handler'])
        if not MODULES_AVAILABLE['resume_handler']:
            self.resume_btn.setToolTip("Resume handler module not available")
        actions_layout.addWidget(self.resume_btn)
        
        self.combine_btn = QPushButton("🔗 Combine Audio Chunks")
        self.combine_btn.clicked.connect(self.combine_audio)
        self.combine_btn.setEnabled(MODULES_AVAILABLE['combine_only'])
        if not MODULES_AVAILABLE['combine_only']:
            self.combine_btn.setToolTip("Combine module not available")
        actions_layout.addWidget(self.combine_btn)
        
        # Tools
        tools_frame = QFrame()
        tools_layout = QVBoxLayout(tools_frame)
        
        self.repair_btn = QPushButton("🔧 Launch Chunk Repair Tool")
        self.repair_btn.clicked.connect(self.launch_repair_tool)
        self.repair_btn.setEnabled(MODULES_AVAILABLE['chunk_tool'])
        if not MODULES_AVAILABLE['chunk_tool']:
            self.repair_btn.setToolTip("Chunk tool module not available")
        tools_layout.addWidget(self.repair_btn)
        
        self.test_btn = QPushButton("🧪 Test Chunking Logic")
        self.test_btn.clicked.connect(self.test_chunking)
        self.test_btn.setEnabled(MODULES_AVAILABLE['text_processor'])
        if not MODULES_AVAILABLE['text_processor']:
            self.test_btn.setToolTip("Text processor module not available")
        tools_layout.addWidget(self.test_btn)
        
        self.generate_btn = QPushButton("⚡ Generate from JSON")
        self.generate_btn.clicked.connect(self.generate_from_json)
        # This will be enabled if the utils module exists
        tools_layout.addWidget(self.generate_btn)
        
        actions_layout.addWidget(tools_frame)
        left_layout.addWidget(actions_group)
        
        # Book selection
        self.book_selector = BookSelectionWidget()
        left_layout.addWidget(self.book_selector)
        
        # TTS parameters
        self.tts_params = TTSParametersWidget()
        left_layout.addWidget(self.tts_params)
        
        left_layout.addStretch()
        
        # Right panel - Output and status
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        
        # Status area
        status_group = QGroupBox("Status")
        status_layout = QVBoxLayout(status_group)
        
        self.status_label = QLabel("Ready")
        self.status_label.setFont(QFont("Arial", 10, QFont.Bold))
        status_layout.addWidget(self.status_label)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        status_layout.addWidget(self.progress_bar)
        
        right_layout.addWidget(status_group)
        
        # Output log
        log_group = QGroupBox("Output Log")
        log_layout = QVBoxLayout(log_group)
        
        self.log_text = QTextEdit()
        self.log_text.setFont(QFont("Consolas", 9))
        self.log_text.setReadOnly(True)
        log_layout.addWidget(self.log_text)
        
        # Clear log button
        clear_btn = QPushButton("🗑️ Clear Log")
        clear_btn.clicked.connect(self.clear_log)
        log_layout.addWidget(clear_btn)
        
        right_layout.addWidget(log_group)
        
        # Add panels to main layout
        main_layout.addWidget(left_panel)
        main_layout.addWidget(right_panel, 1)  # Give right panel more space
        
        # Status bar
        self.statusBar().showMessage("Ready to process audiobooks")
        
        # Initial log message
        self.log("🎙️ ChatterboxTTS GUI Launcher started")
        self.log_module_status()
        self.log("Select a book and choose an action to begin")
    
    def log_module_status(self):
        """Log the status of available modules."""
        self.log("📦 Module Status:")
        for module, available in MODULES_AVAILABLE.items():
            status = "✅" if available else "❌"
            self.log(f"  {status} {module}")
        
        unavailable_count = sum(1 for available in MODULES_AVAILABLE.values() if not available)
        if unavailable_count > 0:
            self.log(f"⚠️ {unavailable_count} modules unavailable - some features disabled")
            if not MODULES_AVAILABLE['vaderSentiment']:
                self.log("💡 To enable sentiment analysis: pip install vaderSentiment")
        else:
            self.log("✅ All modules available!")
    
    def log(self, message):
        """Add a message to the log."""
        import datetime
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        self.log_text.append(f"[{timestamp}] {message}")
        self.log_text.ensureCursorVisible()
    
    def clear_log(self):
        """Clear the log."""
        self.log_text.clear()
    
    def update_status(self, message):
        """Update the status label and status bar."""
        self.status_label.setText(message)
        self.statusBar().showMessage(message)
        self.log(f"Status: {message}")
    
    def show_progress(self, show=True):
        """Show or hide the progress bar."""
        self.progress_bar.setVisible(show)
        if show:
            self.progress_bar.setRange(0, 0)  # Indeterminate progress
    
    def convert_book(self):
        """Convert a book to audiobook."""
        if not MODULES_AVAILABLE['interface']:
            QMessageBox.warning(self, "Module Not Available", 
                "The main interface module is not available.\n"
                "Please ensure the virtual environment is properly set up.")
            return
            
        book_name, file_name = self.book_selector.get_selected_book_and_file()
        
        if not book_name or not file_name:
            QMessageBox.warning(self, "No Selection", "Please select a book and text file first.")
            return
        
        self.update_status(f"Converting {book_name} - {file_name}...")
        self.show_progress(True)
        
        try:
            self.current_task_thread = TaskThread(main)
            self.current_task_thread.finished.connect(self.on_task_finished)
            self.current_task_thread.start()
            
        except Exception as e:
            self.show_progress(False)
            self.update_status("Error starting conversion")
            QMessageBox.critical(self, "Error", f"Failed to start conversion:\n{str(e)}")
    
    def prepare_chunks(self):
        """Prepare text file for chunking."""
        book_name, file_name = self.book_selector.get_selected_book_and_file()
        
        if not book_name or not file_name:
            QMessageBox.warning(self, "No Selection", "Please select a book and text file first.")
            return
        
        self.update_status(f"Preparing chunks for {book_name} - {file_name}...")
        self.show_progress(True)
        
        try:
            # Get parameters
            tts_params = self.tts_params.get_tts_parameters()
            
            # Process the file
            text_file_path = Path("Text_Input") / book_name / file_name
            text_output_dir = Path("Audiobook") / book_name / "TTS" / "text_chunks"
            text_output_dir.mkdir(parents=True, exist_ok=True)
            
            # Run in background thread
            self.current_task_thread = TaskThread(
                generate_enriched_chunks, 
                text_file_path, 
                text_output_dir, 
                tts_params
            )
            self.current_task_thread.finished.connect(self.on_task_finished)
            self.current_task_thread.start()
            
        except Exception as e:
            self.show_progress(False)
            self.update_status("Error preparing chunks")
            QMessageBox.critical(self, "Error", f"Failed to prepare chunks:\n{str(e)}")
    
    def resume_book(self):
        """Resume book processing from a specific chunk."""
        self.update_status("Launching resume interface...")
        
        try:
            # Show input dialog for chunk number
            chunk_num, ok = QInputDialog.getInt(
                self, "Resume from Chunk", 
                "Enter chunk number to resume from:", 
                1, 1, 9999, 1
            )
            
            if ok:
                self.show_progress(True)
                self.current_task_thread = TaskThread(resume_book_from_chunk, chunk_num)
                self.current_task_thread.finished.connect(self.on_task_finished)
                self.current_task_thread.start()
                
        except Exception as e:
            self.update_status("Error starting resume")
            QMessageBox.critical(self, "Error", f"Failed to start resume:\n{str(e)}")
    
    def combine_audio(self):
        """Combine audio chunks into final audiobook."""
        self.update_status("Combining audio chunks...")
        self.show_progress(True)
        
        try:
            self.current_task_thread = TaskThread(run_combine_only_mode)
            self.current_task_thread.finished.connect(self.on_task_finished)
            self.current_task_thread.start()
            
        except Exception as e:
            self.show_progress(False)
            self.update_status("Error combining audio")
            QMessageBox.critical(self, "Error", f"Failed to combine audio:\n{str(e)}")
    
    def launch_repair_tool(self):
        """Launch the chunk repair tool."""
        self.update_status("Launching chunk repair tool...")
        
        try:
            # Run repair tool (this might open a separate window)
            run_chunk_repair_tool()
            self.update_status("Chunk repair tool launched")
            
        except Exception as e:
            self.update_status("Error launching repair tool")
            QMessageBox.critical(self, "Error", f"Failed to launch repair tool:\n{str(e)}")
    
    def test_chunking(self):
        """Test the chunking logic."""
        # Get test parameters
        chunk_params = self.tts_params.get_chunking_parameters()
        
        # Show input dialog for test text
        test_text, ok = QInputDialog.getMultiLineText(
            self, "Test Chunking", 
            "Enter test text (or leave empty for default):"
        )
        
        if ok:
            try:
                self.update_status("Testing chunking logic...")
                
                # Run test chunking
                test_chunking(
                    test_text if test_text.strip() else None,
                    chunk_params['max_words'],
                    chunk_params['min_words']
                )
                
                self.update_status("Chunking test completed")
                
            except Exception as e:
                self.update_status("Error testing chunking")
                QMessageBox.critical(self, "Error", f"Failed to test chunking:\n{str(e)}")
    
    def generate_from_json(self):
        """Generate audio from edited JSON."""
        self.update_status("Generating from JSON...")
        self.show_progress(True)
        
        try:
            from utils.generate_from_json import main as generate_main
            self.current_task_thread = TaskThread(generate_main)
            self.current_task_thread.finished.connect(self.on_task_finished)
            self.current_task_thread.start()
            
        except Exception as e:
            self.show_progress(False)
            self.update_status("Error generating from JSON")
            QMessageBox.critical(self, "Error", f"Failed to generate from JSON:\n{str(e)}")
    
    def on_task_finished(self, success, message):
        """Handle task completion."""
        self.show_progress(False)
        
        if success:
            self.update_status("Task completed successfully")
            QMessageBox.information(self, "Success", message)
        else:
            self.update_status("Task failed")
            QMessageBox.critical(self, "Error", message)
        
        self.current_task_thread = None


def main():
    """Main entry point for the GUI application."""
    app = QApplication(sys.argv)
    app.setApplicationName("ChatterboxTTS Launcher")
    app.setApplicationVersion("1.0")
    
    # Set application style
    app.setStyle('Fusion')
    
    # Create and show main window
    main_window = MainLauncherGUI()
    main_window.show()
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()