# Code Cross-References

## Voice_Samples.mel:<module>
- calls: main
## Voice_Samples.mel:main
- calls: append
- calls: endswith
- calls: enumerate
- calls: exists
- calls: exit
- calls: export
- calls: from_mp3
- calls: input
- calls: int
- calls: len
- calls: listdir
- calls: lower
- calls: print
- calls: process_audio_file
- calls: remove
- calls: splitext
## Voice_Samples.mel:process_audio_file
- calls: len
- calls: load
- calls: print
- calls: splitext
- calls: write
## chatterbox_gui:<module>
- calls: globals
- calls: isinstance
- calls: main
- calls: print
## chatterbox_gui:ChatterboxMainWindow.__init__
- calls: QScrollArea
- calls: QSettings
- calls: QSplitter
- calls: QTabWidget
- calls: QVBoxLayout
- calls: QWidget
- calls: __init__
- calls: addWidget
- calls: connect
- calls: create_audio_output_analyzer_tab
- calls: create_combine_tab
- calls: create_config_tab
- calls: create_convert_book_tab
- calls: create_json_generate_tab
- calls: create_output_area_widget
- calls: create_prepare_text_tab
- calls: create_repair_tool_tab
- calls: create_resume_tab
- calls: create_test_chunking_tab
- calls: create_voice_analyzer_tab
- calls: init_token_logging
- calls: setCentralWidget
- calls: setCollapsible
- calls: setContentsMargins
- calls: setGeometry
- calls: setHorizontalScrollBarPolicy
- calls: setSizes
- calls: setVerticalScrollBarPolicy
- calls: setWidget
- calls: setWidgetResizable
- calls: setWindowTitle
- calls: showMessage
- calls: statusBar
- calls: super
- calls: test_audio_system_startup
## chatterbox_gui:ChatterboxMainWindow._attach_config_key
- calls: setProperty
## chatterbox_gui:ChatterboxMainWindow._attach_spin_reset
- calls: _show_spin_context_menu
- calls: connect
- calls: setContextMenuPolicy
- calls: setProperty
## chatterbox_gui:ChatterboxMainWindow._build_effective_settings
- calls: _read_widget_value
- calls: findChildren
- calls: get
- calls: hasattr
- calls: property
## chatterbox_gui:ChatterboxMainWindow._check_voice_playback
- calls: _reset_voice_buttons
- calls: get_busy
- calls: hasattr
- calls: print
## chatterbox_gui:ChatterboxMainWindow._generate_audiobook_from_json
- calls: generate_audiobook_from_json
- calls: print
## chatterbox_gui:ChatterboxMainWindow._handle_token_overruns
- calls: QMessageBox
- calls: QPushButton
- calls: addButton
- calls: clickedButton
- calls: exec_
- calls: join
- calls: len
- calls: log_output
- calls: setCurrentIndex
- calls: setIcon
- calls: setText
- calls: setWindowTitle
## chatterbox_gui:ChatterboxMainWindow._process_text_file
- calls: _build_effective_settings
- calls: currentText
- calls: generate_enriched_chunks
- calls: isChecked
- calls: len
- calls: mkdir
- calls: print
- calls: value
## chatterbox_gui:ChatterboxMainWindow._read_widget_value
- calls: bool
- calls: currentText
- calls: float
- calls: int
- calls: isChecked
- calls: isdigit
- calls: isinstance
- calls: strip
- calls: value
## chatterbox_gui:ChatterboxMainWindow._reset_spin_from_saved
- calls: blockSignals
- calls: float
- calls: getattr
- calls: hasattr
- calls: int
- calls: isinstance
- calls: max
- calls: maximum
- calls: min
- calls: minimum
- calls: property
- calls: reload
- calls: setValue
- calls: showMessage
- calls: statusBar
## chatterbox_gui:ChatterboxMainWindow._reset_voice_buttons
- calls: hasattr
- calls: setEnabled
- calls: stop
## chatterbox_gui:ChatterboxMainWindow._show_spin_context_menu
- calls: QMenu
- calls: _reset_spin_from_saved
- calls: addAction
- calls: connect
- calls: exec_
- calls: mapToGlobal
## chatterbox_gui:ChatterboxMainWindow.accept_chunk_revision
- calls: accept_revision
- calls: critical
- calls: exists
- calls: hasattr
- calls: information
- calls: log_output
- calls: update_repair_chunk_display
- calls: warning
## chatterbox_gui:ChatterboxMainWindow.add_analyzer_files
- calls: Path
- calls: QListWidgetItem
- calls: addItem
- calls: getOpenFileNames
- calls: len
- calls: log_output
- calls: setData
- calls: setToolTip
- calls: update_analyzer_ui_state
## chatterbox_gui:ChatterboxMainWindow.add_output_files
- calls: Path
- calls: QListWidgetItem
- calls: addItem
- calls: getOpenFileNames
- calls: len
- calls: log_output
- calls: setData
- calls: setToolTip
- calls: update_output_analyzer_ui_state
## chatterbox_gui:ChatterboxMainWindow.analyze_all_outputs
- calls: append
- calls: count
- calls: data
- calls: item
- calls: range
- calls: start_output_analysis
- calls: warning
## chatterbox_gui:ChatterboxMainWindow.analyze_all_voices
- calls: append
- calls: count
- calls: data
- calls: item
- calls: range
- calls: start_voice_analysis
- calls: warning
## chatterbox_gui:ChatterboxMainWindow.analyze_audiobook_file
- calls: Path
- calls: abs
- calls: append
- calls: estimate_bitrate
- calls: fft
- calls: fftfreq
- calls: getsize
- calls: int
- calls: len
- calls: load
- calls: log10
- calls: lower
- calls: max
- calls: mean
- calls: range
- calls: sort
- calls: sqrt
- calls: std
- calls: str
- calls: sum
## chatterbox_gui:ChatterboxMainWindow.analyze_selected_output
- calls: currentItem
- calls: data
- calls: start_output_analysis
- calls: warning
## chatterbox_gui:ChatterboxMainWindow.analyze_selected_voice
- calls: currentItem
- calls: data
- calls: start_voice_analysis
- calls: warning
## chatterbox_gui:ChatterboxMainWindow.analyze_system
- calls: categorize_system
- calls: get_system_profile
- calls: setPlainText
- calls: str
- calls: update_asr_models
## chatterbox_gui:ChatterboxMainWindow.apply_analyzer_fixes
- calls: Path
- calls: QListWidgetItem
- calls: abs
- calls: addItem
- calls: analyze_selected_voice
- calls: append
- calls: critical
- calls: currentItem
- calls: data
- calls: get
- calls: getSaveFileName
- calls: information
- calls: isChecked
- calls: isinstance
- calls: items
- calls: len
- calls: log_output
- calls: process_voice_sample
- calls: question
- calls: setCurrentItem
- calls: setData
- calls: setRange
- calls: setText
- calls: setToolTip
- calls: setVisible
- calls: str
- calls: value
- calls: warning
## chatterbox_gui:ChatterboxMainWindow.apply_analyzer_fixes.progress_callback
- calls: setText
## chatterbox_gui:ChatterboxMainWindow.apply_preset
- calls: currentText
- calls: format_exc
- calls: get
- calls: isChecked
- calls: keys
- calls: list
- calls: log_output
- calls: setChecked
- calls: setCurrentText
- calls: setValue
- calls: str
- calls: value
## chatterbox_gui:ChatterboxMainWindow.browse_book_folder
- calls: getExistingDirectory
- calls: populate_text_files
- calls: setText
- calls: setValue
- calls: value
## chatterbox_gui:ChatterboxMainWindow.browse_combine_book
- calls: getExistingDirectory
- calls: setText
## chatterbox_gui:ChatterboxMainWindow.browse_json_file
- calls: basename
- calls: dirname
- calls: getOpenFileName
- calls: log_output
- calls: setText
- calls: setValue
- calls: value
## chatterbox_gui:ChatterboxMainWindow.browse_m4b_file
- calls: Path
- calls: cwd
- calls: exists
- calls: getOpenFileName
- calls: log_output
- calls: lower
- calls: resolve
- calls: setEnabled
- calls: setToolTip
- calls: str
- calls: warning
## chatterbox_gui:ChatterboxMainWindow.browse_prepare_text
- calls: getOpenFileName
- calls: setText
## chatterbox_gui:ChatterboxMainWindow.browse_voice_file
- calls: Path
- calls: getOpenFileName
- calls: hasattr
- calls: setEnabled
- calls: setText
- calls: setValue
- calls: str
- calls: value
## chatterbox_gui:ChatterboxMainWindow.build_voice_analyzer_gui
- calls: QCheckBox
- calls: QGroupBox
- calls: QHBoxLayout
- calls: QLabel
- calls: QListWidget
- calls: QProgressBar
- calls: QPushButton
- calls: QSplitter
- calls: QTabWidget
- calls: QVBoxLayout
- calls: QWidget
- calls: addLayout
- calls: addStretch
- calls: addWidget
- calls: connect
- calls: setChecked
- calls: setEnabled
- calls: setMaximumWidth
- calls: setSizes
- calls: setStyleSheet
- calls: setToolTip
- calls: setVisible
- calls: setup_analyzer_autofix_tab
- calls: setup_analyzer_comparison_tab
- calls: setup_analyzer_plots_tab
- calls: setup_analyzer_recommendations_tab
- calls: setup_analyzer_scores_tab
- calls: update_analyzer_ui_state
## chatterbox_gui:ChatterboxMainWindow.check_unsaved_config_changes
- calls: question
- calls: save_config_to_file
## chatterbox_gui:ChatterboxMainWindow.clear_all_analyzer_fixes
- calls: setChecked
## chatterbox_gui:ChatterboxMainWindow.clear_analyzer_displays
- calls: clear_analyzer_scores_grid
- calls: setStyleSheet
- calls: setText
## chatterbox_gui:ChatterboxMainWindow.clear_analyzer_files
- calls: clear
- calls: clear_analyzer_displays
- calls: update_analyzer_ui_state
## chatterbox_gui:ChatterboxMainWindow.clear_analyzer_scores_grid
- calls: count
- calls: deleteLater
- calls: takeAt
- calls: widget
## chatterbox_gui:ChatterboxMainWindow.clear_output_displays
- calls: clear_output_quality_grid
- calls: setStyleSheet
- calls: setText
## chatterbox_gui:ChatterboxMainWindow.clear_output_files
- calls: clear
- calls: clear_output_displays
- calls: update_output_analyzer_ui_state
## chatterbox_gui:ChatterboxMainWindow.clear_output_quality_grid
- calls: count
- calls: deleteLater
- calls: takeAt
- calls: widget
## chatterbox_gui:ChatterboxMainWindow.closeEvent
- calls: accept
- calls: hasattr
- calls: stop_voice_sample
## chatterbox_gui:ChatterboxMainWindow.combine_audio
- calls: Path
- calls: ProcessThread
- calls: connect
- calls: log_output
- calls: on_combine_finished
- calls: start
- calls: text
- calls: update_status_display
- calls: warning
## chatterbox_gui:ChatterboxMainWindow.combine_audio_wav_only
- calls: Path
- calls: ProcessThread
- calls: connect
- calls: log_output
- calls: on_combine_wav_finished
- calls: start
- calls: text
- calls: update_status_display
- calls: warning
## chatterbox_gui:ChatterboxMainWindow.create_audio_output_analyzer_tab
- calls: QCheckBox
- calls: QFont
- calls: QGridLayout
- calls: QGroupBox
- calls: QHBoxLayout
- calls: QLabel
- calls: QListWidget
- calls: QProgressBar
- calls: QPushButton
- calls: QSplitter
- calls: QTabWidget
- calls: QVBoxLayout
- calls: QWidget
- calls: addLayout
- calls: addStretch
- calls: addTab
- calls: addWidget
- calls: connect
- calls: setAlignment
- calls: setChecked
- calls: setEnabled
- calls: setFont
- calls: setMaximumWidth
- calls: setSizes
- calls: setStyleSheet
- calls: setToolTip
- calls: setVisible
- calls: setWordWrap
- calls: setup_output_chapter_tab
- calls: setup_output_comparison_tab
- calls: setup_output_quality_tab
- calls: setup_output_standards_tab
- calls: setup_output_technical_tab
- calls: update_output_analyzer_ui_state
## chatterbox_gui:ChatterboxMainWindow.create_combine_tab
- calls: QFormLayout
- calls: QGroupBox
- calls: QHBoxLayout
- calls: QLabel
- calls: QLineEdit
- calls: QProgressBar
- calls: QPushButton
- calls: QVBoxLayout
- calls: QWidget
- calls: addLayout
- calls: addRow
- calls: addStretch
- calls: addTab
- calls: addWidget
- calls: connect
- calls: setPlaceholderText
- calls: setStyleSheet
- calls: setVisible
- calls: setWordWrap
## chatterbox_gui:ChatterboxMainWindow.create_config_tab
- calls: NoScrollDoubleSpinBox
- calls: NoScrollSpinBox
- calls: QCheckBox
- calls: QComboBox
- calls: QFormLayout
- calls: QGroupBox
- calls: QHBoxLayout
- calls: QLabel
- calls: QPushButton
- calls: QScrollArea
- calls: QVBoxLayout
- calls: QWidget
- calls: _attach_config_key
- calls: _attach_spin_reset
- calls: addItems
- calls: addLayout
- calls: addRow
- calls: addSpacing
- calls: addStretch
- calls: addTab
- calls: addWidget
- calls: bool
- calls: connect
- calls: getattr
- calls: globals
- calls: save_original_config_values
- calls: setChecked
- calls: setCurrentText
- calls: setDecimals
- calls: setMaximumWidth
- calls: setRange
- calls: setSingleStep
- calls: setStyleSheet
- calls: setToolTip
- calls: setValue
- calls: setVerticalScrollBarPolicy
- calls: setVisible
- calls: setWidget
- calls: setWidgetResizable
- calls: setWordWrap
- calls: setup_config_change_tracking
- calls: str
## chatterbox_gui:ChatterboxMainWindow.create_convert_book_tab
- calls: NoScrollDoubleSpinBox
- calls: NoScrollSpinBox
- calls: QButtonGroup
- calls: QCheckBox
- calls: QComboBox
- calls: QFormLayout
- calls: QGroupBox
- calls: QHBoxLayout
- calls: QLabel
- calls: QLineEdit
- calls: QPushButton
- calls: QRadioButton
- calls: QScrollArea
- calls: QTextEdit
- calls: QVBoxLayout
- calls: QWidget
- calls: StructuredStatusPanel
- calls: _attach_spin_reset
- calls: addButton
- calls: addItems
- calls: addLayout
- calls: addRow
- calls: addSpacing
- calls: addStretch
- calls: addTab
- calls: addWidget
- calls: connect
- calls: detect_and_update_device_status
- calls: keys
- calls: list
- calls: setChecked
- calls: setCurrentText
- calls: setDecimals
- calls: setEnabled
- calls: setHorizontalScrollBarPolicy
- calls: setLayout
- calls: setMaximumHeight
- calls: setMaximumWidth
- calls: setPlaceholderText
- calls: setPlainText
- calls: setRange
- calls: setReadOnly
- calls: setSingleStep
- calls: setSizePolicy
- calls: setStyleSheet
- calls: setToolTip
- calls: setValue
- calls: setVerticalScrollBarPolicy
- calls: setVisible
- calls: setWidget
- calls: setWidgetResizable
- calls: str
## chatterbox_gui:ChatterboxMainWindow.create_json_generate_tab
- calls: QComboBox
- calls: QFormLayout
- calls: QGroupBox
- calls: QHBoxLayout
- calls: QLabel
- calls: QLineEdit
- calls: QProgressBar
- calls: QPushButton
- calls: QSlider
- calls: QVBoxLayout
- calls: QWidget
- calls: StructuredStatusPanel
- calls: addLayout
- calls: addRow
- calls: addStretch
- calls: addTab
- calls: addWidget
- calls: connect
- calls: refresh_json_voices
- calls: setAlignment
- calls: setEnabled
- calls: setPlaceholderText
- calls: setStyleSheet
- calls: setVisible
## chatterbox_gui:ChatterboxMainWindow.create_output_area
- calls: QWidget
- calls: create_output_area_widget
## chatterbox_gui:ChatterboxMainWindow.create_output_area_widget
- calls: QGroupBox
- calls: QPushButton
- calls: QTextEdit
- calls: QVBoxLayout
- calls: addWidget
- calls: connect
- calls: setContentsMargins
- calls: setMinimumHeight
- calls: setStyleSheet
## chatterbox_gui:ChatterboxMainWindow.create_output_score_widget
- calls: QFont
- calls: QLabel
- calls: QVBoxLayout
- calls: QWidget
- calls: addWidget
- calls: setAlignment
- calls: setFont
- calls: setStyleSheet
- calls: setWordWrap
## chatterbox_gui:ChatterboxMainWindow.create_prepare_text_tab
- calls: QFormLayout
- calls: QGroupBox
- calls: QHBoxLayout
- calls: QLabel
- calls: QLineEdit
- calls: QProgressBar
- calls: QPushButton
- calls: QVBoxLayout
- calls: QWidget
- calls: addRow
- calls: addStretch
- calls: addTab
- calls: addWidget
- calls: connect
- calls: setPlaceholderText
- calls: setStyleSheet
- calls: setVisible
- calls: setWordWrap
## chatterbox_gui:ChatterboxMainWindow.create_repair_tool_tab
- calls: NoScrollDoubleSpinBox
- calls: QComboBox
- calls: QGroupBox
- calls: QHBoxLayout
- calls: QLabel
- calls: QLineEdit
- calls: QListWidget
- calls: QPushButton
- calls: QTextEdit
- calls: QVBoxLayout
- calls: QWidget
- calls: addItem
- calls: addItems
- calls: addLayout
- calls: addStretch
- calls: addTab
- calls: addWidget
- calls: connect
- calls: refresh_repair_books
- calls: setDecimals
- calls: setMaximumHeight
- calls: setMaximumWidth
- calls: setPlaceholderText
- calls: setRange
- calls: setSingleStep
- calls: setSpacing
- calls: setStyleSheet
## chatterbox_gui:ChatterboxMainWindow.create_resume_tab
- calls: QGroupBox
- calls: QLabel
- calls: QListWidget
- calls: QProgressBar
- calls: QPushButton
- calls: QVBoxLayout
- calls: QWidget
- calls: addStretch
- calls: addTab
- calls: addWidget
- calls: connect
- calls: setStyleSheet
- calls: setVisible
## chatterbox_gui:ChatterboxMainWindow.create_score_widget
- calls: QFont
- calls: QLabel
- calls: QVBoxLayout
- calls: QWidget
- calls: addWidget
- calls: setAlignment
- calls: setFont
- calls: setStyleSheet
- calls: setWordWrap
## chatterbox_gui:ChatterboxMainWindow.create_test_chunking_tab
- calls: NoScrollDoubleSpinBox
- calls: NoScrollSpinBox
- calls: QCheckBox
- calls: QFormLayout
- calls: QGroupBox
- calls: QLabel
- calls: QPushButton
- calls: QTextEdit
- calls: QVBoxLayout
- calls: QWidget
- calls: addRow
- calls: addStretch
- calls: addTab
- calls: addWidget
- calls: connect
- calls: setChecked
- calls: setDecimals
- calls: setEnabled
- calls: setMaximumHeight
- calls: setPlaceholderText
- calls: setRange
- calls: setSingleStep
- calls: setStyleSheet
- calls: setToolTip
- calls: setValue
## chatterbox_gui:ChatterboxMainWindow.create_voice_analyzer_tab
- calls: QLabel
- calls: QPushButton
- calls: QVBoxLayout
- calls: QWidget
- calls: addLayout
- calls: addStretch
- calls: addTab
- calls: addWidget
- calls: build_voice_analyzer_gui
- calls: connect
- calls: setStyleSheet
- calls: setWordWrap
- calls: str
## chatterbox_gui:ChatterboxMainWindow.detect_and_update_device_status
- calls: device_count
- calls: float
- calls: get_device_name
- calls: get_device_properties
- calls: group
- calls: hasattr
- calls: int
- calls: is_available
- calls: len
- calls: log_output
- calls: run
- calls: search
- calls: setStyleSheet
- calls: setText
- calls: split
- calls: startswith
- calls: str
## chatterbox_gui:ChatterboxMainWindow.detect_and_update_voice_info
- calls: addItem
- calls: clear
- calls: currentData
- calls: get_likely_voices_for_book
- calls: len
- calls: log_output
- calls: setStyleSheet
- calls: setText
## chatterbox_gui:ChatterboxMainWindow.estimate_bitrate
- calls: getsize
- calls: int
## chatterbox_gui:ChatterboxMainWindow.export_analyzer_plot
- calls: Path
- calls: critical
- calls: getSaveFileName
- calls: hasattr
- calls: information
- calls: log_output
- calls: savefig
- calls: str
- calls: warning
## chatterbox_gui:ChatterboxMainWindow.export_analyzer_report
- calls: Path
- calls: create_summary_report
- calls: critical
- calls: getSaveFileName
- calls: information
- calls: log_output
- calls: open
- calls: str
- calls: warning
- calls: write
## chatterbox_gui:ChatterboxMainWindow.export_output_plot
- calls: Path
- calls: critical
- calls: getSaveFileName
- calls: hasattr
- calls: information
- calls: log_output
- calls: savefig
- calls: str
- calls: warning
## chatterbox_gui:ChatterboxMainWindow.export_output_report
- calls: Path
- calls: critical
- calls: getSaveFileName
- calls: information
- calls: int
- calls: isinstance
- calls: items
- calls: log_output
- calls: open
- calls: replace
- calls: str
- calls: title
- calls: upper
- calls: warning
- calls: write
## chatterbox_gui:ChatterboxMainWindow.ff_json_audio
- calls: log_output
## chatterbox_gui:ChatterboxMainWindow.generate_from_json
- calls: Path
- calls: ProcessThread
- calls: analyze_and_optimize_tokens
- calls: basename
- calls: connect
- calls: critical
- calls: currentText
- calls: exists
- calls: format_analysis_summary
- calls: hasattr
- calls: information
- calls: log_output
- calls: reset
- calls: setEnabled
- calls: setValue
- calls: setVisible
- calls: start
- calls: strip
- calls: text
- calls: update_status
- calls: value
- calls: warning
## chatterbox_gui:ChatterboxMainWindow.handle_asr_toggle
- calls: setVisible
## chatterbox_gui:ChatterboxMainWindow.handle_micro_batching_toggle
- calls: bool
- calls: info
## chatterbox_gui:ChatterboxMainWindow.handle_vader_toggle
- calls: bool
- calls: hasattr
- calls: isChecked
- calls: setChecked
## chatterbox_gui:ChatterboxMainWindow.init_token_logging
- calls: init_token_log
- calls: log_output
## chatterbox_gui:ChatterboxMainWindow.json_generation_finished
- calls: basename
- calls: critical
- calls: information
- calls: log_output
- calls: setEnabled
- calls: setStyleSheet
- calls: setText
- calls: setVisible
## chatterbox_gui:ChatterboxMainWindow.load_chunks_for_repair
- calls: Path
- calls: clear
- calls: currentData
- calls: detect_and_update_voice_info
- calls: enumerate
- calls: len
- calls: load_chunks
- calls: log_output
- calls: str
- calls: update_repair_chunk_display
## chatterbox_gui:ChatterboxMainWindow.log_output
- calls: append
- calls: hasattr
- calls: maximum
- calls: now
- calls: print
- calls: setValue
- calls: strftime
- calls: sub
- calls: verticalScrollBar
## chatterbox_gui:ChatterboxMainWindow.on_analyzer_file_selected
- calls: Path
- calls: data
- calls: update_analyzer_result_display
- calls: update_analyzer_ui_state
## chatterbox_gui:ChatterboxMainWindow.on_combine_finished
- calls: critical
- calls: information
- calls: log_output
- calls: update_status_display
## chatterbox_gui:ChatterboxMainWindow.on_combine_wav_finished
- calls: critical
- calls: information
- calls: log_output
- calls: update_status_display
## chatterbox_gui:ChatterboxMainWindow.on_conversion_finished
- calls: Path
- calls: _handle_token_overruns
- calls: critical
- calls: exists
- calls: get_token_overruns
- calls: information
- calls: log_output
- calls: setEnabled
- calls: setText
- calls: text
- calls: update_status_display
## chatterbox_gui:ChatterboxMainWindow.on_output_file_selected
- calls: Path
- calls: data
- calls: update_output_analyzer_ui_state
- calls: update_output_result_display
## chatterbox_gui:ChatterboxMainWindow.on_tab_changed
- calls: check_unsaved_config_changes
- calls: getattr
- calls: setCurrentIndex
## chatterbox_gui:ChatterboxMainWindow.on_text_prep_finished
- calls: critical
- calls: information
- calls: log_output
- calls: update_status_display
## chatterbox_gui:ChatterboxMainWindow.pause_json_audio
- calls: log_output
- calls: setText
- calls: text
## chatterbox_gui:ChatterboxMainWindow.play_json_audio
- calls: Popen
- calls: basename
- calls: critical
- calls: exists
- calls: log_output
- calls: setEnabled
- calls: system
- calls: warning
## chatterbox_gui:ChatterboxMainWindow.play_m4b_file
- calls: Popen
- calls: critical
- calls: exists
- calls: hasattr
- calls: information
- calls: log_output
- calls: str
## chatterbox_gui:ChatterboxMainWindow.play_original_chunk
- calls: exists
- calls: log_output
- calls: play_chunk_audio
- calls: str
- calls: warning
## chatterbox_gui:ChatterboxMainWindow.play_revised_chunk
- calls: exists
- calls: log_output
- calls: play_chunk_audio
- calls: str
- calls: warning
## chatterbox_gui:ChatterboxMainWindow.play_voice_sample
- calls: Path
- calls: PlaySound
- calls: Popen
- calls: QMessageBox
- calls: QTimer
- calls: connect
- calls: exec_
- calls: exists
- calls: get_init
- calls: hasattr
- calls: init
- calls: load
- calls: play
- calls: setEnabled
- calls: setIcon
- calls: setInformativeText
- calls: setText
- calls: setWindowTitle
- calls: singleShot
- calls: start
- calls: stop_voice_sample
- calls: str
- calls: system
- calls: text
- calls: warning
## chatterbox_gui:ChatterboxMainWindow.populate_text_files
- calls: Path
- calls: addItem
- calls: clear
- calls: glob
- calls: list
- calls: str
## chatterbox_gui:ChatterboxMainWindow.prepare_text
- calls: Path
- calls: ProcessThread
- calls: connect
- calls: log_output
- calls: on_text_prep_finished
- calls: start
- calls: text
- calls: update_status_display
- calls: warning
## chatterbox_gui:ChatterboxMainWindow.refresh_available_voices
- calls: detect_and_update_voice_info
- calls: log_output
## chatterbox_gui:ChatterboxMainWindow.refresh_incomplete_books
- calls: addItem
- calls: clear
- calls: find_incomplete_books
- calls: len
- calls: log_output
- calls: str
## chatterbox_gui:ChatterboxMainWindow.refresh_json_voices
- calls: addItem
- calls: clear
- calls: len
- calls: list_voice_samples
- calls: log_output
- calls: str
## chatterbox_gui:ChatterboxMainWindow.refresh_repair_books
- calls: Path
- calls: addItem
- calls: any
- calls: append
- calls: clear
- calls: exists
- calls: glob
- calls: is_dir
- calls: iterdir
- calls: len
- calls: log_output
- calls: replace
## chatterbox_gui:ChatterboxMainWindow.regenerate_m4b
- calls: QMessageBox
- calls: append
- calls: convert_to_m4b
- calls: critical
- calls: currentText
- calls: exec_
- calls: exists
- calls: glob
- calls: hasattr
- calls: information
- calls: int
- calls: log_output
- calls: max
- calls: rename
- calls: setEnabled
- calls: setIcon
- calls: setInformativeText
- calls: setText
- calls: setToolTip
- calls: setWindowTitle
- calls: split
- calls: stat
- calls: str
- calls: strip
- calls: unlink
- calls: value
- calls: warning
## chatterbox_gui:ChatterboxMainWindow.reload_tab1_from_config
- calls: blockSignals
- calls: float
- calls: getattr
- calls: hasattr
- calls: int
- calls: isinstance
- calls: max
- calls: maximum
- calls: min
- calls: minimum
- calls: reload
- calls: setValue
- calls: showMessage
- calls: statusBar
## chatterbox_gui:ChatterboxMainWindow.remove_analyzer_file
- calls: Path
- calls: clear_analyzer_displays
- calls: currentItem
- calls: currentRow
- calls: data
- calls: takeItem
- calls: update_analyzer_ui_state
## chatterbox_gui:ChatterboxMainWindow.remove_output_file
- calls: Path
- calls: clear_output_displays
- calls: currentItem
- calls: currentRow
- calls: data
- calls: takeItem
- calls: update_output_analyzer_ui_state
## chatterbox_gui:ChatterboxMainWindow.reset_config_defaults
- calls: critical
- calls: currentText
- calls: getattr
- calls: hasattr
- calls: int
- calls: isChecked
- calls: log_output
- calls: reload
- calls: setChecked
- calls: setCurrentText
- calls: setValue
- calls: showMessage
- calls: statusBar
- calls: str
- calls: value
## chatterbox_gui:ChatterboxMainWindow.resume_processing
- calls: ProcessThread
- calls: connect
- calls: currentItem
- calls: log_output
- calls: start
- calls: text
- calls: warning
## chatterbox_gui:ChatterboxMainWindow.resynthesize_chunk
- calls: copy
- calls: critical
- calls: currentData
- calls: currentText
- calls: information
- calls: len
- calls: log_output
- calls: split
- calls: synthesize_chunk
- calls: toPlainText
- calls: value
- calls: warning
## chatterbox_gui:ChatterboxMainWindow.rewind_json_audio
- calls: log_output
## chatterbox_gui:ChatterboxMainWindow.run_book_conversion
- calls: get
- calls: get_best_available_device
- calls: print
- calls: print_exc
- calls: process_book_folder
- calls: upper
## chatterbox_gui:ChatterboxMainWindow.save_chunk_changes
- calls: OrderedDict
- calls: critical
- calls: currentText
- calls: deepcopy
- calls: exists
- calls: fromtimestamp
- calls: get
- calls: getmtime
- calls: information
- calls: keys
- calls: len
- calls: list
- calls: load_chunks
- calls: log_output
- calls: round
- calls: save_chunks
- calls: split
- calls: str
- calls: strftime
- calls: toPlainText
- calls: value
- calls: warning
## chatterbox_gui:ChatterboxMainWindow.save_config_to_file
- calls: _release_global_tts_model
- calls: blockSignals
- calls: collect
- calls: critical
- calls: currentText
- calls: empty_cache
- calls: getattr
- calls: hasattr
- calls: int
- calls: ipc_collect
- calls: isChecked
- calls: is_available
- calls: items
- calls: log_output
- calls: open
- calls: read
- calls: reload
- calls: setCurrentText
- calls: setValue
- calls: showMessage
- calls: statusBar
- calls: str
- calls: sub
- calls: synchronize
- calls: value
- calls: write
## chatterbox_gui:ChatterboxMainWindow.save_original_config_values
- calls: isChecked
- calls: value
## chatterbox_gui:ChatterboxMainWindow.search_chunks_by_number
- calls: QListWidgetItem
- calls: addItem
- calls: append
- calls: clear
- calls: get
- calls: int
- calls: isdigit
- calls: len
- calls: log_output
- calls: setData
- calls: split
- calls: strip
- calls: text
- calls: warning
## chatterbox_gui:ChatterboxMainWindow.search_chunks_for_repair
- calls: QListWidgetItem
- calls: addItem
- calls: clear
- calls: len
- calls: log_output
- calls: search_chunks
- calls: setData
- calls: strip
- calls: text
- calls: warning
## chatterbox_gui:ChatterboxMainWindow.select_all_analyzer_fixes
- calls: setChecked
## chatterbox_gui:ChatterboxMainWindow.select_chunk_for_repair
- calls: data
- calls: log_output
- calls: update_repair_chunk_display
## chatterbox_gui:ChatterboxMainWindow.select_recommended_analyzer_fixes
- calls: clear_all_analyzer_fixes
- calls: information
- calls: log_output
- calls: setChecked
## chatterbox_gui:ChatterboxMainWindow.setup_analyzer_autofix_tab
- calls: NoScrollSpinBox
- calls: QCheckBox
- calls: QFont
- calls: QGroupBox
- calls: QHBoxLayout
- calls: QLabel
- calls: QProgressBar
- calls: QPushButton
- calls: QScrollArea
- calls: QVBoxLayout
- calls: QWidget
- calls: addLayout
- calls: addStretch
- calls: addTab
- calls: addWidget
- calls: connect
- calls: setAlignment
- calls: setChecked
- calls: setEnabled
- calls: setFont
- calls: setLayout
- calls: setRange
- calls: setStyleSheet
- calls: setToolTip
- calls: setValue
- calls: setVisible
- calls: setWidget
- calls: setWidgetResizable
- calls: setWordWrap
## chatterbox_gui:ChatterboxMainWindow.setup_analyzer_comparison_tab
- calls: Figure
- calls: FigureCanvas
- calls: QLabel
- calls: QVBoxLayout
- calls: QWidget
- calls: addTab
- calls: addWidget
- calls: add_subplot
- calls: draw
- calls: setAlignment
- calls: setStyleSheet
- calls: set_title
- calls: text
## chatterbox_gui:ChatterboxMainWindow.setup_analyzer_plots_tab
- calls: Figure
- calls: FigureCanvas
- calls: QLabel
- calls: QVBoxLayout
- calls: QWidget
- calls: addTab
- calls: addWidget
- calls: add_subplot
- calls: draw
- calls: setAlignment
- calls: setStyleSheet
- calls: set_title
- calls: text
## chatterbox_gui:ChatterboxMainWindow.setup_analyzer_recommendations_tab
- calls: QFont
- calls: QTextEdit
- calls: QVBoxLayout
- calls: QWidget
- calls: addTab
- calls: addWidget
- calls: setFont
- calls: setReadOnly
- calls: setText
## chatterbox_gui:ChatterboxMainWindow.setup_analyzer_scores_tab
- calls: QFont
- calls: QGridLayout
- calls: QLabel
- calls: QScrollArea
- calls: QVBoxLayout
- calls: QWidget
- calls: addTab
- calls: addWidget
- calls: setAlignment
- calls: setFont
- calls: setStyleSheet
- calls: setWidget
- calls: setWidgetResizable
## chatterbox_gui:ChatterboxMainWindow.setup_config_change_tracking
- calls: connect
## chatterbox_gui:ChatterboxMainWindow.setup_output_chapter_tab
- calls: QFont
- calls: QTextEdit
- calls: QVBoxLayout
- calls: QWidget
- calls: addTab
- calls: addWidget
- calls: setFont
- calls: setReadOnly
- calls: setText
## chatterbox_gui:ChatterboxMainWindow.setup_output_comparison_tab
- calls: Figure
- calls: FigureCanvas
- calls: QLabel
- calls: QVBoxLayout
- calls: QWidget
- calls: addTab
- calls: addWidget
- calls: add_subplot
- calls: draw
- calls: setAlignment
- calls: setStyleSheet
- calls: set_title
- calls: text
## chatterbox_gui:ChatterboxMainWindow.setup_output_quality_tab
- calls: QFont
- calls: QGridLayout
- calls: QLabel
- calls: QScrollArea
- calls: QVBoxLayout
- calls: QWidget
- calls: addTab
- calls: addWidget
- calls: setAlignment
- calls: setFont
- calls: setStyleSheet
- calls: setWidget
- calls: setWidgetResizable
## chatterbox_gui:ChatterboxMainWindow.setup_output_standards_tab
- calls: QFont
- calls: QTextEdit
- calls: QVBoxLayout
- calls: QWidget
- calls: addTab
- calls: addWidget
- calls: setFont
- calls: setReadOnly
- calls: setText
## chatterbox_gui:ChatterboxMainWindow.setup_output_technical_tab
- calls: QFont
- calls: QTextEdit
- calls: QVBoxLayout
- calls: QWidget
- calls: addTab
- calls: addWidget
- calls: setFont
- calls: setReadOnly
- calls: setText
## chatterbox_gui:ChatterboxMainWindow.start_conversion
- calls: Path
- calls: ProcessThread
- calls: _build_effective_settings
- calls: checkedId
- calls: clear_token_overruns
- calls: connect
- calls: currentData
- calls: currentText
- calls: get
- calls: get_system_profile
- calls: hasattr
- calls: isChecked
- calls: log_output
- calls: print
- calls: recommend_asr_models
- calls: reset
- calls: setEnabled
- calls: setText
- calls: singleShot
- calls: start
- calls: text
- calls: update_status
- calls: update_status_display
- calls: upper
- calls: value
- calls: warning
## chatterbox_gui:ChatterboxMainWindow.start_conversion.debug_scroll
- calls: maximum
- calls: print
- calls: setValue
- calls: verticalScrollBar
## chatterbox_gui:ChatterboxMainWindow.start_output_analysis
- calls: Path
- calls: analyze_audiobook_file
- calls: append
- calls: currentItem
- calls: data
- calls: enumerate
- calls: hasattr
- calls: len
- calls: log_output
- calls: setEnabled
- calls: setRange
- calls: setText
- calls: setValue
- calls: setVisible
- calls: str
- calls: update_output_analyzer_ui_state
- calls: update_output_comparison_plot
- calls: update_output_result_display
## chatterbox_gui:ChatterboxMainWindow.start_voice_analysis
- calls: Path
- calls: analyze_voice_sample
- calls: append
- calls: currentItem
- calls: data
- calls: enumerate
- calls: isChecked
- calls: len
- calls: log_output
- calls: setEnabled
- calls: setRange
- calls: setText
- calls: setValue
- calls: setVisible
- calls: str
- calls: update_analyzer_result_display
- calls: update_analyzer_ui_state
## chatterbox_gui:ChatterboxMainWindow.stop_json_audio
- calls: log_output
- calls: setEnabled
- calls: setText
- calls: terminate
## chatterbox_gui:ChatterboxMainWindow.stop_voice_sample
- calls: PlaySound
- calls: _reset_voice_buttons
- calls: get_init
- calls: print
- calls: stop
- calls: system
## chatterbox_gui:ChatterboxMainWindow.test_audio_system_startup
- calls: init
- calls: quit
- calls: showMessage
- calls: statusBar
- calls: system
## chatterbox_gui:ChatterboxMainWindow.test_chunking
- calls: ChunkingTestWindow
- calls: StringIO
- calls: critical
- calls: getvalue
- calls: log_output
- calls: redirect_stdout
- calls: set_chunking_results
- calls: show
- calls: strip
- calls: test_chunking
- calls: toPlainText
- calls: value
## chatterbox_gui:ChatterboxMainWindow.try_install_voice_analyzer_deps
- calls: critical
- calls: information
- calls: log_output
- calls: question
- calls: run
- calls: str
## chatterbox_gui:ChatterboxMainWindow.update_analyzer_comparison_plot
- calls: add_subplot
- calls: arange
- calls: axhline
- calls: bar
- calls: clear
- calls: draw
- calls: enumerate
- calls: get_height
- calls: get_width
- calls: get_x
- calls: grid
- calls: hasattr
- calls: legend
- calls: len
- calls: range
- calls: set_title
- calls: set_xticklabels
- calls: set_xticks
- calls: set_ylabel
- calls: set_ylim
- calls: str
- calls: text
- calls: tight_layout
- calls: zip
## chatterbox_gui:ChatterboxMainWindow.update_analyzer_fix_ui_state
- calls: any
- calls: currentItem
- calls: isChecked
- calls: setEnabled
- calls: setText
- calls: sum
## chatterbox_gui:ChatterboxMainWindow.update_analyzer_result_display
- calls: addWidget
- calls: clear_analyzer_scores_grid
- calls: create_score_widget
- calls: enumerate
- calls: len
- calls: setStyleSheet
- calls: setText
- calls: update_analyzer_comparison_plot
- calls: update_analyzer_visualization
## chatterbox_gui:ChatterboxMainWindow.update_analyzer_ui_state
- calls: count
- calls: currentItem
- calls: len
- calls: setEnabled
## chatterbox_gui:ChatterboxMainWindow.update_analyzer_visualization
- calls: add_subplot
- calls: axhline
- calls: bar
- calls: clear
- calls: draw
- calls: get_height
- calls: get_width
- calls: get_x
- calls: get_xticklabels
- calls: grid
- calls: hasattr
- calls: legend
- calls: set_title
- calls: set_ylabel
- calls: set_ylim
- calls: setp
- calls: str
- calls: text
- calls: tight_layout
- calls: zip
## chatterbox_gui:ChatterboxMainWindow.update_asr_models
- calls: checkedId
- calls: get_system_profile
- calls: recommend_asr_models
- calls: setPlainText
- calls: str
- calls: upper
## chatterbox_gui:ChatterboxMainWindow.update_output_analyzer_ui_state
- calls: count
- calls: currentItem
- calls: len
- calls: setEnabled
## chatterbox_gui:ChatterboxMainWindow.update_output_comparison_plot
- calls: add_subplot
- calls: arange
- calls: axhline
- calls: bar
- calls: clear
- calls: draw
- calls: enumerate
- calls: get_height
- calls: get_width
- calls: get_x
- calls: grid
- calls: hasattr
- calls: legend
- calls: len
- calls: range
- calls: set_title
- calls: set_xticklabels
- calls: set_xticks
- calls: set_ylabel
- calls: set_ylim
- calls: str
- calls: text
- calls: tight_layout
- calls: zip
## chatterbox_gui:ChatterboxMainWindow.update_output_result_display
- calls: addWidget
- calls: append
- calls: clear_output_quality_grid
- calls: create_output_score_widget
- calls: enumerate
- calls: int
- calls: setStyleSheet
- calls: setText
- calls: upper
## chatterbox_gui:ChatterboxMainWindow.update_repair_chunk_display
- calls: clear
- calls: get
- calls: setCurrentText
- calls: setPlainText
- calls: setText
- calls: setValue
## chatterbox_gui:ChatterboxMainWindow.update_tab1_status_panel
- calls: get
- calls: hasattr
- calls: update_status
## chatterbox_gui:ChatterboxMainWindow.update_tab8_status_panel
- calls: get
- calls: hasattr
- calls: update_status
## chatterbox_gui:ChunkingTestWindow.__init__
- calls: QHBoxLayout
- calls: QLabel
- calls: QPushButton
- calls: QTextEdit
- calls: QVBoxLayout
- calls: __init__
- calls: addLayout
- calls: addStretch
- calls: addWidget
- calls: connect
- calls: setGeometry
- calls: setModal
- calls: setReadOnly
- calls: setStyleSheet
- calls: setWindowTitle
- calls: super
## chatterbox_gui:ChunkingTestWindow.copy_to_clipboard
- calls: clipboard
- calls: information
- calls: setText
- calls: toPlainText
## chatterbox_gui:ChunkingTestWindow.set_chunking_results
- calls: movePosition
- calls: setPlainText
- calls: setTextCursor
- calls: textCursor
## chatterbox_gui:NoScrollDoubleSpinBox.wheelEvent
- calls: ignore
## chatterbox_gui:NoScrollSpinBox.wheelEvent
- calls: ignore
## chatterbox_gui:ProcessThread
- calls: pyqtSignal
## chatterbox_gui:ProcessThread.__init__
- calls: __init__
- calls: super
## chatterbox_gui:ProcessThread.parse_and_emit_status
- calls: emit
- calls: group
- calls: int
- calls: search
## chatterbox_gui:ProcessThread.parse_chunk_progress
- calls: emit
- calls: group
- calls: int
- calls: search
## chatterbox_gui:ProcessThread.run
- calls: GUIOutput
- calls: emit
- calls: hasattr
- calls: str
- calls: target_function
## chatterbox_gui:ProcessThread.run.GUIOutput.flush
- calls: flush
## chatterbox_gui:ProcessThread.run.GUIOutput.write
- calls: emit
- calls: parse_chunk_progress
- calls: strip
- calls: write
## chatterbox_gui:StructuredStatusPanel.__init__
- calls: __init__
- calls: setup_ui
- calls: super
## chatterbox_gui:StructuredStatusPanel.reset
- calls: setText
- calls: setVisible
## chatterbox_gui:StructuredStatusPanel.setup_ui
- calls: QFormLayout
- calls: QLabel
- calls: QProgressBar
- calls: addRow
- calls: setFormat
- calls: setStyleSheet
- calls: setTextVisible
- calls: setVisible
## chatterbox_gui:StructuredStatusPanel.update_status
- calls: endswith
- calls: isinstance
- calls: setMaximum
- calls: setText
- calls: setValue
- calls: setVisible
- calls: str
## chatterbox_gui:main
- calls: ChatterboxMainWindow
- calls: QApplication
- calls: exec_
- calls: exit
- calls: setStyle
- calls: show
## config.config:<module>
- calls: Path
- calls: get
## gradio_app:<module>
- calls: SentimentIntensityAnalyzer
- calls: basicConfig
- calls: create_interface
- calls: error
- calls: getLogger
- calls: info
- calls: initialize_tts
- calls: launch
## gradio_app:create_interface
- calls: Accordion
- calls: Audio
- calls: Blocks
- calls: Button
- calls: Column
- calls: File
- calls: Markdown
- calls: Row
- calls: Slider
- calls: Soft
- calls: Textbox
- calls: click
## gradio_app:generate_audiobook
- calls: NamedTemporaryFile
- calls: Progress
- calls: append
- calls: cat
- calls: enumerate
- calls: error
- calls: format_exc
- calls: generate_chunk_audio
- calls: info
- calls: join
- calls: len
- calls: open
- calls: process_text_to_chunks
- calls: progress
- calls: read
- calls: save
- calls: str
- calls: strip
## gradio_app:generate_chunk_audio
- calls: add_contextual_silence
- calls: error
- calls: generate_speech
- calls: get
- calls: initialize_tts
- calls: progress_callback
## gradio_app:initialize_tts
- calls: ChatterboxTTS
- calls: error
- calls: info
- calls: is_available
- calls: set_per_process_memory_fraction
## gradio_app:process_text_to_chunks
- calls: append
- calls: enumerate
- calls: error
- calls: max
- calls: min
- calls: polarity_scores
- calls: round
- calls: sentence_chunk_text
- calls: smart_punctuate
## gradio_launcher:<module>
- calls: main
## gradio_launcher:GradioLauncher._launch_direct
- calls: exit
- calls: getenv
- calls: hasattr
- calls: launch_interface
- calls: print
- calls: sleep
- calls: str
## gradio_launcher:GradioLauncher.check_and_install_requirements
- calls: append
- calls: check_package_installed
- calls: compare_versions
- calls: get
- calls: install_package
- calls: items
- calls: len
- calls: print
## gradio_launcher:GradioLauncher.check_gpu_availability
- calls: device_count
- calls: get_device_name
- calls: hasattr
- calls: is_available
- calls: print
- calls: str
## gradio_launcher:GradioLauncher.check_package_installed
- calls: Path
- calls: exists
- calls: get_distribution
- calls: getattr
- calls: hasattr
- calls: import_module
- calls: run
- calls: split
- calls: startswith
- calls: strip
## gradio_launcher:GradioLauncher.check_python_version
- calls: exit
- calls: print
## gradio_launcher:GradioLauncher.check_working_directory
- calls: Path
- calls: append
- calls: exists
- calls: join
- calls: print
## gradio_launcher:GradioLauncher.compare_versions
- calls: extend
- calls: int
- calls: len
- calls: max
- calls: split
## gradio_launcher:GradioLauncher.create_directories
- calls: Path
- calls: append
- calls: exists
- calls: join
- calls: mkdir
- calls: print
## gradio_launcher:GradioLauncher.install_package
- calls: Path
- calls: exists
- calls: getattr
- calls: hasattr
- calls: install_package
- calls: print
- calls: run
- calls: setup_virtual_environment
- calls: str
## gradio_launcher:GradioLauncher.launch_interface
- calls: Path
- calls: _launch_direct
- calls: exists
- calls: exit
- calls: getenv
- calls: hasattr
- calls: print
- calls: run
- calls: str
## gradio_launcher:GradioLauncher.print_header
- calls: print
## gradio_launcher:GradioLauncher.run
- calls: check_and_install_requirements
- calls: check_gpu_availability
- calls: check_python_version
- calls: check_working_directory
- calls: create_directories
- calls: exit
- calls: launch_interface
- calls: print
- calls: print_header
- calls: verify_installation
## gradio_launcher:GradioLauncher.setup_virtual_environment
- calls: Path
- calls: exists
- calls: print
- calls: run
- calls: str
- calls: strip
## gradio_launcher:GradioLauncher.verify_installation
- calls: append
- calls: import_module
- calls: join
- calls: print
- calls: str
## gradio_launcher:main
- calls: GradioLauncher
- calls: run
## gradio_main_interface:<module>
- calls: Path
- calls: append
- calls: launch_interface
- calls: print
- calls: str
## gradio_main_interface:create_main_interface
- calls: Blocks
- calls: Markdown
- calls: Soft
- calls: Tab
- calls: Tabs
- calls: create_chunk_tools_tab
- calls: create_combine_audio_tab
- calls: create_configuration_tab
- calls: create_convert_book_tab
- calls: create_json_generate_tab
- calls: create_placeholder_tab
- calls: create_prepare_text_tab
- calls: create_settings_tab_interface
- calls: detect_device_status
## gradio_main_interface:create_placeholder_tab
- calls: Button
- calls: Column
- calls: Markdown
## gradio_main_interface:detect_device_status
- calls: get_device_name
- calls: get_device_properties
- calls: is_available
## gradio_main_interface:launch_interface
- calls: create_main_interface
- calls: getenv
- calls: launch
- calls: print
## gradio_tabs.tab1_convert_book:<module>
- calls: Blocks
- calls: create_convert_book_tab
- calls: filterwarnings
- calls: launch
- calls: module_from_spec
- calls: print
- calls: spec_from_file_location
## gradio_tabs.tab1_convert_book:create_convert_book_tab
- calls: Audio
- calls: Button
- calls: Checkbox
- calls: Column
- calls: Dropdown
- calls: File
- calls: Markdown
- calls: Number
- calls: Radio
- calls: Row
- calls: Slider
- calls: Textbox
- calls: WaveformOptions
- calls: change
- calls: click
- calls: keys
- calls: list
## gradio_tabs.tab1_convert_book:create_convert_book_tab.analyze_system
- calls: categorize_system
- calls: get_system_profile
- calls: str
## gradio_tabs.tab1_convert_book:create_convert_book_tab.apply_preset
- calls: get
- calls: update
## gradio_tabs.tab1_convert_book:create_convert_book_tab.get_current_stats
- calls: Path
- calls: exists
- calls: get
- calls: glob
- calls: int
- calls: len
- calls: list
- calls: load
- calls: open
- calls: print
## gradio_tabs.tab1_convert_book:create_convert_book_tab.get_session_audiobooks
- calls: Path
- calls: append
- calls: exists
- calls: glob
- calls: is_dir
- calls: iterdir
- calls: sort
- calls: stat
- calls: str
## gradio_tabs.tab1_convert_book:create_convert_book_tab.get_status_and_results
- calls: load_selected_audiobook
- calls: update
- calls: update_audiobook_dropdowns_after_conversion
## gradio_tabs.tab1_convert_book:create_convert_book_tab.handle_asr_toggle
- calls: update
## gradio_tabs.tab1_convert_book:create_convert_book_tab.handle_m4b_regeneration
- calls: Path
- calls: load_selected_audiobook
- calls: regenerate_m4b_file
- calls: update
- calls: update_playback_only
## gradio_tabs.tab1_convert_book:create_convert_book_tab.handle_voice_upload
- calls: update
## gradio_tabs.tab1_convert_book:create_convert_book_tab.load_selected_audiobook
- calls: get_session_audiobooks
## gradio_tabs.tab1_convert_book:create_convert_book_tab.start_conversion
- calls: Path
- calls: Thread
- calls: copy2
- calls: format_path_warning_text
- calls: get
- calls: get_system_profile
- calls: mkdir
- calls: now
- calls: print
- calls: recommend_asr_models
- calls: replace
- calls: start
- calls: str
- calls: strftime
- calls: update
- calls: validate_book_path
## gradio_tabs.tab1_convert_book:create_convert_book_tab.start_conversion.run_conversion_thread
- calls: get
- calls: run_book_conversion
- calls: str
## gradio_tabs.tab1_convert_book:create_convert_book_tab.update_asr_models
- calls: get_system_profile
- calls: recommend_asr_models
- calls: str
- calls: upper
## gradio_tabs.tab1_convert_book:create_convert_book_tab.update_audiobook_dropdowns
- calls: get_session_audiobooks
- calls: update
## gradio_tabs.tab1_convert_book:create_convert_book_tab.update_audiobook_dropdowns_after_conversion
- calls: update_audiobook_dropdowns
## gradio_tabs.tab1_convert_book:create_convert_book_tab.update_playback_only
- calls: get_session_audiobooks
- calls: update
## gradio_tabs.tab1_convert_book:find_generated_audiobook
- calls: Path
- calls: exists
- calls: glob
- calls: print
- calls: str
- calls: upper
## gradio_tabs.tab1_convert_book:get_book_folders
- calls: Path
- calls: append
- calls: exists
- calls: is_dir
- calls: iterdir
- calls: sorted
## gradio_tabs.tab1_convert_book:get_text_files_in_folder
- calls: Path
- calls: append
- calls: exists
- calls: glob
- calls: sorted
## gradio_tabs.tab1_convert_book:get_voice_samples
- calls: Path
- calls: append
- calls: exists
- calls: glob
- calls: sorted
## gradio_tabs.tab1_convert_book:list_text_files
- calls: Path
- calls: glob
- calls: is_dir
- calls: update
## gradio_tabs.tab1_convert_book:parse_progress_stats
- calls: group
- calls: int
- calls: print
- calls: search
## gradio_tabs.tab1_convert_book:play_voice_sample
- calls: Path
- calls: exists
- calls: get_busy
- calls: init
- calls: load
- calls: play
- calls: print
- calls: sleep
## gradio_tabs.tab1_convert_book:regenerate_m4b_file
- calls: Path
- calls: add_metadata_to_m4b
- calls: convert_to_m4b
- calls: exists
- calls: glob
- calls: is_dir
- calls: iterdir
- calls: print
- calls: replace
- calls: str
- calls: unlink
## gradio_tabs.tab1_convert_book:run_book_conversion
- calls: Path
- calls: get
- calls: get_best_available_device
- calls: print
- calls: print_exc
- calls: process_book_folder
- calls: str
- calls: upper
## gradio_tabs.tab1_convert_book:run_book_conversion.progress_callback
- calls: int
- calls: print
## gradio_tabs.tab2_configuration:<module>
- calls: Blocks
- calls: Path
- calls: create_configuration_tab
- calls: launch
## gradio_tabs.tab2_configuration:_atomic_write_with_backup
- calls: NamedTemporaryFile
- calls: copy2
- calls: now
- calls: replace
- calls: str
- calls: strftime
- calls: with_suffix
- calls: write
## gradio_tabs.tab2_configuration:_get_literal
- calls: escape
- calls: group
- calls: literal_eval
- calls: search
- calls: strip
## gradio_tabs.tab2_configuration:_load_config_from_file
- calls: _get_literal
- calls: read_text
- calls: tuple
- calls: v
## gradio_tabs.tab2_configuration:_patch_config
- calls: compile
- calls: enumerate
- calls: escape
- calls: groups
- calls: isinstance
- calls: items
- calls: join
- calls: lstrip
- calls: match
- calls: read_text
- calls: repr
- calls: splitlines
- calls: startswith
- calls: str
## gradio_tabs.tab2_configuration:create_configuration_tab
- calls: Button
- calls: Checkbox
- calls: Column
- calls: Markdown
- calls: Row
- calls: Slider
- calls: Textbox
- calls: click
- calls: field_value_from_file
## gradio_tabs.tab2_configuration:create_configuration_tab.field_value_from_file
- calls: _load_config_from_file
## gradio_tabs.tab2_configuration:create_configuration_tab.reload_configuration
- calls: _load_config_from_file
## gradio_tabs.tab2_configuration:create_configuration_tab.reset_configuration
- calls: _load_config_from_file
## gradio_tabs.tab2_configuration:create_configuration_tab.save_configuration
- calls: _atomic_write_with_backup
- calls: _patch_config
- calls: bool
- calls: exists
- calls: float
- calls: format_exc
- calls: int
- calls: reload
## gradio_tabs.tab4_combine_audio:<module>
- calls: Blocks
- calls: create_combine_audio_tab
- calls: launch
- calls: print
## gradio_tabs.tab4_combine_audio:combine_audio_for_book
- calls: ImportError
## gradio_tabs.tab4_combine_audio:create_combine_audio_tab
- calls: Button
- calls: Column
- calls: Dropdown
- calls: Markdown
- calls: Number
- calls: Row
- calls: Textbox
- calls: change
- calls: click
- calls: get_available_books
## gradio_tabs.tab4_combine_audio:create_combine_audio_tab.get_current_status
- calls: get
- calls: int
- calls: time
- calls: update
## gradio_tabs.tab4_combine_audio:create_combine_audio_tab.get_selected_book_path
- calls: strip
## gradio_tabs.tab4_combine_audio:create_combine_audio_tab.refresh_book_list
- calls: get_available_books
- calls: update
## gradio_tabs.tab4_combine_audio:create_combine_audio_tab.start_combine_operation
- calls: Path
- calls: Thread
- calls: get
- calls: get_selected_book_path
- calls: start
- calls: str
- calls: update
## gradio_tabs.tab4_combine_audio:create_combine_audio_tab.start_combine_operation.run_combine_thread
- calls: Path
- calls: append
- calls: exists
- calls: get
- calls: join
- calls: run_combine_operation
- calls: stat
- calls: str
- calls: strip
- calls: time
## gradio_tabs.tab4_combine_audio:create_combine_audio_tab.stop_combine_operation
- calls: get
- calls: update
## gradio_tabs.tab4_combine_audio:create_combine_audio_tab.update_book_info
- calls: get_book_info
## gradio_tabs.tab4_combine_audio:get_audio_files_in_directory
- calls: ImportError
## gradio_tabs.tab4_combine_audio:get_available_books
- calls: Path
- calls: append
- calls: exists
- calls: get_wav_duration
- calls: glob
- calls: int
- calls: is_dir
- calls: iterdir
- calls: len
- calls: list
- calls: sorted
- calls: str
- calls: sum
## gradio_tabs.tab4_combine_audio:get_book_info
- calls: Path
- calls: append
- calls: exists
- calls: get_audio_files_in_directory
- calls: get_wav_duration
- calls: int
- calls: join
- calls: len
- calls: stat
- calls: str
- calls: sum
## gradio_tabs.tab4_combine_audio:get_wav_duration
- calls: ImportError
## gradio_tabs.tab4_combine_audio:run_combine_operation
- calls: Path
- calls: combine_audio_for_book
- calls: print
- calls: str
## gradio_tabs.tab5_prepare_text:<module>
- calls: Blocks
- calls: create_prepare_text_tab
- calls: launch
- calls: print
## gradio_tabs.tab5_prepare_text:create_prepare_text_tab
- calls: Button
- calls: Checkbox
- calls: Column
- calls: Dropdown
- calls: Markdown
- calls: Row
- calls: Slider
- calls: Textbox
- calls: change
- calls: click
- calls: get_available_text_files
- calls: then
- calls: update
## gradio_tabs.tab5_prepare_text:create_prepare_text_tab.refresh_file_list
- calls: get_available_text_files
- calls: update
## gradio_tabs.tab5_prepare_text:generate_enriched_chunks
- calls: ImportError
## gradio_tabs.tab5_prepare_text:get_available_text_files
- calls: Path
- calls: append
- calls: exists
- calls: glob
- calls: globals
- calls: is_dir
- calls: iterdir
- calls: sorted
- calls: stat
- calls: str
## gradio_tabs.tab5_prepare_text:get_preparation_status
- calls: get
## gradio_tabs.tab5_prepare_text:load_text_file_info
- calls: Path
- calls: exists
- calls: get_available_text_files
- calls: len
- calls: load
- calls: max
- calls: open
- calls: read
- calls: split
- calls: splitlines
- calls: str
- calls: strip
## gradio_tabs.tab5_prepare_text:start_text_preparation
- calls: Thread
- calls: get_available_text_files
- calls: start
- calls: str
## gradio_tabs.tab5_prepare_text:start_text_preparation.preparation_worker
- calls: Path
- calls: format_path_warning_text
- calls: generate_enriched_chunks
- calls: int
- calls: len
- calls: mkdir
- calls: str
- calls: validate_book_path
## gradio_tabs.tab5_prepare_text:stop_text_preparation
- calls: get
## gradio_tabs.tab6_settings:<module>
- calls: print
## gradio_tabs.tab6_settings:ConfigManager.__init__
- calls: Path
- calls: load_current_config
## gradio_tabs.tab6_settings:ConfigManager.get_config_categories
- calls: any
- calls: append
- calls: items
- calls: keys
- calls: lower
## gradio_tabs.tab6_settings:ConfigManager.load_current_config
- calls: dir
- calls: getattr
- calls: isinstance
- calls: startswith
## gradio_tabs.tab6_settings:ConfigManager.reload_config
- calls: load_current_config
- calls: reload
- calls: str
## gradio_tabs.tab6_settings:ConfigManager.save_config_value
- calls: hasattr
- calls: setattr
- calls: str
## gradio_tabs.tab6_settings:create_chunking_test
- calls: Button
- calls: Column
- calls: Markdown
- calls: Row
- calls: Slider
- calls: Textbox
- calls: click
## gradio_tabs.tab6_settings:create_chunking_test.run_chunking_test
- calls: StringIO
- calls: getvalue
- calls: redirect_stdout
- calls: str
- calls: strip
- calls: test_chunking
## gradio_tabs.tab6_settings:create_config_backup
- calls: Button
- calls: Column
- calls: File
- calls: Markdown
- calls: Row
- calls: Textbox
- calls: click
## gradio_tabs.tab6_settings:create_config_backup.create_backup
- calls: Path
- calls: dir
- calls: dump
- calls: getattr
- calls: isinstance
- calls: open
- calls: startswith
- calls: str
## gradio_tabs.tab6_settings:create_config_backup.restore_backup
- calls: hasattr
- calls: items
- calls: load
- calls: open
- calls: setattr
- calls: str
## gradio_tabs.tab6_settings:create_config_editor
- calls: Accordion
- calls: Button
- calls: Checkbox
- calls: Column
- calls: Markdown
- calls: Number
- calls: Textbox
- calls: click
- calls: get
- calls: get_config_categories
- calls: isinstance
- calls: items
- calls: list
- calls: str
- calls: values
## gradio_tabs.tab6_settings:create_config_editor.reload_config
- calls: get
- calls: items
- calls: reload_config
- calls: update
- calls: values
## gradio_tabs.tab6_settings:create_config_editor.save_all_changes
- calls: append
- calls: enumerate
- calls: items
- calls: join
- calls: save_config_value
## gradio_tabs.tab6_settings:create_settings_tab
- calls: Column
- calls: ConfigManager
- calls: Markdown
- calls: Tab
- calls: Tabs
- calls: create_chunking_test
- calls: create_config_backup
- calls: create_config_editor
- calls: create_system_info
## gradio_tabs.tab6_settings:create_settings_tab_interface
- calls: create_settings_tab
## gradio_tabs.tab6_settings:create_system_info
- calls: Button
- calls: Column
- calls: Markdown
- calls: click
- calls: get_system_info
## gradio_tabs.tab6_settings:create_system_info.get_system_info
- calls: Path
- calls: append
- calls: dir
- calls: exists
- calls: getcwd
- calls: join
- calls: len
- calls: split
- calls: startswith
## gradio_tabs.tab7_chunk_tools:<module>
- calls: Blocks
- calls: create_chunk_tools_tab
- calls: launch
- calls: print
## gradio_tabs.tab7_chunk_tools:accept_chunk_revision
- calls: accept_revision
- calls: str
## gradio_tabs.tab7_chunk_tools:accept_revision
- calls: ImportError
## gradio_tabs.tab7_chunk_tools:create_chunk_tools_tab
- calls: Button
- calls: Column
- calls: Dropdown
- calls: Markdown
- calls: Row
- calls: Slider
- calls: Textbox
- calls: change
- calls: click
- calls: get_available_repair_books
- calls: submit
## gradio_tabs.tab7_chunk_tools:create_chunk_tools_tab.refresh_book_list
- calls: get_available_repair_books
- calls: update
## gradio_tabs.tab7_chunk_tools:create_chunk_tools_tab.refresh_voice_candidates
- calls: append
- calls: get_likely_voices_for_book
- calls: len
- calls: str
- calls: update
## gradio_tabs.tab7_chunk_tools:get_available_repair_books
- calls: Path
- calls: any
- calls: append
- calls: exists
- calls: glob
- calls: is_dir
- calls: iterdir
- calls: len
- calls: load
- calls: open
- calls: replace
- calls: sorted
- calls: str
## gradio_tabs.tab7_chunk_tools:get_likely_voices_for_book
- calls: ImportError
## gradio_tabs.tab7_chunk_tools:load_book_chunks
- calls: Path
- calls: append
- calls: enumerate
- calls: get_available_repair_books
- calls: get_likely_voices_for_book
- calls: len
- calls: load_chunks
- calls: str
## gradio_tabs.tab7_chunk_tools:load_chunks
- calls: ImportError
## gradio_tabs.tab7_chunk_tools:play_chunk_audio
- calls: ImportError
## gradio_tabs.tab7_chunk_tools:play_original_audio
- calls: Thread
- calls: exists
- calls: start
- calls: str
## gradio_tabs.tab7_chunk_tools:play_original_audio.play_audio
- calls: play_chunk_audio
- calls: print
- calls: str
## gradio_tabs.tab7_chunk_tools:play_revised_audio
- calls: Thread
- calls: exists
- calls: start
- calls: str
## gradio_tabs.tab7_chunk_tools:play_revised_audio.play_audio
- calls: play_chunk_audio
- calls: print
- calls: str
## gradio_tabs.tab7_chunk_tools:resynthesize_chunk_audio
- calls: Thread
- calls: start
- calls: str
- calls: strip
## gradio_tabs.tab7_chunk_tools:resynthesize_chunk_audio.resynth_worker
- calls: print
- calls: str
- calls: synthesize_chunk
## gradio_tabs.tab7_chunk_tools:save_chunk_changes
- calls: len
- calls: save_chunks
- calls: split
- calls: str
- calls: strip
## gradio_tabs.tab7_chunk_tools:save_chunks
- calls: ImportError
## gradio_tabs.tab7_chunk_tools:search_chunks
- calls: ImportError
## gradio_tabs.tab7_chunk_tools:search_for_chunks
- calls: append
- calls: len
- calls: search_chunks
- calls: str
- calls: strip
- calls: update
## gradio_tabs.tab7_chunk_tools:select_chunk_for_editing
- calls: get
- calls: int
- calls: split
- calls: str
## gradio_tabs.tab7_chunk_tools:synthesize_chunk
- calls: ImportError
## gradio_tabs.tab7_chunk_tools:update_chunk
- calls: ImportError
## gradio_tabs.tab8_json_generate:<module>
- calls: Blocks
- calls: create_json_generate_tab
- calls: launch
- calls: print
## gradio_tabs.tab8_json_generate:create_json_generate_tab
- calls: Button
- calls: Column
- calls: Dropdown
- calls: Markdown
- calls: Row
- calls: Slider
- calls: Textbox
- calls: change
- calls: click
- calls: get_available_json_files
- calls: get_available_voices
## gradio_tabs.tab8_json_generate:create_json_generate_tab.refresh_json_files
- calls: get_available_json_files
- calls: update
## gradio_tabs.tab8_json_generate:create_json_generate_tab.refresh_voice_list
- calls: get_available_voices
- calls: update
## gradio_tabs.tab8_json_generate:generate_audiobook_from_json
- calls: ImportError
## gradio_tabs.tab8_json_generate:get_available_json_files
- calls: Path
- calls: any
- calls: append
- calls: exists
- calls: glob
- calls: is_dir
- calls: iterdir
- calls: len
- calls: load
- calls: open
- calls: replace
- calls: sorted
- calls: str
## gradio_tabs.tab8_json_generate:get_available_voices
- calls: append
- calls: list_voice_samples
- calls: print
- calls: sorted
- calls: str
## gradio_tabs.tab8_json_generate:get_generation_status
- calls: get
## gradio_tabs.tab8_json_generate:list_voice_samples
- calls: ImportError
## gradio_tabs.tab8_json_generate:load_json_file_info
- calls: Path
- calls: exists
- calls: get
- calls: get_available_json_files
- calls: glob
- calls: int
- calls: len
- calls: list
- calls: load
- calls: open
- calls: split
- calls: str
- calls: sum
## gradio_tabs.tab8_json_generate:play_audio
- calls: Path
- calls: exists
- calls: get
- calls: isinstance
- calls: str
## gradio_tabs.tab8_json_generate:start_json_generation
- calls: Thread
- calls: get_available_json_files
- calls: get_available_voices
- calls: start
- calls: str
## gradio_tabs.tab8_json_generate:start_json_generation.generation_worker
- calls: generate_audiobook_from_json
- calls: str
## gradio_tabs.tab8_json_generate:stop_json_generation
- calls: get
## interface:<module>
- calls: ArgumentParser
- calls: add_argument
- calls: filterwarnings
- calls: flush
- calls: main
- calls: parse_known_args
- calls: print
- calls: resume_book_from_chunk
- calls: signal
## interface:main
- calls: Path
- calls: append
- calls: ensure_voice_sample_compatibility
- calls: enumerate
- calls: input
- calls: is_dir
- calls: isinstance
- calls: iterdir
- calls: len
- calls: list_voice_samples
- calls: log_console
- calls: lower
- calls: pipeline_book_processing
- calls: print
- calls: prompt_book_selection
- calls: prompt_tts_params
- calls: prompt_voice_selection
## interface:main_with_resume
- calls: input
- calls: int
- calls: main
- calls: print
- calls: resume_book_from_chunk
- calls: run_combine_only_mode
- calls: strip
## interface:pipeline_book_processing
- calls: append
- calls: enumerate
- calls: exists
- calls: get
- calls: get_best_available_device
- calls: len
- calls: print
- calls: print_exc
- calls: process_book_folder
## interface:prompt_book_selection
- calls: enumerate
- calls: input
- calls: int
- calls: isdigit
- calls: len
- calls: print
- calls: strip
## interface:prompt_tts_params
- calls: get_choice_input
- calls: get_float_input
- calls: get_system_profile
- calls: get_yes_no_input
- calls: len
- calls: list
- calls: print
- calls: print_system_summary
- calls: range
- calls: recommend_asr_models
- calls: upper
## interface:prompt_tts_params.get_choice_input
- calls: input
- calls: int
- calls: len
- calls: print
- calls: strip
## interface:prompt_tts_params.get_float_input
- calls: float
- calls: input
- calls: print
- calls: str
- calls: strip
## interface:prompt_tts_params.get_yes_no_input
- calls: input
- calls: lower
- calls: print
- calls: strip
## interface:prompt_voice_selection
- calls: enumerate
- calls: input
- calls: int
- calls: isdigit
- calls: len
- calls: print
- calls: strip
## interface:signal_handler
- calls: print
## launch:<module>
- calls: exit
- calls: main
## launch:main
- calls: Path
- calls: absolute
- calls: chdir
- calls: exists
- calls: print
- calls: run
- calls: str
## main_launcher:<module>
- calls: wrapper_main
## main_launcher:main_with_resume
- calls: input
- calls: int
- calls: main
- calls: print
- calls: resume_book_from_chunk
- calls: run_combine_only_mode
- calls: strip
## main_launcher:prepare_chunk_file
- calls: Path
- calls: enumerate
- calls: exists
- calls: generate_enriched_chunks
- calls: get_float_input
- calls: get_yes_no_input
- calls: glob
- calls: input
- calls: int
- calls: is_dir
- calls: iterdir
- calls: len
- calls: list
- calls: mkdir
- calls: print
- calls: strip
## main_launcher:prepare_chunk_file.get_float_input
- calls: float
- calls: input
- calls: print
- calls: strip
## main_launcher:prepare_chunk_file.get_yes_no_input
- calls: input
- calls: lower
- calls: print
- calls: strip
## main_launcher:prompt_menu
- calls: enumerate
- calls: input
- calls: int
- calls: isdigit
- calls: len
- calls: print
- calls: strip
## main_launcher:wrapper_main
- calls: generate_from_json_main
- calls: input
- calls: int
- calls: main
- calls: prepare_chunk_file
- calls: print
- calls: prompt_menu
- calls: resume_book_from_chunk
- calls: run_chunk_repair_tool
- calls: run_combine_only_mode
- calls: strip
- calls: test_chunking
## modules.advanced_optimizations:<module>
- calls: getLogger
## modules.advanced_optimizations:AdvancedOptimizer._enable_efficient_attention
- calls: append
- calls: enable_flash_sdp
- calls: enable_math_sdp
- calls: enable_mem_efficient_sdp
- calls: hasattr
- calls: info
- calls: lower
- calls: named_modules
- calls: warning
## modules.advanced_optimizations:AdvancedOptimizer._get_model_memory_usage
- calls: element_size
- calls: hasattr
- calls: numel
- calls: parameters
- calls: sum
## modules.advanced_optimizations:AdvancedOptimizer._set_memory_env_vars
- calls: info
- calls: items
## modules.advanced_optimizations:AdvancedOptimizer._test_compiled_method
- calls: cuda
- calls: info
- calls: is_available
- calls: randint
- calls: randn
- calls: warning
## modules.advanced_optimizations:AdvancedOptimizer.apply_advanced_int8_quantization
- calls: _get_model_memory_usage
- calls: dict
- calls: error
- calls: hasattr
- calls: info
- calls: isinstance
- calls: join
- calls: named_modules
- calls: quantize_dynamic
- calls: setattr
- calls: split
- calls: warning
## modules.advanced_optimizations:AdvancedOptimizer.apply_memory_optimizations
- calls: _enable_efficient_attention
- calls: _set_memory_env_vars
- calls: contiguous
- calls: error
- calls: gradient_checkpointing_enable
- calls: hasattr
- calls: info
- calls: is_available
- calls: is_contiguous
- calls: isinstance
- calls: named_modules
- calls: named_parameters
- calls: to
- calls: warning
## modules.advanced_optimizations:AdvancedOptimizer.apply_smart_torch_compile
- calls: _test_compiled_method
- calls: compile
- calls: error
- calls: hasattr
- calls: info
- calls: warning
## modules.advanced_optimizations:AdvancedOptimizer.diagnose_and_fix_torch_compile
- calls: append
- calls: info
- calls: len
- calls: run
- calls: split
## modules.advanced_optimizations:AdvancedOptimizer.revert_optimizations
- calls: clear
- calls: error
- calls: hasattr
- calls: info
- calls: items
## modules.advanced_optimizations:get_advanced_optimizer
- calls: AdvancedOptimizer
## modules.advanced_optimizations:optimize_model_advanced
- calls: append
- calls: apply_advanced_int8_quantization
- calls: apply_memory_optimizations
- calls: apply_smart_torch_compile
- calls: diagnose_and_fix_torch_compile
- calls: error
- calls: get_advanced_optimizer
- calls: info
- calls: join
## modules.advanced_optimizations:set_warmup_mode
- calls: info
## modules.asr_manager:<module>
- calls: cleanup_asr_model
- calls: get_asr_memory_info
- calls: load_asr_model_adaptive
- calls: print
## modules.asr_manager:calculate_available_vram_for_asr
- calls: get_real_time_vram_status
- calls: max
## modules.asr_manager:can_model_fit_gpu
- calls: get
## modules.asr_manager:cleanup_asr_model
- calls: empty_cache
- calls: is_available
- calls: print
- calls: warning
## modules.asr_manager:get_asr_memory_info
- calls: calculate_available_vram_for_asr
- calls: get_real_time_vram_status
## modules.asr_manager:get_real_time_vram_status
- calls: device_count
- calls: get_device_properties
- calls: is_available
- calls: memory_allocated
- calls: memory_reserved
- calls: warning
## modules.asr_manager:load_asr_model_adaptive
- calls: calculate_available_vram_for_asr
- calls: can_model_fit_gpu
- calls: get
- calls: get_real_time_vram_status
- calls: load_model
- calls: lower
- calls: print
- calls: try_load_model_with_fallback
- calls: upper
## modules.asr_manager:try_load_model_with_fallback
- calls: Exception
- calls: convert_device_name
- calls: load_model
- calls: print
- calls: str
- calls: upper
## modules.asr_manager:try_load_model_with_fallback.convert_device_name
- calls: lower
## modules.audio_processor:<module>
- calls: warning
## modules.audio_processor:add_chunk_end_silence
- calls: export
- calls: from_wav
- calls: info
- calls: silent
- calls: warning
## modules.audio_processor:add_contextual_silence
- calls: export
- calls: from_wav
- calls: info
- calls: silent
## modules.audio_processor:add_contextual_silence_memory
- calls: silent
## modules.audio_processor:adjust_parameters_for_retry
- calls: copy
- calls: max
- calls: min
## modules.audio_processor:apply_smart_fade
- calls: detect_end_artifact
- calls: fade_out_wav
- calls: find_end_of_speech
## modules.audio_processor:apply_smart_fade_memory
- calls: fade_out
## modules.audio_processor:calculate_text_similarity
- calls: intersection
- calls: len
- calls: normalize_text
- calls: set
## modules.audio_processor:calculate_text_similarity.normalize_text
- calls: lower
- calls: split
- calls: sub
## modules.audio_processor:check_audio_health
- calls: abs
- calls: len
- calls: mean
- calls: read
- calls: round
- calls: sqrt
- calls: str
## modules.audio_processor:detect_end_artifact
- calls: abs
- calls: diff
- calls: info
- calls: int
- calls: len
- calls: mean
- calls: read
- calls: rfft
- calls: rfftfreq
- calls: sign
- calls: sqrt
- calls: str
- calls: sum
## modules.audio_processor:detect_spectral_artifacts
- calls: abs
- calls: array
- calls: astype
- calls: debug
- calls: diff
- calls: error
- calls: get_array_of_samples
- calls: isinstance
- calls: len
- calls: max
- calls: mean
- calls: mfcc
- calls: min
- calls: read
- calls: reshape
- calls: str
- calls: var
## modules.audio_processor:detect_tts_hum_artifact
- calls: abs
- calls: info
- calls: len
- calls: mean
- calls: range
- calls: read
- calls: rfft
- calls: rfftfreq
- calls: sqrt
- calls: str
- calls: sum
## modules.audio_processor:evaluate_chunk_quality
- calls: append
- calls: check_audio_health
- calls: detect_spectral_artifacts
- calls: isinstance
- calls: len
- calls: sum
- calls: validate_output_matches_input
## modules.audio_processor:fade_out_wav
- calls: int
- calls: len
- calls: linspace
- calls: read
- calls: str
- calls: write
## modules.audio_processor:find_end_of_speech
- calls: get
- calls: getLogger
- calls: get_speech_timestamps
- calls: int
- calls: items
- calls: load
- calls: pop
- calls: read_audio
- calls: setLevel
- calls: str
## modules.audio_processor:get_chunk_audio_duration
- calls: get_wav_duration
- calls: len
- calls: read
- calls: str
## modules.audio_processor:get_wav_duration
- calls: float
- calls: getframerate
- calls: getnframes
- calls: open
- calls: str
## modules.audio_processor:handle_problematic_chunks
- calls: mkdir
- calls: move
- calls: str
- calls: warning
## modules.audio_processor:has_mid_energy_drop
- calls: enumerate
- calls: int
- calls: len
- calls: max
- calls: mean
- calls: numpy
- calls: range
- calls: sqrt
- calls: squeeze
## modules.audio_processor:pause_for_chunk_review
- calls: any
- calls: error
- calls: glob
- calls: input
- calls: iterdir
- calls: len
- calls: list
- calls: move
- calls: print
- calls: rmdir
- calls: str
- calls: strip
- calls: sub
## modules.audio_processor:process_audio_with_trimming_and_silence
- calls: add_contextual_silence_memory
- calls: trim_audio_endpoint
## modules.audio_processor:smart_audio_validation
- calls: check_audio_health
- calls: detect_tts_hum_artifact
- calls: handle_problematic_chunks
## modules.audio_processor:smart_fade_out
- calls: detect_silence
- calls: export
- calls: fade_out
- calls: from_wav
- calls: get_array_of_samples
- calls: info
- calls: len
- calls: max
## modules.audio_processor:trim_audio_endpoint
- calls: append
- calls: array
- calls: astype
- calls: get_array_of_samples
- calls: int
- calls: len
- calls: max
- calls: mean
- calls: min
- calls: range
- calls: reshape
- calls: sqrt
## modules.audio_processor:validate_output_matches_input
- calls: NamedTemporaryFile
- calls: calculate_text_similarity
- calls: error
- calls: export
- calls: get
- calls: isinstance
- calls: load_asr_model_adaptive
- calls: str
- calls: strip
- calls: transcribe
- calls: unlink
- calls: warning
## modules.bandwidth_monitor:RealTimeBandwidthMonitor.__init__
- calls: Queue
## modules.bandwidth_monitor:RealTimeBandwidthMonitor._analyze_bandwidth_data
- calls: len
- calls: max
- calls: min
- calls: sum
## modules.bandwidth_monitor:RealTimeBandwidthMonitor._get_bandwidth_sample
- calls: float
- calls: len
- calls: run
- calls: split
- calls: strip
## modules.bandwidth_monitor:RealTimeBandwidthMonitor._monitor_loop
- calls: _get_bandwidth_sample
- calls: get
- calls: print
- calls: put
- calls: sleep
- calls: time
## modules.bandwidth_monitor:RealTimeBandwidthMonitor.start_monitoring
- calls: Thread
- calls: print
- calls: start
## modules.bandwidth_monitor:RealTimeBandwidthMonitor.stop_monitoring
- calls: _analyze_bandwidth_data
- calls: append
- calls: empty
- calls: get_nowait
- calls: join
## modules.bandwidth_monitor:TTSBandwidthProfiler.__init__
- calls: RealTimeBandwidthMonitor
## modules.bandwidth_monitor:TTSBandwidthProfiler._print_bandwidth_report
- calls: print
## modules.bandwidth_monitor:TTSBandwidthProfiler.profile_tts_generation
- calls: _print_bandwidth_report
- calls: generate
- calls: len
- calls: print
- calls: sleep
- calls: start_monitoring
- calls: stop_monitoring
- calls: time
## modules.bandwidth_monitor:monitor_tts_bandwidth
- calls: TTSBandwidthProfiler
- calls: append
- calls: enumerate
- calls: len
- calls: print
- calls: profile_tts_generation
- calls: sleep
## modules.batch_processor:<module>
- calls: ArgumentParser
- calls: Path
- calls: add_argument
- calls: append
- calls: get
- calls: load
- calls: open
- calls: parse_args
- calls: process_single_batch
## modules.cuda_optimizer:<module>
- calls: getLogger
## modules.cuda_optimizer:CudaOptimizer.__init__
- calls: _setup_cuda_streams
## modules.cuda_optimizer:CudaOptimizer._enable_kernel_fusion
- calls: append
- calls: hasattr
- calls: set_fusion_strategy
- calls: warning
## modules.cuda_optimizer:CudaOptimizer._optimize_cuda_settings
- calls: append
- calls: hasattr
- calls: warning
## modules.cuda_optimizer:CudaOptimizer._optimize_memory_allocator
- calls: append
- calls: get_device_properties
- calls: hasattr
- calls: is_available
- calls: set_per_process_memory_fraction
- calls: warning
## modules.cuda_optimizer:CudaOptimizer._optimize_tensor_operations
- calls: append
- calls: hasattr
- calls: set_num_threads
- calls: warning
## modules.cuda_optimizer:CudaOptimizer._setup_cuda_streams
- calls: Stream
- calls: info
- calls: is_available
- calls: warning
## modules.cuda_optimizer:CudaOptimizer.apply_cuda_optimizations
- calls: _enable_kernel_fusion
- calls: _optimize_cuda_settings
- calls: _optimize_memory_allocator
- calls: _optimize_tensor_operations
- calls: error
- calls: extend
- calls: is_available
## modules.cuda_optimizer:CudaOptimizer.async_batch_inference
- calls: batch_fn
- calls: stream
- calls: warning
## modules.cuda_optimizer:CudaOptimizer.clear_memory_efficiently
- calls: collect
- calls: empty_cache
- calls: is_available
- calls: synchronize
- calls: warning
## modules.cuda_optimizer:CudaOptimizer.create_optimized_tensor
- calls: empty
- calls: optimize_tensor_memory_layout
- calls: startswith
- calls: warning
## modules.cuda_optimizer:CudaOptimizer.fused_attention_with_cache
- calls: cat
- calls: hasattr
- calls: matmul
- calls: scaled_dot_product_attention
- calls: size
- calls: softmax
- calls: transpose
- calls: warning
## modules.cuda_optimizer:CudaOptimizer.get_optimization_summary
- calls: is_available
- calls: len
## modules.cuda_optimizer:CudaOptimizer.get_preallocated_tensor
- calls: clone
- calls: create_optimized_tensor
## modules.cuda_optimizer:CudaOptimizer.optimize_batch_processing
- calls: get_device_properties
- calls: int
- calls: is_available
- calls: max
- calls: memory_allocated
- calls: min
- calls: warning
## modules.cuda_optimizer:CudaOptimizer.optimize_tensor_memory_layout
- calls: contiguous
- calls: dim
- calls: is_contiguous
- calls: to
- calls: warning
## modules.cuda_optimizer:CudaOptimizer.pipeline_batch_processing
- calls: append
- calls: cuda
- calls: hasattr
- calls: len
- calls: model_fn
- calls: range
- calls: stream
- calls: synchronize
- calls: values
- calls: warning
## modules.cuda_optimizer:CudaOptimizer.preallocate_batch_tensors
- calls: contiguous
- calls: empty
- calls: info
- calls: len
- calls: str
- calls: to
- calls: warning
## modules.cuda_optimizer:CudaOptimizer.restore_original_settings
- calls: items
- calls: warning
## modules.cuda_optimizer:create_cuda_optimizer
- calls: CudaOptimizer
- calls: apply_cuda_optimizations
- calls: info
- calls: len
## modules.dual_model_optimizer:<module>
- calls: test_dual_model_optimization
## modules.dual_model_optimizer:DualModelParallelOptimizer.__init__
- calls: ThreadPoolExecutor
## modules.dual_model_optimizer:DualModelParallelOptimizer._generate_single_threaded
- calls: generate
- calls: no_grad
- calls: print
## modules.dual_model_optimizer:DualModelParallelOptimizer.benchmark_dual_vs_single
- calls: _generate_single_threaded
- calls: append
- calls: extend
- calls: generate_parallel_pair
- calls: len
- calls: locals
- calls: print
- calls: synchronize
- calls: time
## modules.dual_model_optimizer:DualModelParallelOptimizer.cleanup
- calls: empty_cache
- calls: print
- calls: shutdown
## modules.dual_model_optimizer:DualModelParallelOptimizer.generate_parallel_pair
- calls: result
- calls: submit
## modules.dual_model_optimizer:DualModelParallelOptimizer.load_dual_models
- calls: Path
- calls: _load_single_model
- calls: collect
- calls: empty_cache
- calls: get_device_properties
- calls: insert
- calls: isinstance
- calls: len
- calls: memory_allocated
- calls: memory_reserved
- calls: optimize_chatterbox_model
- calls: print
- calls: str
- calls: synchronize
## modules.dual_model_optimizer:DualModelParallelOptimizer.load_dual_models._load_single_model
- calls: Path
- calls: exists
- calls: from_local
- calls: from_pretrained
- calls: print
- calls: strip
## modules.dual_model_optimizer:DualModelParallelOptimizer.process_chunks_parallel
- calls: _generate_single_threaded
- calls: append
- calls: extend
- calls: generate_parallel_pair
- calls: len
- calls: print
- calls: range
- calls: time
## modules.dual_model_optimizer:test_dual_model_optimization
- calls: DualModelParallelOptimizer
- calls: benchmark_dual_vs_single
- calls: cleanup
- calls: load_dual_models
- calls: print
## modules.dual_t3_engine:<module>
- calls: getLogger
## modules.dual_t3_engine:DualT3Coordinator.__init__
- calls: Queue
- calls: S3GenWorker
- calls: Stream
- calls: T3Worker
- calls: info
## modules.dual_t3_engine:DualT3Coordinator._dispatch_chunks
- calls: WorkItem
- calls: debug
- calls: full
- calls: get
- calls: put
- calls: sleep
- calls: time
## modules.dual_t3_engine:DualT3Coordinator._print_statistics
- calls: info
- calls: len
- calls: sum
## modules.dual_t3_engine:DualT3Coordinator.process_chunks
- calls: Thread
- calls: _print_statistics
- calls: append
- calls: get
- calls: info
- calls: join
- calls: len
- calls: sort
- calls: start
- calls: stop
- calls: time
- calls: warning
## modules.dual_t3_engine:DualT3Coordinator.start
- calls: info
- calls: start
## modules.dual_t3_engine:DualT3Coordinator.stop
- calls: info
- calls: join
- calls: stop
## modules.dual_t3_engine:S3GenWorker.__init__
- calls: __init__
- calls: info
- calls: super
## modules.dual_t3_engine:S3GenWorker._process_tokens
- calls: AudioResult
- calls: cpu
- calls: error
- calls: inference
- calls: numpy
- calls: stream
- calls: synchronize
- calls: time
## modules.dual_t3_engine:S3GenWorker.run
- calls: _process_tokens
- calls: debug
- calls: empty
- calls: error
- calls: get
- calls: info
- calls: put
- calls: time
- calls: warning
## modules.dual_t3_engine:TTSWorker.__init__
- calls: __init__
- calls: float
- calls: info
- calls: super
## modules.dual_t3_engine:TTSWorker._process_chunk
- calls: AudioResult
- calls: TokenResult
- calls: dim
- calls: empty_cache
- calls: error
- calls: generate
- calls: hasattr
- calls: inference
- calls: len
- calls: str
- calls: stream
- calls: synchronize
- calls: time
## modules.dual_t3_engine:TTSWorker.run
- calls: _process_chunk
- calls: debug
- calls: error
- calls: get
- calls: info
- calls: put
- calls: time
## modules.dual_t3_engine:load_dual_t3_models
- calls: Path
- calls: empty_cache
- calls: error
- calls: from_local
- calls: info
- calls: memory_allocated
- calls: memory_reserved
- calls: str
- calls: warning
## modules.dual_tts_engine:<module>
- calls: getLogger
## modules.dual_tts_engine:DualTTSCoordinator.__init__
- calls: Queue
- calls: Stream
- calls: TTSWorker
- calls: info
## modules.dual_tts_engine:DualTTSCoordinator._dispatch_chunks
- calls: WorkItem
- calls: debug
- calls: full
- calls: get
- calls: put
- calls: sleep
## modules.dual_tts_engine:DualTTSCoordinator._print_statistics
- calls: info
- calls: len
- calls: sum
- calls: warning
## modules.dual_tts_engine:DualTTSCoordinator.process_chunks
- calls: Thread
- calls: _print_statistics
- calls: append
- calls: get
- calls: info
- calls: join
- calls: len
- calls: sort
- calls: start
- calls: stop
- calls: time
- calls: warning
## modules.dual_tts_engine:DualTTSCoordinator.start
- calls: info
- calls: start
## modules.dual_tts_engine:DualTTSCoordinator.stop
- calls: info
- calls: join
- calls: stop
## modules.dual_tts_engine:TTSWorker.__init__
- calls: __init__
- calls: info
- calls: super
## modules.dual_tts_engine:TTSWorker._process_chunk
- calls: AudioResult
- calls: cpu
- calls: detach
- calls: drop_invalid_tokens
- calls: empty_cache
- calls: error
- calls: from_numpy
- calls: generate
- calls: get
- calls: inference
- calls: inference_mode
- calls: numpy
- calls: pad
- calls: punc_norm
- calls: squeeze
- calls: str
- calls: stream
- calls: synchronize
- calls: text_to_tokens
- calls: time
- calls: to
- calls: unsqueeze
## modules.dual_tts_engine:TTSWorker.run
- calls: _process_chunk
- calls: error
- calls: get
- calls: info
- calls: put
- calls: time
## modules.dual_tts_engine:load_dual_tts_models
- calls: Path
- calls: empty_cache
- calls: error
- calls: from_local
- calls: info
- calls: memory_allocated
- calls: memory_reserved
- calls: str
- calls: warning
## modules.file_manager:add_metadata_to_m4b
- calls: FileNotFoundError
- calls: append
- calls: exists
- calls: extend
- calls: ffmpeg_error_message
- calls: is_ffmpeg_available
- calls: open
- calls: print
- calls: run_ffmpeg
- calls: split
- calls: str
- calls: strip
- calls: unlink
## modules.file_manager:apply_batch_binning
- calls: abs
- calls: add
- calls: append
- calls: copy
- calls: get
- calls: items
- calls: len
- calls: print
- calls: round
- calls: set
- calls: sum
- calls: values
## modules.file_manager:chunk_sort_key
- calls: group
- calls: int
- calls: match
## modules.file_manager:cleanup_temp_files
- calls: glob
- calls: unlink
## modules.file_manager:combine_audio_chunks
- calls: FileNotFoundError
- calls: RuntimeError
- calls: append
- calls: create_concat_file
- calls: error
- calls: exists
- calls: info
- calls: len
- calls: mkdir
- calls: open
- calls: read
- calls: resolve
- calls: run_ffmpeg
- calls: str
## modules.file_manager:convert_to_m4b
- calls: FileNotFoundError
- calls: Popen
- calls: convert_to_m4b_with_loudness_normalization
- calls: convert_to_m4b_with_peak_normalization
- calls: convert_to_m4b_with_simple_normalization
- calls: ffmpeg_error_message
- calls: group
- calls: groups
- calls: is_ffmpeg_available
- calls: map
- calls: print
- calls: search
- calls: str
- calls: time
- calls: wait
## modules.file_manager:convert_to_m4b_with_loudness_normalization
- calls: FileNotFoundError
- calls: Popen
- calls: append
- calls: convert_to_m4b_with_peak_normalization
- calls: ffmpeg_error_message
- calls: group
- calls: groups
- calls: is_ffmpeg_available
- calls: join
- calls: loads
- calls: map
- calls: print
- calls: run
- calls: search
- calls: split
- calls: startswith
- calls: str
- calls: strip
- calls: time
- calls: wait
## modules.file_manager:convert_to_m4b_with_peak_normalization
- calls: FileNotFoundError
- calls: Popen
- calls: append
- calls: ffmpeg_error_message
- calls: group
- calls: groups
- calls: is_ffmpeg_available
- calls: join
- calls: map
- calls: print
- calls: search
- calls: str
- calls: time
- calls: wait
## modules.file_manager:convert_to_m4b_with_simple_normalization
- calls: FileNotFoundError
- calls: Popen
- calls: append
- calls: ffmpeg_error_message
- calls: group
- calls: groups
- calls: is_ffmpeg_available
- calls: join
- calls: map
- calls: print
- calls: search
- calls: str
- calls: time
- calls: wait
## modules.file_manager:create_concat_file
- calls: info
- calls: len
- calls: open
- calls: replace
- calls: resolve
- calls: str
- calls: write
## modules.file_manager:ensure_voice_sample_compatibility
- calls: basename
- calls: dirname
- calls: info
- calls: join
- calls: lower
- calls: run
- calls: splitext
- calls: str
## modules.file_manager:export_processing_log
- calls: items
- calls: open
- calls: write
## modules.file_manager:find_book_files
- calls: exists
- calls: glob
- calls: sorted
## modules.file_manager:get_audio_files_in_directory
- calls: fullmatch
- calls: glob
- calls: sorted
## modules.file_manager:is_ffmpeg_available
- calls: run
## modules.file_manager:list_voice_samples
- calls: glob
- calls: lower
- calls: sorted
## modules.file_manager:load_chunk_info
- calls: exists
- calls: load
- calls: open
- calls: warning
## modules.file_manager:run_ffmpeg
- calls: RuntimeError
- calls: error
- calls: join
- calls: run
## modules.file_manager:sanitize_filename
- calls: strip
- calls: sub
## modules.file_manager:save_chunk_info
- calls: apply_batch_binning
- calls: dump
- calls: open
## modules.file_manager:setup_book_directories
- calls: info
- calls: mkdir
- calls: sanitize_filename
## modules.file_manager:verify_audio_file
- calls: error
- calls: info
- calls: str
## modules.file_manager:verify_chunk_completeness
- calls: append
- calls: exists
- calls: range
- calls: verify_audio_file
## modules.gpu_bandwidth_monitor:<module>
- calls: getLogger
## modules.gpu_bandwidth_monitor:GPUBandwidthMonitor.__init__
- calls: Lock
- calls: __init__
- calls: super
## modules.gpu_bandwidth_monitor:GPUBandwidthMonitor._sample_gpu
- calls: GPUSample
- calls: float
- calls: int
- calls: len
- calls: run
- calls: split
- calls: strip
- calls: time
## modules.gpu_bandwidth_monitor:GPUBandwidthMonitor.get_statistics
- calls: len
- calls: max
- calls: min
- calls: sum
## modules.gpu_bandwidth_monitor:GPUBandwidthMonitor.print_report
- calls: get_statistics
- calls: print
- calls: warning
## modules.gpu_bandwidth_monitor:GPUBandwidthMonitor.run
- calls: _sample_gpu
- calls: append
- calls: debug
- calls: info
- calls: sleep
## modules.gui_json_generator:<module>
- calls: Path
- calls: append
- calls: print
- calls: str
## modules.gui_json_generator:generate_audiobook_from_json
- calls: Exception
- calls: Path
- calls: ThreadPoolExecutor
- calls: ValueError
- calls: all
- calls: append
- calls: as_completed
- calls: combine_audio_for_book
- calls: endswith
- calls: ensure_voice_sample_compatibility
- calls: enumerate
- calls: exists
- calls: get
- calls: glob
- calls: index
- calls: int
- calls: is_available
- calls: isinstance
- calls: len
- calls: list_voice_samples
- calls: load_chunks
- calls: load_optimized_model
- calls: log_chunk_progress
- calls: mkdir
- calls: prewarm_model_with_voice
- calls: print
- calls: replace
- calls: result
- calls: str
- calls: submit
- calls: time
- calls: timedelta
- calls: unlink
## modules.gui_json_generator:get_book_name_from_json_path
- calls: Path
- calls: endswith
- calls: index
- calls: len
- calls: replace
## modules.onnx_optimizer:T3ONNXOptimizer._initialize_onnx_session
- calls: InferenceSession
- calls: SessionOptions
- calls: get_providers
- calls: print
## modules.onnx_optimizer:T3ONNXOptimizer._optimize_onnx_graph
- calls: load
- calls: optimize_model
- calls: print
- calls: replace
- calls: save_model_to_file
## modules.onnx_optimizer:T3ONNXOptimizer.benchmark_onnx_vs_pytorch
- calls: inference
- calls: no_grad
- calls: onnx_inference
- calls: print
- calls: randint
- calls: randn
- calls: range
- calls: synchronize
- calls: time
- calls: to
## modules.onnx_optimizer:T3ONNXOptimizer.convert_t3_to_onnx
- calls: T3InferenceWrapper
- calls: _initialize_onnx_session
- calls: _optimize_onnx_graph
- calls: eval
- calls: export
- calls: join
- calls: mkdtemp
- calls: print
- calls: randint
- calls: randn
- calls: to
## modules.onnx_optimizer:T3ONNXOptimizer.convert_t3_to_onnx.T3InferenceWrapper.__init__
- calls: __init__
- calls: super
## modules.onnx_optimizer:T3ONNXOptimizer.convert_t3_to_onnx.T3InferenceWrapper.forward
- calls: inference
## modules.onnx_optimizer:T3ONNXOptimizer.onnx_inference
- calls: array
- calls: astype
- calls: cpu
- calls: from_numpy
- calls: numpy
- calls: print
- calls: run
- calls: to
## modules.onnx_optimizer:optimize_model_with_onnx
- calls: T3ONNXOptimizer
- calls: benchmark_onnx_vs_pytorch
- calls: convert_t3_to_onnx
- calls: print
## modules.onnx_optimizer:optimize_model_with_onnx.onnx_wrapped_inference
- calls: onnx_inference
- calls: original_inference
## modules.path_validator:check_existing_audiobook_paths
- calls: append
- calls: detect_problematic_characters
- calls: exists
- calls: is_dir
- calls: iterdir
- calls: join
- calls: suggest_safe_path
## modules.path_validator:detect_problematic_characters
- calls: append
- calls: items
- calls: search
## modules.path_validator:format_path_warning_html
- calls: detect_problematic_characters
- calls: validate_book_path
## modules.path_validator:format_path_warning_text
- calls: validate_book_path
## modules.path_validator:suggest_safe_path
- calls: sanitize_filename
## modules.path_validator:validate_and_create_audiobook_path
- calls: validate_book_path
## modules.path_validator:validate_book_path
- calls: detect_problematic_characters
- calls: join
- calls: suggest_safe_path
## modules.progress_tracker:PerformanceTracker.__init__
- calls: time
## modules.progress_tracker:PerformanceTracker.get_performance_summary
- calls: len
- calls: max
- calls: sum
- calls: time
## modules.progress_tracker:PerformanceTracker.log_batch_completion
- calls: append
- calls: len
- calls: sum
## modules.progress_tracker:PerformanceTracker.log_chunk_completion
- calls: append
- calls: monitor_vram_usage
- calls: sum
- calls: time
## modules.progress_tracker:create_status_line
- calls: int
- calls: str
- calls: timedelta
## modules.progress_tracker:display_batch_progress
- calls: print
## modules.progress_tracker:display_final_summary
- calls: int
- calls: print
- calls: timedelta
## modules.progress_tracker:display_system_info
- calls: get_device_name
- calls: get_device_properties
- calls: is_available
- calls: print
## modules.progress_tracker:export_performance_report
- calls: int
- calls: open
- calls: timedelta
- calls: write
## modules.progress_tracker:log_chunk_progress
- calls: _status_callback
- calls: flush
- calls: fmt
- calls: get_reload_manager
- calls: get_running_avg_its
- calls: get_statistics
- calls: hasattr
- calls: info
- calls: monitor_vram_usage
- calls: print
- calls: time
## modules.progress_tracker:log_chunk_progress.fmt
- calls: int
- calls: str
- calls: timedelta
## modules.progress_tracker:log_console
- calls: get
- calls: info
- calls: print
## modules.progress_tracker:log_processing_error
- calls: error
- calls: print
- calls: strftime
## modules.progress_tracker:log_processing_warning
- calls: print
- calls: strftime
- calls: warning
## modules.progress_tracker:log_run
- calls: open
- calls: write
## modules.progress_tracker:monitor_gpu_utilization
- calls: nvmlDeviceGetHandleByIndex
- calls: nvmlDeviceGetTemperature
- calls: nvmlDeviceGetUtilizationRates
- calls: nvmlInit
## modules.progress_tracker:monitor_vram_usage
- calls: is_available
- calls: memory_allocated
- calls: memory_reserved
- calls: optimize_memory_if_needed
- calls: warning
## modules.progress_tracker:optimize_memory_if_needed
- calls: collect
- calls: empty_cache
- calls: ipc_collect
- calls: is_available
- calls: optimize_cuda_memory_usage
## modules.progress_tracker:setup_logging
- calls: Formatter
- calls: StreamHandler
- calls: addHandler
- calls: basicConfig
- calls: close
- calls: getLogger
- calls: open
- calls: setFormatter
- calls: setLevel
- calls: str
## modules.progress_tracker:update_status_line
- calls: print
## modules.real_tts_optimizer:RealTTSOptimizer.__init__
- calls: getLogger
## modules.real_tts_optimizer:RealTTSOptimizer._apply_torch_compile
- calls: compile
- calls: hasattr
- calls: print
## modules.real_tts_optimizer:RealTTSOptimizer._optimize_cuda_settings
- calls: is_available
## modules.real_tts_optimizer:RealTTSOptimizer._optimize_s3gen_inference
- calls: hasattr
## modules.real_tts_optimizer:RealTTSOptimizer._optimize_s3gen_inference.optimized_s3gen_inference
- calls: autocast
## modules.real_tts_optimizer:RealTTSOptimizer._optimize_t3_inference
- calls: hasattr
## modules.real_tts_optimizer:RealTTSOptimizer._optimize_t3_inference.optimized_t3_inference
- calls: autocast
## modules.real_tts_optimizer:RealTTSOptimizer.apply_optimizations
- calls: _apply_torch_compile
- calls: _optimize_cuda_settings
- calls: _optimize_s3gen_inference
- calls: _optimize_t3_inference
- calls: append
- calls: dir
- calls: format_exc
- calls: get_device_name
- calls: hasattr
- calls: is_available
- calls: join
- calls: print
- calls: startswith
- calls: type
## modules.real_tts_optimizer:RealTTSOptimizer.fp32_fallback_mode
- calls: print
## modules.real_tts_optimizer:RealTTSOptimizer.restore_original_methods
- calls: hasattr
- calls: print
## modules.real_tts_optimizer:get_tts_optimizer
- calls: RealTTSOptimizer
## modules.real_tts_optimizer:optimize_chatterbox_model
- calls: apply_optimizations
- calls: get_tts_optimizer
## modules.real_tts_optimizer:optimized_inference
- calls: apply_optimizations
- calls: get_tts_optimizer
- calls: print
- calls: restore_original_methods
## modules.resume_handler:analyze_existing_chunks
- calls: append
- calls: exists
- calls: get_audio_files_in_directory
- calls: group
- calls: int
- calls: len
- calls: match
- calls: max
- calls: print
- calls: range
- calls: sort
## modules.resume_handler:auto_resume_incomplete
- calls: enumerate
- calls: find_incomplete_books
- calls: input
- calls: int
- calls: len
- calls: lower
- calls: print
- calls: resume_book_from_chunk
- calls: strip
## modules.resume_handler:find_incomplete_books
- calls: analyze_existing_chunks
- calls: append
- calls: exists
- calls: glob
- calls: is_dir
- calls: iterdir
- calls: len
- calls: list
## modules.resume_handler:process_book_folder_resume
- calls: ThreadPoolExecutor
- calls: add_metadata_to_m4b
- calls: append
- calls: as_completed
- calls: cleanup_asr_model
- calls: collect
- calls: combine_audio_chunks
- calls: convert_to_m4b
- calls: detect_deployment_environment
- calls: empty_cache
- calls: enable_gpu_persistence_mode
- calls: ensure_voice_sample_compatibility
- calls: enumerate
- calls: error
- calls: exists
- calls: extend
- calls: find_book_files
- calls: find_chunks_json_file
- calls: get
- calls: get_chunk_audio_duration
- calls: get_optimal_workers
- calls: info
- calls: int
- calls: is_dir
- calls: isinstance
- calls: join
- calls: len
- calls: load_asr_model_adaptive
- calls: load_chunks
- calls: load_optimized_model
- calls: log_chunk_progress
- calls: log_run
- calls: min
- calls: mkdir
- calls: pause_for_chunk_review
- calls: prewarm_model_with_voice
- calls: print
- calls: process_chunks_with_pipeline
- calls: range
- calls: result
- calls: rmtree
- calls: setup_book_directories
- calls: setup_logging
- calls: sleep
- calls: str
- calls: strftime
- calls: submit
- calls: sum
- calls: time
- calls: timedelta
- calls: validate_resume_point
- calls: warning
## modules.resume_handler:resume_book_from_chunk
- calls: Path
- calls: analyze_existing_chunks
- calls: dict
- calls: enumerate
- calls: exists
- calls: get_best_available_device
- calls: input
- calls: int
- calls: is_dir
- calls: iterdir
- calls: len
- calls: list_voice_samples
- calls: print
- calls: process_book_folder_resume
- calls: prompt_float
- calls: sorted
- calls: strip
- calls: suggest_resume_point
## modules.resume_handler:resume_book_from_chunk.prompt_float
- calls: float
- calls: input
- calls: strip
## modules.resume_handler:suggest_resume_point
- calls: min
- calls: print
## modules.resume_handler:validate_resume_point
- calls: print
## modules.sequence_batch_processor:<module>
- calls: getLogger
## modules.sequence_batch_processor:SequenceBatchProcessor.__init__
- calls: getLogger
## modules.sequence_batch_processor:SequenceBatchProcessor._create_parameter_signature
- calls: get
- calls: round
## modules.sequence_batch_processor:SequenceBatchProcessor._generate_recommendations
- calls: append
- calls: len
- calls: sum
## modules.sequence_batch_processor:SequenceBatchProcessor._group_by_parameters
- calls: _create_parameter_signature
- calls: append
- calls: defaultdict
- calls: enumerate
- calls: get
- calls: list
- calls: sort
- calls: values
## modules.sequence_batch_processor:SequenceBatchProcessor._log_performance_summary
- calls: info
## modules.sequence_batch_processor:SequenceBatchProcessor._process_chunk_batch
- calls: _process_individual_chunk
- calls: error
- calls: generate_batch
- calls: get
- calls: info
- calls: len
- calls: time
- calls: zip
## modules.sequence_batch_processor:SequenceBatchProcessor._process_individual_chunk
- calls: error
- calls: generate
- calls: get
- calls: info
- calls: time
- calls: zeros
## modules.sequence_batch_processor:SequenceBatchProcessor._process_parameter_group
- calls: _process_chunk_batch
- calls: _process_individual_chunk
- calls: len
- calls: range
## modules.sequence_batch_processor:SequenceBatchProcessor.analyze_batching_potential
- calls: _generate_recommendations
- calls: _group_by_parameters
- calls: len
- calls: sum
## modules.sequence_batch_processor:SequenceBatchProcessor.process_chunks_with_sequence_batching
- calls: _group_by_parameters
- calls: _log_performance_summary
- calls: _process_parameter_group
- calls: enumerate
- calls: get
- calls: info
- calls: len
- calls: time
## modules.sequence_batch_processor:create_sequence_batch_processor
- calls: SequenceBatchProcessor
- calls: info
## modules.simple_token_logger:init_token_log
- calls: exists
- calls: makedirs
- calls: now
- calls: open
- calls: strftime
- calls: write
## modules.simple_token_logger:log_chunk
- calls: open
- calls: write
## modules.system_detector:<module>
- calls: Path
- calls: get_system_profile
- calls: insert
- calls: items
- calls: print
- calls: print_system_summary
- calls: recommend_asr_models
- calls: str
- calls: upper
## modules.system_detector:get_cpu_cores
- calls: cpu_count
## modules.system_detector:get_gpu_memory
- calls: device_count
- calls: get_device_properties
- calls: is_available
- calls: memory_allocated
## modules.system_detector:get_safe_asr_models
- calls: append
- calls: items
## modules.system_detector:get_safe_cpu_models
- calls: append
- calls: items
## modules.system_detector:get_system_memory
- calls: virtual_memory
## modules.system_detector:get_system_profile
- calls: estimate_tts_vram_usage
- calls: get_cpu_cores
- calls: get_gpu_memory
- calls: get_system_memory
- calls: max
## modules.system_detector:print_system_summary
- calls: categorize_system
- calls: print
## modules.system_detector:recommend_asr_models
- calls: categorize_system
- calls: get_safe_asr_models
- calls: get_safe_cpu_models
- calls: index
- calls: len
- calls: max
- calls: range
- calls: reversed
## modules.t3_minimal_export:<module>
- calls: Path
- calls: export_t3_minimal
- calls: insert
- calls: str
## modules.t3_minimal_export:create_working_t3_cond
- calls: T3Cond
- calls: size
## modules.t3_minimal_export:export_t3_minimal
- calls: InferenceSession
- calls: Path
- calls: T3WorkingWrapper
- calls: astype
- calls: collect
- calls: cpu
- calls: empty_cache
- calls: encode
- calls: export
- calls: is_available
- calls: load_t3_minimal
- calls: mkdir
- calls: numpy
- calls: print
- calls: print_exc
- calls: randn
- calls: run
- calls: tensor
- calls: unsqueeze
- calls: wrapper
## modules.t3_minimal_export:export_t3_minimal.T3WorkingWrapper.__init__
- calls: __init__
- calls: super
## modules.t3_minimal_export:export_t3_minimal.T3WorkingWrapper.forward
- calls: create_working_t3_cond
- calls: full
- calls: no_grad
- calls: ones
- calls: size
- calls: t3
- calls: zeros
## modules.t3_standalone_export:<module>
- calls: Path
- calls: export_t3_standalone
- calls: getLogger
- calls: insert
- calls: str
## modules.t3_standalone_export:create_minimal_t3_wrapper
- calls: T3MinimalWrapper
## modules.t3_standalone_export:create_minimal_t3_wrapper.T3MinimalWrapper.__init__
- calls: __init__
- calls: super
## modules.t3_standalone_export:create_minimal_t3_wrapper.T3MinimalWrapper.forward
- calls: T3Cond
- calls: full
- calls: hasattr
- calls: no_grad
- calls: ones
- calls: size
- calls: t3
- calls: zeros
## modules.t3_standalone_export:export_t3_standalone
- calls: InferenceSession
- calls: Path
- calls: abs
- calls: astype
- calls: collect
- calls: cpu
- calls: create_minimal_t3_wrapper
- calls: empty_cache
- calls: encode
- calls: export
- calls: get_available_providers
- calls: insert
- calls: is_available
- calls: load_t3_minimal
- calls: max
- calls: min
- calls: mkdir
- calls: numpy
- calls: print
- calls: print_exc
- calls: randn
- calls: run
- calls: stat
- calls: tensor
- calls: unsqueeze
- calls: wrapper
## modules.t3_standalone_export:find_cached_model_files
- calls: FileNotFoundError
- calls: expanduser
- calls: get
- calls: glob
- calls: join
- calls: max
## modules.t3_standalone_export:load_t3_minimal
- calls: EnTokenizer
- calls: Path
- calls: T3
- calls: collect
- calls: empty_cache
- calls: error
- calls: eval
- calls: find_cached_model_files
- calls: get_tensor
- calls: is_available
- calls: isinstance
- calls: keys
- calls: load_state_dict
- calls: max_memory_allocated
- calls: memory_allocated
- calls: print
- calls: print_exc
- calls: reset_peak_memory_stats
- calls: safe_open
- calls: to
## modules.terminal_logger:TerminalLogger.__init__
- calls: Lock
- calls: Path
- calls: resolve
## modules.terminal_logger:TerminalLogger._emit_chunk_summary
- calls: float
- calls: flush
- calls: open
- calls: str
- calls: write
## modules.terminal_logger:TerminalLogger.emit_chunk_summary
- calls: _emit_chunk_summary
## modules.terminal_logger:TerminalLogger.flush
- calls: flush
## modules.terminal_logger:TerminalLogger.set_batch_size
- calls: int
- calls: max
## modules.terminal_logger:TerminalLogger.set_eta_frequency
- calls: int
- calls: max
## modules.terminal_logger:TerminalLogger.start_logging
- calls: now
- calls: open
- calls: print
- calls: write
## modules.terminal_logger:TerminalLogger.stop_logging
- calls: now
- calls: open
- calls: print
- calls: write
## modules.terminal_logger:TerminalLogger.write
- calls: any
- calls: flush
- calls: group
- calls: int
- calls: open
- calls: print
- calls: search
- calls: splitlines
- calls: startswith
- calls: strip
- calls: write
## modules.terminal_logger:TerminalLogger.write_file_only
- calls: endswith
- calls: flush
- calls: open
- calls: write
## modules.terminal_logger:emit_chunk_summary
- calls: emit_chunk_summary
## modules.terminal_logger:get_running_avg_its
- calls: get_running_avg_its
## modules.terminal_logger:log_only
- calls: Path
- calls: endswith
- calls: open
- calls: write
- calls: write_file_only
## modules.terminal_logger:set_batch_size
- calls: set_batch_size
## modules.terminal_logger:set_eta_frequency
- calls: set_eta_frequency
## modules.terminal_logger:start_terminal_logging
- calls: TerminalLogger
- calls: start_logging
- calls: stop_logging
## modules.terminal_logger:stop_terminal_logging
- calls: stop_logging
## modules.text_processor:_break_long_sentence_simple
- calls: append
- calls: end
- calls: finditer
- calls: len
- calls: list
- calls: reversed
- calls: split
- calls: strip
## modules.text_processor:_combine_small_chunks
- calls: append
- calls: len
- calls: split
## modules.text_processor:_is_apostrophe
- calls: isalpha
- calls: len
## modules.text_processor:_split_long_dialogue
- calls: _split_long_dialogue
- calls: append
- calls: end
- calls: enumerate
- calls: extend
- calls: finditer
- calls: join
- calls: len
- calls: list
- calls: min
- calls: split
- calls: strip
## modules.text_processor:analyze_chunk_distribution
- calls: append
- calls: calculate_optimization_potential
- calls: get_chunk_bucket
- calls: isinstance
- calls: items
- calls: len
- calls: max
- calls: min
- calls: sum
## modules.text_processor:break_long_sentence_backwards
- calls: append
- calls: end
- calls: finditer
- calls: join
- calls: len
- calls: list
- calls: min
- calls: range
- calls: split
- calls: strip
## modules.text_processor:calculate_optimization_potential
- calls: max
## modules.text_processor:create_bucketed_chunk_groups
- calls: append
- calls: enumerate
- calls: get_chunk_bucket
- calls: isinstance
- calls: items
## modules.text_processor:create_sample_abbreviations_file
- calls: open
- calls: print
- calls: write
## modules.text_processor:detect_content_boundaries
- calls: detect_punctuation_boundary
- calls: len
- calls: search
- calls: strip
## modules.text_processor:detect_punctuation_boundary
- calls: endswith
- calls: strip
## modules.text_processor:fix_short_sentence_artifacts
- calls: append
- calls: endswith
- calls: join
- calls: len
- calls: range
- calls: split
- calls: strip
- calls: sum
## modules.text_processor:get_chunk_bucket
- calls: len
## modules.text_processor:load_abbreviations
- calls: Path
- calls: create_sample_abbreviations_file
- calls: enumerate
- calls: exists
- calls: len
- calls: open
- calls: print
- calls: split
- calls: startswith
- calls: strip
## modules.text_processor:log_chunk_bucketing_stats
- calls: analyze_chunk_distribution
- calls: capitalize
- calls: items
- calls: log_func
- calls: upper
## modules.text_processor:preprocess_abbreviations
- calls: info
- calls: items
- calls: replace
## modules.text_processor:reload_abbreviations
- calls: load_abbreviations
## modules.text_processor:sentence_chunk_text
- calls: _break_long_sentence_simple
- calls: _combine_small_chunks
- calls: any
- calls: append
- calls: enumerate
- calls: extend
- calls: len
- calls: lower
- calls: range
- calls: split
- calls: strip
## modules.text_processor:smart_punctuate
- calls: append
- calls: join
- calls: load_abbreviations
- calls: preprocess_abbreviations
- calls: print
- calls: replace
- calls: search
- calls: splitlines
- calls: strip
- calls: sub
## modules.text_processor:test_abbreviations
- calls: load_abbreviations
- calls: preprocess_abbreviations
- calls: print
## modules.text_processor:test_chunking
- calls: enumerate
- calls: len
- calls: print
- calls: sentence_chunk_text
- calls: split
## modules.token_analyzer:<module>
- calls: getLogger
## modules.token_analyzer:TokenAnalyzer.analyze_chunks_json
- calls: ValueError
- calls: append
- calls: error
- calls: get
- calls: int
- calls: len
- calls: load
- calls: max
- calls: mean
- calls: median
- calls: min
- calls: open
- calls: percentile
- calls: predict_chunk_tokens
- calls: std
- calls: str
## modules.token_analyzer:TokenAnalyzer.predict_chunk_tokens
- calls: abs
- calls: get
- calls: int
- calls: max
- calls: min
- calls: warning
## modules.token_analyzer:TokenAnalyzer.update_max_tokens_config
- calls: Path
- calls: error
- calls: exists
- calls: info
- calls: read_text
- calls: sub
- calls: write_text
## modules.token_analyzer:analyze_and_optimize_tokens
- calls: __import__
- calls: analyze_chunks_json
- calls: get_token_analyzer
- calls: getattr
- calls: update_max_tokens_config
## modules.token_analyzer:format_analysis_summary
- calls: append
- calls: get
- calls: join
## modules.token_analyzer:get_token_analyzer
- calls: TokenAnalyzer
## modules.token_calculator:TTSTokenCalculator.__init__
- calls: getattr
- calls: hasattr
## modules.token_calculator:TTSTokenCalculator.analyze_chunks
- calls: analyze_single_chunk
- calls: append
## modules.token_calculator:TTSTokenCalculator.analyze_single_chunk
- calls: TokenAnalysis
- calls: encode
- calls: hasattr
- calls: isinstance
- calls: len
- calls: max
- calls: print
- calls: size
- calls: split
- calls: tokenize
## modules.token_calculator:TTSTokenCalculator.print_analysis_summary
- calls: enumerate
- calls: len
- calls: print
## modules.token_calculator:TTSTokenCalculator.print_real_audiobook_analysis
- calls: append
- calls: get
- calls: hasattr
- calls: len
- calls: max
- calls: min
- calls: print
- calls: print_analysis_summary
- calls: sorted
- calls: sum
## modules.token_calculator:analyze_real_audiobook_chunks
- calls: TTSTokenCalculator
- calls: analyze_chunks
- calls: analyze_test_chunks
- calls: get
- calls: len
- calls: load
- calls: max
- calls: min
- calls: open
- calls: print
- calls: print_real_audiobook_analysis
- calls: sum
## modules.token_calculator:analyze_test_chunks
- calls: TTSTokenCalculator
- calls: analyze_chunks
- calls: print_analysis_summary
## modules.token_usage_logger:TokenUsageLogger.__init__
- calls: Lock
- calls: _initialize_log_file
## modules.token_usage_logger:TokenUsageLogger._initialize_log_file
- calls: now
- calls: open
- calls: print
- calls: write
## modules.token_usage_logger:TokenUsageLogger.get_log_summary
- calls: append
- calls: float
- calls: int
- calls: len
- calls: max
- calls: min
- calls: open
- calls: sorted
- calls: split
- calls: startswith
- calls: strip
- calls: sum
## modules.token_usage_logger:TokenUsageLogger.log_chunk_completion
- calls: open
- calls: print
- calls: time
- calls: write
## modules.token_usage_logger:TokenUsageLogger.log_chunk_data
- calls: open
- calls: print
- calls: write
## modules.token_usage_logger:TokenUsageLogger.print_summary
- calls: float
- calls: get_log_summary
- calls: print
## modules.token_usage_logger:TokenUsageLogger.start_chunk
- calls: time
## modules.token_usage_logger:initialize_token_logging
- calls: TokenUsageLogger
## modules.token_usage_logger:log_chunk_data_direct
- calls: log_chunk_data
## modules.token_usage_logger:log_chunk_tokens
- calls: log_chunk_completion
## modules.token_usage_logger:print_token_usage_summary
- calls: print
- calls: print_summary
## modules.token_usage_logger:start_chunk_logging
- calls: start_chunk
## modules.tts_engine:<module>
- calls: Lock
- calls: set
## modules.tts_engine:_core_tts_params_sig
- calls: float
- calls: get
- calls: round
## modules.tts_engine:_release_global_tts_model
- calls: clear
- calls: clear_cache
- calls: collect
- calls: cpu
- calls: empty_cache
- calls: hasattr
- calls: ipc_collect
- calls: is_available
- calls: items
- calls: print
- calls: reset_peak_memory_stats
- calls: reset_states
- calls: synchronize
## modules.tts_engine:_voice_sig
- calls: Path
- calls: resolve
- calls: stat
- calls: str
## modules.tts_engine:clear_voice_cache
- calls: info
## modules.tts_engine:create_parameter_microbatches
- calls: append
- calls: defaultdict
- calls: float
- calls: get
- calls: isinstance
- calls: items
- calls: len
- calls: print
- calls: range
- calls: sort
## modules.tts_engine:find_chunks_json_file
- calls: Path
- calls: exists
- calls: lower
- calls: replace
## modules.tts_engine:generate_enriched_chunks
- calls: SentimentIntensityAnalyzer
- calls: abs
- calls: add_voice_to_json
- calls: append
- calls: detect_content_boundaries
- calls: enumerate
- calls: get
- calls: info
- calls: int
- calls: len
- calls: max
- calls: min
- calls: polarity_scores
- calls: print
- calls: read_text
- calls: round
- calls: save_chunks
- calls: sentence_chunk_text
- calls: smart_punctuate
- calls: smooth_sentiment_scores
- calls: split
- calls: strftime
## modules.tts_engine:get_best_available_device
- calls: empty_cache
- calls: is_available
- calls: tensor
- calls: to
- calls: warning
## modules.tts_engine:get_optimal_workers
- calls: memory_allocated
- calls: min
## modules.tts_engine:load_optimized_model
- calls: Path
- calls: bool
- calls: error
- calls: eval
- calls: exists
- calls: from_local
- calls: from_pretrained
- calls: hasattr
- calls: info
- calls: is_available
- calls: optimize_chatterbox_model
- calls: randn
- calls: set_float32_matmul_precision
- calls: strip
- calls: warning
## modules.tts_engine:monitor_gpu_activity
- calls: is_available
- calls: memory_allocated
## modules.tts_engine:monitor_vram_usage
- calls: is_available
- calls: memory_allocated
- calls: memory_reserved
- calls: optimize_memory_usage
- calls: warning
## modules.tts_engine:optimize_memory_usage
- calls: collect
- calls: empty_cache
- calls: ipc_collect
- calls: is_available
## modules.tts_engine:patch_alignment_layer
- calls: MethodType
## modules.tts_engine:patch_alignment_layer.patched_forward
- calls: original_forward
## modules.tts_engine:prewarm_model_with_voice
- calls: ensure_voice_sample_compatibility
- calls: generate
- calls: prepare_conditionals
- calls: print
- calls: restore_voice_cache
- calls: store_voice_cache
## modules.tts_engine:process_batch
- calls: BytesIO
- calls: append
- calls: cpu
- calls: dim
- calls: enumerate
- calls: export
- calls: float
- calls: from_wav
- calls: gen_with_backoff
- calls: get
- calls: hasattr
- calls: info
- calls: items
- calls: len
- calls: max
- calls: min
- calls: no_grad
- calls: numpy
- calls: process_audio_with_trimming_and_silence
- calls: process_one_chunk
- calls: seek
- calls: set_seed
- calls: squeeze
- calls: trim_audio_endpoint
- calls: unsqueeze
- calls: warning
- calls: write
## modules.tts_engine:process_batch.gen_with_backoff
- calls: clear
- calls: collect
- calls: empty_cache
- calls: extend
- calls: generate_batch
- calls: is_available
- calls: len
- calls: lower
- calls: max
- calls: range
- calls: str
- calls: warning
## modules.tts_engine:process_book_folder
- calls: Path
- calls: ThreadPoolExecutor
- calls: _cuda_clearCublasWorkspaces
- calls: _release_global_tts_model
- calls: add_metadata_to_m4b
- calls: append
- calls: as_completed
- calls: bool
- calls: cleanup_asr_model
- calls: clear_voice_cache
- calls: collect
- calls: combine_audio_chunks
- calls: convert_to_m4b
- calls: copy
- calls: create_parameter_microbatches
- calls: empty_cache
- calls: ensure_voice_sample_compatibility
- calls: enumerate
- calls: error
- calls: estimate_tokens_in_text
- calls: exists
- calls: extend
- calls: find_book_files
- calls: float
- calls: generate_enriched_chunks
- calls: get
- calls: get_audio_files_in_directory
- calls: get_chunk_audio_duration
- calls: get_optimal_workers
- calls: getattr
- calls: glob
- calls: hasattr
- calls: info
- calls: int
- calls: ipc_collect
- calls: is_available
- calls: isinstance
- calls: join
- calls: len
- calls: load_asr_model_adaptive
- calls: load_optimized_model
- calls: log_chunk_progress
- calls: log_only
- calls: log_run
- calls: min
- calls: pause_for_chunk_review
- calls: prewarm_model_with_voice
- calls: print
- calls: range
- calls: record_model_reload
- calls: reset_peak_memory_stats
- calls: reset_reload_manager
- calls: result
- calls: round
- calls: set_batch_size
- calls: setup_book_directories
- calls: setup_logging
- calls: should_reload_model
- calls: sleep
- calls: start_terminal_logging
- calls: str
- calls: strftime
- calls: submit
- calls: sum
- calls: synchronize
- calls: time
- calls: timedelta
- calls: track_chunk_performance
- calls: type
- calls: unlink
## modules.tts_engine:process_one_chunk
- calls: BytesIO
- calls: RuntimeError
- calls: ValueError
- calls: _cuda_clearCublasWorkspaces
- calls: adjust_parameters_for_retry
- calls: array
- calls: astype
- calls: calculate_text_similarity
- calls: clear_cache
- calls: collect
- calls: copy
- calls: cpu
- calls: detach
- calls: dim
- calls: emit_chunk_summary
- calls: empty_cache
- calls: error
- calls: evaluate_chunk_quality
- calls: export
- calls: fp32_fallback_mode
- calls: from_wav
- calls: generate
- calls: get
- calls: get_array_of_samples
- calls: get_tts_optimizer
- calls: getenv
- calls: glob
- calls: has_mid_energy_drop
- calls: hasattr
- calls: info
- calls: ipc_collect
- calls: is_available
- calls: isinstance
- calls: items
- calls: len
- calls: list
- calls: locals
- calls: log_only
- calls: log_run_func
- calls: mean
- calls: memory_allocated
- calls: memory_reserved
- calls: no_grad
- calls: numpy
- calls: open
- calls: optimize_memory_usage
- calls: print
- calls: print_exc
- calls: process_audio_with_trimming_and_silence
- calls: punc_norm
- calls: range
- calls: reset_peak_memory_stats
- calls: reset_states
- calls: reshape
- calls: seek
- calls: set_seed
- calls: silent
- calls: sleep
- calls: squeeze
- calls: str
- calls: strip
- calls: synchronize
- calls: time
- calls: transcribe
- calls: trim_audio_endpoint
- calls: type
- calls: unlink
- calls: unsqueeze
- calls: warning
- calls: write
## modules.tts_engine:process_single_batch
- calls: Path
- calls: cleanup_asr_model
- calls: collect
- calls: empty_cache
- calls: ensure_voice_sample_compatibility
- calls: len
- calls: load_asr_model_adaptive
- calls: load_optimized_model
- calls: prewarm_model_with_voice
- calls: print
- calls: process_batch
- calls: punc_norm
## modules.tts_engine:process_single_batch.log_run
- calls: open
- calls: write
## modules.tts_engine:restore_voice_cache
- calls: debug
- calls: info
## modules.tts_engine:set_seed
- calls: hasattr
- calls: info
- calls: is_available
- calls: manual_seed
- calls: manual_seed_all
- calls: seed
## modules.tts_engine:smooth_sentiment_scores
- calls: len
- calls: max
- calls: reversed
- calls: sum
- calls: zip
## modules.tts_engine:store_voice_cache
- calls: getsizeof
- calls: hasattr
- calls: info
- calls: time
- calls: warning
## modules.voice_detector:add_voice_to_json
- calls: any
- calls: dump
- calls: insert
- calls: isinstance
- calls: keys
- calls: loads
- calls: open
- calls: print
- calls: read
- calls: startswith
- calls: write
## modules.voice_detector:detect_voice_for_book
- calls: get_likely_voices_for_book
## modules.voice_detector:find_voice_file_by_name
- calls: list_voice_samples
- calls: lower
## modules.voice_detector:get_likely_voices_for_book
- calls: any
- calls: append
- calls: find_voice_file_by_name
- calls: get_voice_from_json
- calls: get_voice_from_log
- calls: get_voices_from_filenames
- calls: len
- calls: print
## modules.voice_detector:get_voice_from_filename
- calls: get_voices_from_filenames
## modules.voice_detector:get_voice_from_json
- calls: group
- calls: isinstance
- calls: loads
- calls: open
- calls: print
- calls: read
- calls: search
- calls: strip
## modules.voice_detector:get_voice_from_log
- calls: Path
- calls: exists
- calls: open
- calls: print
- calls: split
- calls: startswith
- calls: strip
## modules.voice_detector:get_voices_from_filenames
- calls: Path
- calls: append
- calls: exists
- calls: glob
- calls: group
- calls: search
## modules.voice_detector:remove_voice_comment_from_json
- calls: join
- calls: len
- calls: open
- calls: print
- calls: read
- calls: split
- calls: startswith
- calls: strip
- calls: write
## modules.vram_bandwidth_monitor:VRAMBandwidthMonitor._analyze_snapshots
- calls: abs
- calls: append
- calls: len
- calls: max
- calls: min
- calls: range
- calls: sum
## modules.vram_bandwidth_monitor:VRAMBandwidthMonitor._get_vram_snapshot
- calls: VRAMSnapshot
- calls: int
- calls: len
- calls: run
- calls: split
- calls: strip
- calls: time
## modules.vram_bandwidth_monitor:VRAMBandwidthMonitor.print_analysis
- calls: print
## modules.vram_bandwidth_monitor:VRAMBandwidthMonitor.start_monitoring
- calls: Thread
- calls: print
- calls: start
## modules.vram_bandwidth_monitor:VRAMBandwidthMonitor.start_monitoring.monitor_loop
- calls: _get_vram_snapshot
- calls: append
- calls: sleep
## modules.vram_bandwidth_monitor:VRAMBandwidthMonitor.stop_monitoring
- calls: _analyze_snapshots
- calls: join
- calls: len
- calls: print
## modules.vram_bandwidth_monitor:monitor_t3_bandwidth.wrapper
- calls: func
- calls: start_vram_monitoring
- calls: stop_vram_monitoring_and_analyze
## modules.vram_bandwidth_monitor:start_vram_monitoring
- calls: VRAMBandwidthMonitor
- calls: start_monitoring
## modules.vram_bandwidth_monitor:stop_vram_monitoring_and_analyze
- calls: print_analysis
- calls: stop_monitoring
## scripts.make_backup:<module>
- calls: main
## scripts.make_backup:main
- calls: ArgumentParser
- calls: Path
- calls: add_argument
- calls: make_backup
- calls: parse_args
- calls: resolve
## scripts.make_backup:make_backup
- calls: ZipFile
- calls: add_path
- calls: exists
- calls: now
- calls: print
## scripts.make_backup:make_backup.add_path
- calls: is_dir
- calls: is_file
- calls: relative_to
- calls: rglob
- calls: str
- calls: write
## src.chatterbox.models.s3gen.decoder:CausalBlock1D.__init__
- calls: CausalConv1d
- calls: LayerNorm
- calls: Mish
- calls: Sequential
- calls: Transpose
- calls: __init__
- calls: super
## src.chatterbox.models.s3gen.decoder:CausalBlock1D.forward
- calls: block
## src.chatterbox.models.s3gen.decoder:CausalConv1d.__init__
- calls: __init__
- calls: super
## src.chatterbox.models.s3gen.decoder:CausalConv1d.forward
- calls: forward
- calls: pad
- calls: super
## src.chatterbox.models.s3gen.decoder:CausalResnetBlock1D.__init__
- calls: CausalBlock1D
- calls: __init__
- calls: super
## src.chatterbox.models.s3gen.decoder:ConditionalDecoder.__init__
- calls: BasicTransformerBlock
- calls: Block1D
- calls: CausalBlock1D
- calls: CausalConv1d
- calls: CausalResnetBlock1D
- calls: Conv1d
- calls: Downsample1D
- calls: ModuleList
- calls: ResnetBlock1D
- calls: SinusoidalPosEmb
- calls: TimestepEmbedding
- calls: Upsample1D
- calls: __init__
- calls: append
- calls: initialize_weights
- calls: len
- calls: range
- calls: super
- calls: tuple
## src.chatterbox.models.s3gen.decoder:ConditionalDecoder.forward
- calls: add_optional_chunk_mask
- calls: append
- calls: bool
- calls: contiguous
- calls: downsample
- calls: final_block
- calls: final_proj
- calls: mask_to_bias
- calls: pack
- calls: pop
- calls: rearrange
- calls: repeat
- calls: resnet
- calls: time_embeddings
- calls: time_mlp
- calls: to
- calls: transformer_block
- calls: upsample
## src.chatterbox.models.s3gen.decoder:ConditionalDecoder.initialize_weights
- calls: constant_
- calls: isinstance
- calls: kaiming_normal_
- calls: modules
## src.chatterbox.models.s3gen.decoder:Transpose.__init__
- calls: __init__
- calls: super
## src.chatterbox.models.s3gen.decoder:Transpose.forward
- calls: transpose
## src.chatterbox.models.s3gen.decoder:mask_to_bias
- calls: to
## src.chatterbox.models.s3gen.f0_predictor:ConvRNNF0Predictor.__init__
- calls: Conv1d
- calls: ELU
- calls: Linear
- calls: Sequential
- calls: __init__
- calls: super
- calls: weight_norm
## src.chatterbox.models.s3gen.f0_predictor:ConvRNNF0Predictor.forward
- calls: abs
- calls: classifier
- calls: condnet
- calls: squeeze
- calls: transpose
## src.chatterbox.models.s3gen.flow:CausalMaskedDiffWithXvec.__init__
- calls: DictConfig
- calls: Embedding
- calls: Linear
- calls: __init__
- calls: info
- calls: output_size
- calls: super
## src.chatterbox.models.s3gen.flow:CausalMaskedDiffWithXvec.inference
- calls: clamp
- calls: concat
- calls: contiguous
- calls: decoder
- calls: encoder
- calls: encoder_proj
- calls: float
- calls: half
- calls: inference_mode
- calls: input_embedding
- calls: make_pad_mask
- calls: normalize
- calls: spk_embed_affine_layer
- calls: tensor
- calls: to
- calls: transpose
- calls: unsqueeze
- calls: zeros
## src.chatterbox.models.s3gen.flow:MaskedDiffWithXvec.__init__
- calls: DictConfig
- calls: Embedding
- calls: Linear
- calls: __init__
- calls: info
- calls: output_size
- calls: super
## src.chatterbox.models.s3gen.flow:MaskedDiffWithXvec.forward
- calls: clamp
- calls: compute_loss
- calls: contiguous
- calls: encoder
- calls: encoder_proj
- calls: enumerate
- calls: float
- calls: input_embedding
- calls: int
- calls: interpolate
- calls: length_regulator
- calls: make_pad_mask
- calls: normalize
- calls: randint
- calls: random
- calls: spk_embed_affine_layer
- calls: squeeze
- calls: to
- calls: transpose
- calls: unsqueeze
- calls: zeros
## src.chatterbox.models.s3gen.flow:MaskedDiffWithXvec.inference
- calls: clamp
- calls: concat
- calls: contiguous
- calls: decoder
- calls: encoder
- calls: encoder_proj
- calls: float
- calls: half
- calls: inference
- calls: inference_mode
- calls: input_embedding
- calls: int
- calls: make_pad_mask
- calls: normalize
- calls: spk_embed_affine_layer
- calls: tensor
- calls: to
- calls: transpose
- calls: unsqueeze
- calls: zeros
## src.chatterbox.models.s3gen.flow_matching:<module>
- calls: create
## src.chatterbox.models.s3gen.flow_matching:CausalConditionalCFM.__init__
- calls: __init__
- calls: randn
- calls: super
## src.chatterbox.models.s3gen.flow_matching:CausalConditionalCFM.forward
- calls: cos
- calls: inference_mode
- calls: linspace
- calls: size
- calls: solve_euler
- calls: to
## src.chatterbox.models.s3gen.flow_matching:ConditionalCFM.__init__
- calls: Lock
- calls: __init__
- calls: super
## src.chatterbox.models.s3gen.flow_matching:ConditionalCFM.compute_loss
- calls: cos
- calls: estimator
- calls: mse_loss
- calls: rand
- calls: randn_like
- calls: squeeze
- calls: sum
- calls: view
## src.chatterbox.models.s3gen.flow_matching:ConditionalCFM.forward
- calls: concat
- calls: cos
- calls: inference_mode
- calls: linspace
- calls: randn_like
- calls: solve_euler
- calls: stack
- calls: to
- calls: zeros
## src.chatterbox.models.s3gen.flow_matching:ConditionalCFM.forward_estimator
- calls: contiguous
- calls: data_ptr
- calls: execute_v2
- calls: forward
- calls: isinstance
- calls: set_input_shape
- calls: size
## src.chatterbox.models.s3gen.flow_matching:ConditionalCFM.solve_euler
- calls: append
- calls: float
- calls: forward_estimator
- calls: len
- calls: range
- calls: size
- calls: split
- calls: unsqueeze
- calls: zeros
## src.chatterbox.models.s3gen.hifigan:HiFTGenerator.__init__
- calls: Conv1d
- calls: ConvTranspose1d
- calls: ModuleList
- calls: ReflectionPad1d
- calls: ResBlock
- calls: SourceModuleHnNSF
- calls: Upsample
- calls: __init__
- calls: append
- calls: apply
- calls: astype
- calls: cumprod
- calls: enumerate
- calls: from_numpy
- calls: get_window
- calls: len
- calls: prod
- calls: range
- calls: super
- calls: weight_norm
- calls: zip
## src.chatterbox.models.s3gen.hifigan:HiFTGenerator._istft
- calls: clip
- calls: complex
- calls: cos
- calls: istft
- calls: sin
- calls: to
## src.chatterbox.models.s3gen.hifigan:HiFTGenerator._stft
- calls: stft
- calls: to
- calls: view_as_real
## src.chatterbox.models.s3gen.hifigan:HiFTGenerator.decode
- calls: _istft
- calls: _stft
- calls: cat
- calls: clamp
- calls: conv_post
- calls: conv_pre
- calls: exp
- calls: leaky_relu
- calls: range
- calls: reflection_pad
- calls: sin
- calls: squeeze
- calls: zeros
## src.chatterbox.models.s3gen.hifigan:HiFTGenerator.forward
- calls: decode
- calls: f0_predictor
- calls: f0_upsamp
- calls: m_source
- calls: to
- calls: transpose
## src.chatterbox.models.s3gen.hifigan:HiFTGenerator.inference
- calls: decode
- calls: f0_predictor
- calls: f0_upsamp
- calls: inference_mode
- calls: m_source
- calls: transpose
- calls: zeros
## src.chatterbox.models.s3gen.hifigan:HiFTGenerator.remove_weight_norm
- calls: print
- calls: remove_weight_norm
## src.chatterbox.models.s3gen.hifigan:ResBlock.__init__
- calls: Conv1d
- calls: ModuleList
- calls: Snake
- calls: __init__
- calls: append
- calls: apply
- calls: get_padding
- calls: len
- calls: range
- calls: super
- calls: weight_norm
## src.chatterbox.models.s3gen.hifigan:ResBlock.forward
- calls: len
- calls: range
## src.chatterbox.models.s3gen.hifigan:ResBlock.remove_weight_norm
- calls: len
- calls: range
- calls: remove_weight_norm
## src.chatterbox.models.s3gen.hifigan:SineGen.__init__
- calls: __init__
- calls: super
## src.chatterbox.models.s3gen.hifigan:SineGen._f02uv
- calls: type
## src.chatterbox.models.s3gen.hifigan:SineGen.forward
- calls: Uniform
- calls: _f02uv
- calls: cumsum
- calls: no_grad
- calls: randn_like
- calls: range
- calls: sample
- calls: sin
- calls: size
- calls: to
- calls: zeros
## src.chatterbox.models.s3gen.hifigan:Snake.__init__
- calls: Parameter
- calls: __init__
- calls: ones
- calls: super
- calls: zeros
## src.chatterbox.models.s3gen.hifigan:Snake.forward
- calls: exp
- calls: pow
- calls: sin
- calls: unsqueeze
## src.chatterbox.models.s3gen.hifigan:SourceModuleHnNSF.__init__
- calls: Linear
- calls: SineGen
- calls: Tanh
- calls: __init__
- calls: super
## src.chatterbox.models.s3gen.hifigan:SourceModuleHnNSF.forward
- calls: l_linear
- calls: l_sin_gen
- calls: l_tanh
- calls: no_grad
- calls: randn_like
- calls: transpose
## src.chatterbox.models.s3gen.hifigan:get_padding
- calls: int
## src.chatterbox.models.s3gen.hifigan:init_weights
- calls: find
- calls: normal_
## src.chatterbox.models.s3gen.matcha.decoder:Block1D.__init__
- calls: Conv1d
- calls: GroupNorm
- calls: Mish
- calls: Sequential
- calls: __init__
- calls: super
## src.chatterbox.models.s3gen.matcha.decoder:Block1D.forward
- calls: block
## src.chatterbox.models.s3gen.matcha.decoder:ConformerWrapper.__init__
- calls: __init__
- calls: super
## src.chatterbox.models.s3gen.matcha.decoder:ConformerWrapper.forward
- calls: bool
- calls: forward
- calls: super
## src.chatterbox.models.s3gen.matcha.decoder:Decoder.__init__
- calls: Block1D
- calls: Conv1d
- calls: Downsample1D
- calls: ModuleList
- calls: ResnetBlock1D
- calls: SinusoidalPosEmb
- calls: TimestepEmbedding
- calls: Upsample1D
- calls: __init__
- calls: append
- calls: get_block
- calls: initialize_weights
- calls: len
- calls: range
- calls: super
- calls: tuple
## src.chatterbox.models.s3gen.matcha.decoder:Decoder.forward
- calls: append
- calls: downsample
- calls: final_block
- calls: final_proj
- calls: pack
- calls: pop
- calls: rearrange
- calls: repeat
- calls: resnet
- calls: time_embeddings
- calls: time_mlp
- calls: transformer_block
- calls: upsample
## src.chatterbox.models.s3gen.matcha.decoder:Decoder.get_block
- calls: BasicTransformerBlock
- calls: ConformerWrapper
- calls: ValueError
## src.chatterbox.models.s3gen.matcha.decoder:Decoder.initialize_weights
- calls: constant_
- calls: isinstance
- calls: kaiming_normal_
- calls: modules
## src.chatterbox.models.s3gen.matcha.decoder:Downsample1D.__init__
- calls: Conv1d
- calls: __init__
- calls: super
## src.chatterbox.models.s3gen.matcha.decoder:Downsample1D.forward
- calls: conv
## src.chatterbox.models.s3gen.matcha.decoder:ResnetBlock1D.__init__
- calls: Block1D
- calls: Conv1d
- calls: Linear
- calls: Mish
- calls: Sequential
- calls: __init__
- calls: super
## src.chatterbox.models.s3gen.matcha.decoder:ResnetBlock1D.forward
- calls: block1
- calls: block2
- calls: mlp
- calls: res_conv
- calls: unsqueeze
## src.chatterbox.models.s3gen.matcha.decoder:SinusoidalPosEmb.__init__
- calls: __init__
- calls: super
## src.chatterbox.models.s3gen.matcha.decoder:SinusoidalPosEmb.forward
- calls: arange
- calls: cat
- calls: cos
- calls: exp
- calls: float
- calls: log
- calls: sin
- calls: unsqueeze
## src.chatterbox.models.s3gen.matcha.decoder:TimestepEmbedding.__init__
- calls: Linear
- calls: __init__
- calls: get_activation
- calls: super
## src.chatterbox.models.s3gen.matcha.decoder:TimestepEmbedding.forward
- calls: act
- calls: cond_proj
- calls: linear_1
- calls: linear_2
- calls: post_act
## src.chatterbox.models.s3gen.matcha.decoder:Upsample1D.__init__
- calls: Conv1d
- calls: ConvTranspose1d
- calls: __init__
- calls: super
## src.chatterbox.models.s3gen.matcha.decoder:Upsample1D.forward
- calls: conv
- calls: interpolate
## src.chatterbox.models.s3gen.matcha.flow_matching:BASECFM.__init__
- calls: __init__
- calls: hasattr
- calls: super
## src.chatterbox.models.s3gen.matcha.flow_matching:BASECFM.compute_loss
- calls: estimator
- calls: mse_loss
- calls: rand
- calls: randn_like
- calls: squeeze
- calls: sum
## src.chatterbox.models.s3gen.matcha.flow_matching:BASECFM.forward
- calls: inference_mode
- calls: linspace
- calls: randn_like
- calls: solve_euler
## src.chatterbox.models.s3gen.matcha.flow_matching:BASECFM.solve_euler
- calls: append
- calls: estimator
- calls: len
- calls: range
## src.chatterbox.models.s3gen.matcha.flow_matching:CFM.__init__
- calls: Decoder
- calls: __init__
- calls: super
## src.chatterbox.models.s3gen.matcha.text_encoder:ConvReluNorm.__init__
- calls: Conv1d
- calls: Dropout
- calls: LayerNorm
- calls: ModuleList
- calls: ReLU
- calls: Sequential
- calls: __init__
- calls: append
- calls: range
- calls: super
- calls: zero_
## src.chatterbox.models.s3gen.matcha.text_encoder:ConvReluNorm.forward
- calls: proj
- calls: range
- calls: relu_drop
## src.chatterbox.models.s3gen.matcha.text_encoder:DurationPredictor.__init__
- calls: Conv1d
- calls: Dropout
- calls: LayerNorm
- calls: __init__
- calls: super
## src.chatterbox.models.s3gen.matcha.text_encoder:DurationPredictor.forward
- calls: conv_1
- calls: conv_2
- calls: drop
- calls: norm_1
- calls: norm_2
- calls: proj
- calls: relu
## src.chatterbox.models.s3gen.matcha.text_encoder:Encoder.__init__
- calls: Dropout
- calls: FFN
- calls: LayerNorm
- calls: ModuleList
- calls: MultiHeadAttention
- calls: __init__
- calls: append
- calls: range
- calls: super
## src.chatterbox.models.s3gen.matcha.text_encoder:Encoder.forward
- calls: drop
- calls: range
- calls: unsqueeze
## src.chatterbox.models.s3gen.matcha.text_encoder:FFN.__init__
- calls: Conv1d
- calls: Dropout
- calls: __init__
- calls: super
## src.chatterbox.models.s3gen.matcha.text_encoder:FFN.forward
- calls: conv_1
- calls: conv_2
- calls: drop
- calls: relu
## src.chatterbox.models.s3gen.matcha.text_encoder:LayerNorm.__init__
- calls: Parameter
- calls: __init__
- calls: ones
- calls: super
- calls: zeros
## src.chatterbox.models.s3gen.matcha.text_encoder:LayerNorm.forward
- calls: len
- calls: mean
- calls: rsqrt
- calls: view
## src.chatterbox.models.s3gen.matcha.text_encoder:MultiHeadAttention.__init__
- calls: Conv1d
- calls: Dropout
- calls: RotaryPositionalEmbeddings
- calls: __init__
- calls: copy_
- calls: super
- calls: xavier_uniform_
## src.chatterbox.models.s3gen.matcha.text_encoder:MultiHeadAttention._attention_bias_proximal
- calls: abs
- calls: arange
- calls: log1p
- calls: unsqueeze
## src.chatterbox.models.s3gen.matcha.text_encoder:MultiHeadAttention.attention
- calls: _attention_bias_proximal
- calls: contiguous
- calls: drop
- calls: key_rotary_pe
- calls: masked_fill
- calls: matmul
- calls: query_rotary_pe
- calls: rearrange
- calls: size
- calls: softmax
- calls: sqrt
- calls: to
- calls: transpose
- calls: view
## src.chatterbox.models.s3gen.matcha.text_encoder:MultiHeadAttention.forward
- calls: attention
- calls: conv_k
- calls: conv_o
- calls: conv_q
- calls: conv_v
## src.chatterbox.models.s3gen.matcha.text_encoder:RotaryPositionalEmbeddings.__init__
- calls: __init__
- calls: int
- calls: super
## src.chatterbox.models.s3gen.matcha.text_encoder:RotaryPositionalEmbeddings._build_cache
- calls: arange
- calls: cat
- calls: cos
- calls: einsum
- calls: float
- calls: sin
- calls: to
## src.chatterbox.models.s3gen.matcha.text_encoder:RotaryPositionalEmbeddings._neg_half
- calls: cat
## src.chatterbox.models.s3gen.matcha.text_encoder:RotaryPositionalEmbeddings.forward
- calls: _build_cache
- calls: _neg_half
- calls: cat
- calls: rearrange
## src.chatterbox.models.s3gen.matcha.text_encoder:TextEncoder.__init__
- calls: Conv1d
- calls: ConvReluNorm
- calls: DurationPredictor
- calls: Embedding
- calls: Encoder
- calls: __init__
- calls: normal_
- calls: super
## src.chatterbox.models.s3gen.matcha.text_encoder:TextEncoder.forward
- calls: cat
- calls: detach
- calls: emb
- calls: encoder
- calls: prenet
- calls: proj_m
- calls: proj_w
- calls: repeat
- calls: sequence_mask
- calls: size
- calls: sqrt
- calls: to
- calls: transpose
- calls: unsqueeze
## src.chatterbox.models.s3gen.matcha.text_encoder:sequence_mask
- calls: arange
- calls: max
- calls: unsqueeze
## src.chatterbox.models.s3gen.matcha.transformer:BasicTransformerBlock.__init__
- calls: AdaLayerNorm
- calls: AdaLayerNormZero
- calls: Attention
- calls: FeedForward
- calls: LayerNorm
- calls: ValueError
- calls: __init__
- calls: super
## src.chatterbox.models.s3gen.matcha.transformer:BasicTransformerBlock.forward
- calls: ValueError
- calls: attn1
- calls: attn2
- calls: cat
- calls: chunk
- calls: ff
- calls: norm1
- calls: norm2
- calls: norm3
- calls: unsqueeze
## src.chatterbox.models.s3gen.matcha.transformer:FeedForward.__init__
- calls: ApproximateGELU
- calls: Dropout
- calls: GEGLU
- calls: GELU
- calls: LoRACompatibleLinear
- calls: ModuleList
- calls: SnakeBeta
- calls: __init__
- calls: append
- calls: int
- calls: super
## src.chatterbox.models.s3gen.matcha.transformer:FeedForward.forward
- calls: module
## src.chatterbox.models.s3gen.matcha.transformer:SnakeBeta.__init__
- calls: LoRACompatibleLinear
- calls: Parameter
- calls: __init__
- calls: isinstance
- calls: ones
- calls: super
- calls: zeros
## src.chatterbox.models.s3gen.matcha.transformer:SnakeBeta.forward
- calls: exp
- calls: pow
- calls: proj
- calls: sin
## src.chatterbox.models.s3gen.s3gen:S3Token2Mel.__init__
- calls: CAMPPlus
- calls: CausalConditionalCFM
- calls: CausalMaskedDiffWithXvec
- calls: ConditionalDecoder
- calls: DictConfig
- calls: S3Tokenizer
- calls: UpsampleConformerEncoder
- calls: __init__
- calls: super
## src.chatterbox.models.s3gen.s3gen:S3Token2Mel.device
- calls: next
- calls: parameters
## src.chatterbox.models.s3gen.s3gen:S3Token2Mel.embed_ref
- calls: dict
- calls: float
- calls: from_numpy
- calls: get_resampler
- calls: inference
- calls: isinstance
- calls: len
- calls: mel_extractor
- calls: print
- calls: size
- calls: to
- calls: tokenizer
- calls: transpose
- calls: unsqueeze
- calls: warning
## src.chatterbox.models.s3gen.s3gen:S3Token2Mel.forward
- calls: LongTensor
- calls: embed_ref
- calls: from_numpy
- calls: inference
- calls: is_tensor
- calls: isinstance
- calls: len
- calls: list
- calls: size
- calls: to
- calls: unsqueeze
## src.chatterbox.models.s3gen.s3gen:S3Token2Wav.__init__
- calls: ConvRNNF0Predictor
- calls: HiFTGenerator
- calls: __init__
- calls: cos
- calls: linspace
- calls: register_buffer
- calls: super
- calls: zeros
## src.chatterbox.models.s3gen.s3gen:S3Token2Wav.flow_inference
- calls: forward
- calls: inference_mode
- calls: super
## src.chatterbox.models.s3gen.s3gen:S3Token2Wav.forward
- calls: forward
- calls: inference
- calls: len
- calls: min
- calls: size
- calls: super
- calls: to
- calls: zeros
## src.chatterbox.models.s3gen.s3gen:S3Token2Wav.hift_inference
- calls: inference
- calls: inference_mode
- calls: to
- calls: zeros
## src.chatterbox.models.s3gen.s3gen:S3Token2Wav.inference
- calls: flow_inference
- calls: hift_inference
- calls: inference_mode
- calls: len
- calls: min
- calls: size
## src.chatterbox.models.s3gen.s3gen:drop_invalid_tokens
- calls: len
## src.chatterbox.models.s3gen.s3gen:get_resampler
- calls: Resample
- calls: lru_cache
- calls: to
## src.chatterbox.models.s3gen.transformer.activation:Snake.__init__
- calls: Parameter
- calls: __init__
- calls: ones
- calls: super
- calls: zeros
## src.chatterbox.models.s3gen.transformer.activation:Snake.forward
- calls: exp
- calls: pow
- calls: sin
- calls: unsqueeze
## src.chatterbox.models.s3gen.transformer.activation:Swish.forward
- calls: sigmoid
## src.chatterbox.models.s3gen.transformer.attention:MultiHeadedAttention.__init__
- calls: Dropout
- calls: Linear
- calls: __init__
- calls: super
## src.chatterbox.models.s3gen.transformer.attention:MultiHeadedAttention.forward
- calls: cat
- calls: empty
- calls: forward_attention
- calls: forward_qkv
- calls: matmul
- calls: ones
- calls: size
- calls: split
- calls: sqrt
- calls: transpose
- calls: zeros
## src.chatterbox.models.s3gen.transformer.attention:MultiHeadedAttention.forward_attention
- calls: contiguous
- calls: dropout
- calls: eq
- calls: float
- calls: linear_out
- calls: masked_fill
- calls: matmul
- calls: ones
- calls: size
- calls: softmax
- calls: transpose
- calls: unsqueeze
- calls: view
## src.chatterbox.models.s3gen.transformer.attention:MultiHeadedAttention.forward_qkv
- calls: linear_k
- calls: linear_q
- calls: linear_v
- calls: size
- calls: transpose
- calls: view
## src.chatterbox.models.s3gen.transformer.attention:RelPositionMultiHeadedAttention.__init__
- calls: Linear
- calls: Parameter
- calls: Tensor
- calls: __init__
- calls: super
- calls: xavier_uniform_
## src.chatterbox.models.s3gen.transformer.attention:RelPositionMultiHeadedAttention.forward
- calls: cat
- calls: empty
- calls: forward_attention
- calls: forward_qkv
- calls: linear_pos
- calls: matmul
- calls: ones
- calls: rel_shift
- calls: size
- calls: split
- calls: sqrt
- calls: to
- calls: transpose
- calls: view
- calls: zeros
## src.chatterbox.models.s3gen.transformer.attention:RelPositionMultiHeadedAttention.rel_shift
- calls: cat
- calls: size
- calls: view
- calls: view_as
- calls: zeros
## src.chatterbox.models.s3gen.transformer.convolution:ConvolutionModule.__init__
- calls: BatchNorm1d
- calls: Conv1d
- calls: LayerNorm
- calls: ReLU
- calls: __init__
- calls: super
## src.chatterbox.models.s3gen.transformer.convolution:ConvolutionModule.forward
- calls: activation
- calls: cat
- calls: depthwise_conv
- calls: glu
- calls: masked_fill_
- calls: norm
- calls: ones
- calls: pad
- calls: pointwise_conv1
- calls: pointwise_conv2
- calls: size
- calls: transpose
- calls: zeros
## src.chatterbox.models.s3gen.transformer.embedding:EspnetRelPositionalEncoding.__init__
- calls: Dropout
- calls: __init__
- calls: expand
- calls: extend_pe
- calls: sqrt
- calls: super
- calls: tensor
## src.chatterbox.models.s3gen.transformer.embedding:EspnetRelPositionalEncoding.extend_pe
- calls: arange
- calls: cat
- calls: cos
- calls: exp
- calls: flip
- calls: log
- calls: sin
- calls: size
- calls: to
- calls: unsqueeze
- calls: zeros
## src.chatterbox.models.s3gen.transformer.embedding:EspnetRelPositionalEncoding.forward
- calls: dropout
- calls: extend_pe
- calls: position_encoding
- calls: size
## src.chatterbox.models.s3gen.transformer.embedding:EspnetRelPositionalEncoding.position_encoding
- calls: size
## src.chatterbox.models.s3gen.transformer.embedding:LearnablePositionalEncoding.__init__
- calls: Parameter
- calls: __init__
- calls: empty
- calls: super
## src.chatterbox.models.s3gen.transformer.embedding:NoPositionalEncoding.__init__
- calls: Dropout
- calls: __init__
- calls: super
## src.chatterbox.models.s3gen.transformer.embedding:NoPositionalEncoding.forward
- calls: dropout
- calls: size
- calls: to
- calls: zeros
## src.chatterbox.models.s3gen.transformer.embedding:NoPositionalEncoding.position_encoding
- calls: zeros
## src.chatterbox.models.s3gen.transformer.embedding:PositionalEncoding.__init__
- calls: Dropout
- calls: __init__
- calls: arange
- calls: cos
- calls: exp
- calls: log
- calls: sin
- calls: sqrt
- calls: super
- calls: unsqueeze
- calls: zeros
## src.chatterbox.models.s3gen.transformer.embedding:PositionalEncoding.forward
- calls: dropout
- calls: position_encoding
- calls: size
- calls: to
## src.chatterbox.models.s3gen.transformer.embedding:PositionalEncoding.position_encoding
- calls: arange
- calls: dim
- calls: dropout
- calls: embedding
- calls: isinstance
- calls: max
- calls: to
- calls: unsqueeze
## src.chatterbox.models.s3gen.transformer.embedding:RelPositionalEncoding.__init__
- calls: __init__
- calls: super
## src.chatterbox.models.s3gen.transformer.embedding:RelPositionalEncoding.forward
- calls: dropout
- calls: position_encoding
- calls: size
- calls: to
## src.chatterbox.models.s3gen.transformer.embedding:WhisperPositionalEncoding.__init__
- calls: __init__
- calls: arange
- calls: cat
- calls: cos
- calls: delattr
- calls: exp
- calls: log
- calls: register_buffer
- calls: sin
- calls: super
- calls: unsqueeze
## src.chatterbox.models.s3gen.transformer.encoder_layer:ConformerEncoderLayer.__init__
- calls: Dropout
- calls: LayerNorm
- calls: __init__
- calls: super
## src.chatterbox.models.s3gen.transformer.encoder_layer:ConformerEncoderLayer.forward
- calls: conv_module
- calls: dropout
- calls: feed_forward
- calls: feed_forward_macaron
- calls: norm_conv
- calls: norm_ff
- calls: norm_ff_macaron
- calls: norm_final
- calls: norm_mha
- calls: ones
- calls: self_attn
- calls: zeros
## src.chatterbox.models.s3gen.transformer.encoder_layer:TransformerEncoderLayer.__init__
- calls: Dropout
- calls: LayerNorm
- calls: __init__
- calls: super
## src.chatterbox.models.s3gen.transformer.encoder_layer:TransformerEncoderLayer.forward
- calls: dropout
- calls: feed_forward
- calls: norm1
- calls: norm2
- calls: ones
- calls: self_attn
- calls: zeros
## src.chatterbox.models.s3gen.transformer.positionwise_feed_forward:MoEFFNLayer.__init__
- calls: Linear
- calls: ModuleList
- calls: PositionwiseFeedForward
- calls: ReLU
- calls: __init__
- calls: range
- calls: super
## src.chatterbox.models.s3gen.transformer.positionwise_feed_forward:MoEFFNLayer.forward
- calls: enumerate
- calls: expert
- calls: gate
- calls: size
- calls: softmax
- calls: to
- calls: topk
- calls: view
- calls: where
- calls: zeros_like
## src.chatterbox.models.s3gen.transformer.positionwise_feed_forward:PositionwiseFeedForward.__init__
- calls: Dropout
- calls: Linear
- calls: ReLU
- calls: __init__
- calls: super
## src.chatterbox.models.s3gen.transformer.positionwise_feed_forward:PositionwiseFeedForward.forward
- calls: activation
- calls: dropout
- calls: w_1
- calls: w_2
## src.chatterbox.models.s3gen.transformer.subsampling:BaseSubsampling.__init__
- calls: __init__
- calls: super
## src.chatterbox.models.s3gen.transformer.subsampling:BaseSubsampling.position_encoding
- calls: position_encoding
## src.chatterbox.models.s3gen.transformer.subsampling:Conv1dSubsampling2.__init__
- calls: Conv1d
- calls: GELU
- calls: Sequential
- calls: __init__
- calls: super
## src.chatterbox.models.s3gen.transformer.subsampling:Conv1dSubsampling2.forward
- calls: conv
- calls: pos_enc
- calls: size
- calls: transpose
## src.chatterbox.models.s3gen.transformer.subsampling:Conv2dSubsampling4.__init__
- calls: Conv2d
- calls: Linear
- calls: ReLU
- calls: Sequential
- calls: __init__
- calls: super
## src.chatterbox.models.s3gen.transformer.subsampling:Conv2dSubsampling4.forward
- calls: contiguous
- calls: conv
- calls: out
- calls: pos_enc
- calls: size
- calls: transpose
- calls: unsqueeze
- calls: view
## src.chatterbox.models.s3gen.transformer.subsampling:Conv2dSubsampling6.__init__
- calls: Conv2d
- calls: Linear
- calls: ReLU
- calls: Sequential
- calls: __init__
- calls: super
## src.chatterbox.models.s3gen.transformer.subsampling:Conv2dSubsampling6.forward
- calls: contiguous
- calls: conv
- calls: linear
- calls: pos_enc
- calls: size
- calls: transpose
- calls: unsqueeze
- calls: view
## src.chatterbox.models.s3gen.transformer.subsampling:Conv2dSubsampling8.__init__
- calls: Conv2d
- calls: Linear
- calls: ReLU
- calls: Sequential
- calls: __init__
- calls: super
## src.chatterbox.models.s3gen.transformer.subsampling:Conv2dSubsampling8.forward
- calls: contiguous
- calls: conv
- calls: linear
- calls: pos_enc
- calls: size
- calls: transpose
- calls: unsqueeze
- calls: view
## src.chatterbox.models.s3gen.transformer.subsampling:EmbedinigNoSubsampling.__init__
- calls: Embedding
- calls: __init__
- calls: super
## src.chatterbox.models.s3gen.transformer.subsampling:EmbedinigNoSubsampling.forward
- calls: embed
- calls: pos_enc
## src.chatterbox.models.s3gen.transformer.subsampling:LegacyLinearNoSubsampling.__init__
- calls: Dropout
- calls: LayerNorm
- calls: Linear
- calls: ReLU
- calls: Sequential
- calls: __init__
- calls: super
## src.chatterbox.models.s3gen.transformer.subsampling:LegacyLinearNoSubsampling.forward
- calls: out
- calls: pos_enc
## src.chatterbox.models.s3gen.transformer.subsampling:LinearNoSubsampling.__init__
- calls: Dropout
- calls: LayerNorm
- calls: Linear
- calls: Sequential
- calls: __init__
- calls: super
## src.chatterbox.models.s3gen.transformer.subsampling:LinearNoSubsampling.forward
- calls: out
- calls: pos_enc
## src.chatterbox.models.s3gen.transformer.upsample_encoder:PreLookaheadLayer.__init__
- calls: Conv1d
- calls: __init__
- calls: super
## src.chatterbox.models.s3gen.transformer.upsample_encoder:PreLookaheadLayer.forward
- calls: contiguous
- calls: conv1
- calls: conv2
- calls: leaky_relu
- calls: pad
- calls: transpose
## src.chatterbox.models.s3gen.transformer.upsample_encoder:Upsample1D.__init__
- calls: Conv1d
- calls: __init__
- calls: super
## src.chatterbox.models.s3gen.transformer.upsample_encoder:Upsample1D.forward
- calls: conv
- calls: float
- calls: interpolate
- calls: pad
## src.chatterbox.models.s3gen.transformer.upsample_encoder:UpsampleConformerEncoder.__init__
- calls: ConformerEncoderLayer
- calls: ConvolutionModule
- calls: LayerNorm
- calls: ModuleList
- calls: PositionwiseFeedForward
- calls: PreLookaheadLayer
- calls: Upsample1D
- calls: __init__
- calls: range
- calls: super
## src.chatterbox.models.s3gen.transformer.upsample_encoder:UpsampleConformerEncoder.forward
- calls: add_optional_chunk_mask
- calls: after_norm
- calls: contiguous
- calls: embed
- calls: forward_layers
- calls: forward_up_layers
- calls: global_cmvn
- calls: make_pad_mask
- calls: pre_lookahead_layer
- calls: size
- calls: transpose
- calls: unsqueeze
- calls: up_embed
- calls: up_layer
## src.chatterbox.models.s3gen.transformer.upsample_encoder:UpsampleConformerEncoder.forward_layers
- calls: layer
## src.chatterbox.models.s3gen.transformer.upsample_encoder:UpsampleConformerEncoder.forward_up_layers
- calls: layer
## src.chatterbox.models.s3gen.utils.class_utils:<module>
- calls: getattr
## src.chatterbox.models.s3gen.utils.mask:add_optional_chunk_mask
- calls: item
- calls: randint
- calls: size
- calls: subsequent_chunk_mask
- calls: sum
- calls: unsqueeze
- calls: warning
## src.chatterbox.models.s3gen.utils.mask:make_pad_mask
- calls: arange
- calls: expand
- calls: item
- calls: max
- calls: size
- calls: unsqueeze
## src.chatterbox.models.s3gen.utils.mask:subsequent_chunk_mask
- calls: arange
- calls: device
- calls: div
- calls: unsqueeze
## src.chatterbox.models.s3gen.utils.mel:dynamic_range_compression_torch
- calls: clamp
- calls: log
## src.chatterbox.models.s3gen.utils.mel:mel_spectrogram
- calls: float
- calls: from_numpy
- calls: hann_window
- calls: int
- calls: isinstance
- calls: len
- calls: librosa_mel_fn
- calls: matmul
- calls: max
- calls: min
- calls: pad
- calls: pow
- calls: print
- calls: spectral_normalize_torch
- calls: sqrt
- calls: squeeze
- calls: stft
- calls: str
- calls: sum
- calls: tensor
- calls: to
- calls: unsqueeze
- calls: view_as_real
## src.chatterbox.models.s3gen.utils.mel:spectral_normalize_torch
- calls: dynamic_range_compression_torch
## src.chatterbox.models.s3gen.xvector:BasicResBlock.__init__
- calls: BatchNorm2d
- calls: Conv2d
- calls: Sequential
- calls: __init__
- calls: super
## src.chatterbox.models.s3gen.xvector:BasicResBlock.forward
- calls: bn1
- calls: bn2
- calls: conv1
- calls: conv2
- calls: relu
- calls: shortcut
## src.chatterbox.models.s3gen.xvector:CAMDenseTDNNBlock.__init__
- calls: CAMDenseTDNNLayer
- calls: __init__
- calls: add_module
- calls: range
- calls: super
## src.chatterbox.models.s3gen.xvector:CAMDenseTDNNBlock.forward
- calls: cat
- calls: layer
## src.chatterbox.models.s3gen.xvector:CAMDenseTDNNLayer.__init__
- calls: CAMLayer
- calls: Conv1d
- calls: __init__
- calls: format
- calls: get_nonlinear
- calls: super
## src.chatterbox.models.s3gen.xvector:CAMDenseTDNNLayer.bn_function
- calls: linear1
- calls: nonlinear1
## src.chatterbox.models.s3gen.xvector:CAMDenseTDNNLayer.forward
- calls: bn_function
- calls: cam_layer
- calls: checkpoint
- calls: nonlinear2
## src.chatterbox.models.s3gen.xvector:CAMLayer.__init__
- calls: Conv1d
- calls: ReLU
- calls: Sigmoid
- calls: __init__
- calls: super
## src.chatterbox.models.s3gen.xvector:CAMLayer.forward
- calls: linear1
- calls: linear2
- calls: linear_local
- calls: mean
- calls: relu
- calls: seg_pooling
- calls: sigmoid
## src.chatterbox.models.s3gen.xvector:CAMLayer.seg_pooling
- calls: ValueError
- calls: avg_pool1d
- calls: expand
- calls: max_pool1d
- calls: reshape
- calls: unsqueeze
## src.chatterbox.models.s3gen.xvector:CAMPPlus.__init__
- calls: CAMDenseTDNNBlock
- calls: DenseLayer
- calls: FCM
- calls: OrderedDict
- calls: Sequential
- calls: StatsPool
- calls: TDNNLayer
- calls: TransitLayer
- calls: __init__
- calls: add_module
- calls: enumerate
- calls: get_nonlinear
- calls: isinstance
- calls: kaiming_normal_
- calls: modules
- calls: super
- calls: zeros_
- calls: zip
## src.chatterbox.models.s3gen.xvector:CAMPPlus.forward
- calls: head
- calls: permute
- calls: transpose
- calls: xvector
## src.chatterbox.models.s3gen.xvector:CAMPPlus.inference
- calls: extract_feature
- calls: forward
- calls: to
## src.chatterbox.models.s3gen.xvector:DenseLayer.__init__
- calls: Conv1d
- calls: __init__
- calls: get_nonlinear
- calls: super
## src.chatterbox.models.s3gen.xvector:DenseLayer.forward
- calls: len
- calls: linear
- calls: nonlinear
- calls: squeeze
- calls: unsqueeze
## src.chatterbox.models.s3gen.xvector:FCM.__init__
- calls: BatchNorm2d
- calls: Conv2d
- calls: __init__
- calls: _make_layer
- calls: super
## src.chatterbox.models.s3gen.xvector:FCM._make_layer
- calls: Sequential
- calls: append
- calls: block
## src.chatterbox.models.s3gen.xvector:FCM.forward
- calls: bn1
- calls: bn2
- calls: conv1
- calls: conv2
- calls: layer1
- calls: layer2
- calls: relu
- calls: reshape
- calls: unsqueeze
## src.chatterbox.models.s3gen.xvector:StatsPool.forward
- calls: statistics_pooling
## src.chatterbox.models.s3gen.xvector:TDNNLayer.__init__
- calls: Conv1d
- calls: __init__
- calls: format
- calls: get_nonlinear
- calls: super
## src.chatterbox.models.s3gen.xvector:TDNNLayer.forward
- calls: linear
- calls: nonlinear
## src.chatterbox.models.s3gen.xvector:TransitLayer.__init__
- calls: Conv1d
- calls: __init__
- calls: get_nonlinear
- calls: super
## src.chatterbox.models.s3gen.xvector:TransitLayer.forward
- calls: linear
- calls: nonlinear
## src.chatterbox.models.s3gen.xvector:extract_feature
- calls: append
- calls: fbank
- calls: mean
- calls: pad_list
- calls: unsqueeze
## src.chatterbox.models.s3gen.xvector:get_nonlinear
- calls: BatchNorm1d
- calls: PReLU
- calls: ReLU
- calls: Sequential
- calls: ValueError
- calls: add_module
- calls: format
- calls: split
## src.chatterbox.models.s3gen.xvector:pad_list
- calls: fill_
- calls: len
- calls: max
- calls: new
- calls: range
- calls: size
## src.chatterbox.models.s3gen.xvector:statistics_pooling
- calls: cat
- calls: mean
- calls: std
- calls: unsqueeze
## src.chatterbox.models.s3tokenizer.__init__:drop_invalid_tokens
- calls: len
- calls: nonzero
- calls: squeeze
## src.chatterbox.models.s3tokenizer.s3tokenizer:S3Tokenizer.__init__
- calls: FloatTensor
- calls: ModelConfig
- calls: __init__
- calls: hann_window
- calls: mel
- calls: register_buffer
- calls: super
## src.chatterbox.models.s3tokenizer.s3tokenizer:S3Tokenizer._prepare_audio
- calls: append
- calls: dim
- calls: from_numpy
- calls: isinstance
- calls: unsqueeze
## src.chatterbox.models.s3tokenizer.s3tokenizer:S3Tokenizer.forward
- calls: _prepare_audio
- calls: append
- calls: detach
- calls: log_mel_spectrogram
- calls: long
- calls: no_grad
- calls: padding
- calls: quantize
- calls: squeeze
- calls: to
- calls: unwrap_model
## src.chatterbox.models.s3tokenizer.s3tokenizer:S3Tokenizer.log_mel_spectrogram
- calls: abs
- calls: clamp
- calls: from_numpy
- calls: is_tensor
- calls: log10
- calls: max
- calls: maximum
- calls: pad
- calls: stft
- calls: to
## src.chatterbox.models.s3tokenizer.s3tokenizer:S3Tokenizer.pad
- calls: append
- calls: ceil
- calls: dim
- calls: from_numpy
- calls: int
- calls: isinstance
- calls: pad
- calls: unsqueeze
## src.chatterbox.models.t3.inference.alignment_stream_analyzer:<module>
- calls: getLogger
## src.chatterbox.models.t3.inference.alignment_stream_analyzer:AlignmentStreamAnalyzer.__init__
- calls: _add_attention_spy
- calls: device
- calls: next
- calls: parameters
- calls: zeros
## src.chatterbox.models.t3.inference.alignment_stream_analyzer:AlignmentStreamAnalyzer._add_attention_spy
- calls: MethodType
- calls: register_forward_hook
## src.chatterbox.models.t3.inference.alignment_stream_analyzer:AlignmentStreamAnalyzer._add_attention_spy.attention_forward_hook
- calls: detach
- calls: mean
## src.chatterbox.models.t3.inference.alignment_stream_analyzer:AlignmentStreamAnalyzer._add_attention_spy.patched_forward
- calls: original_forward
## src.chatterbox.models.t3.inference.alignment_stream_analyzer:AlignmentStreamAnalyzer.close
- calls: hasattr
- calls: remove
## src.chatterbox.models.t3.inference.alignment_stream_analyzer:AlignmentStreamAnalyzer.step
- calls: argmax
- calls: cat
- calls: clone
- calls: max
- calls: ones_like
- calls: sum
- calls: warn
## src.chatterbox.models.t3.inference.t3_hf_backend:T3HuggingfaceBackend.__init__
- calls: __init__
- calls: super
## src.chatterbox.models.t3.inference.t3_hf_backend:T3HuggingfaceBackend.forward
- calls: CausalLMOutputWithCrossAttentions
- calls: inference_mode
- calls: len
- calls: model
- calls: size
- calls: speech_head
## src.chatterbox.models.t3.inference.t3_hf_backend:T3HuggingfaceBackend.prepare_inputs_for_generation
- calls: cat
- calls: expand
- calls: inference_mode
- calls: size
- calls: speech_enc
## src.chatterbox.models.t3.llama_configs:<module>
- calls: dict
## src.chatterbox.models.t3.modules.cond_enc:T3Cond.load
- calls: T3Cond
- calls: load
## src.chatterbox.models.t3.modules.cond_enc:T3Cond.save
- calls: save
## src.chatterbox.models.t3.modules.cond_enc:T3Cond.to
- calls: is_tensor
- calls: item
- calls: items
- calls: setattr
- calls: to
- calls: type
- calls: view
## src.chatterbox.models.t3.modules.cond_enc:T3CondEnc.__init__
- calls: Linear
- calls: NotImplementedError
- calls: Perceiver
- calls: __init__
- calls: str
- calls: super
## src.chatterbox.models.t3.modules.cond_enc:T3CondEnc.forward
- calls: cat
- calls: emotion_adv_fc
- calls: perceiver
- calls: spkr_enc
- calls: view
- calls: zeros_like
## src.chatterbox.models.t3.modules.learned_pos_emb:LearnedPositionEmbeddings.__init__
- calls: Embedding
- calls: __init__
- calls: normal_
- calls: super
## src.chatterbox.models.t3.modules.learned_pos_emb:LearnedPositionEmbeddings.forward
- calls: arange
- calls: emb
## src.chatterbox.models.t3.modules.learned_pos_emb:LearnedPositionEmbeddings.get_fixed_embedding
- calls: atleast_2d
- calls: emb
- calls: is_tensor
- calls: tensor
- calls: to
## src.chatterbox.models.t3.modules.perceiver:AttentionBlock2.__init__
- calls: AttentionQKV
- calls: LayerNorm
- calls: Linear
- calls: RelativePositionBias
- calls: __init__
- calls: super
## src.chatterbox.models.t3.modules.perceiver:AttentionBlock2.forward
- calls: attention
- calls: norm
- calls: proj_out
- calls: reshape
- calls: to_k
- calls: to_q
- calls: to_v
## src.chatterbox.models.t3.modules.perceiver:AttentionQKV.__init__
- calls: Dropout
- calls: __init__
- calls: setup_flash_config
- calls: super
## src.chatterbox.models.t3.modules.perceiver:AttentionQKV.combine_heads
- calls: contiguous
- calls: permute
- calls: view
## src.chatterbox.models.t3.modules.perceiver:AttentionQKV.flash_attention
- calls: scaled_dot_product_attention
- calls: sdp_kernel
## src.chatterbox.models.t3.modules.perceiver:AttentionQKV.forward
- calls: combine_heads
- calls: flash_attention
- calls: scaled_dot_product_attention
- calls: split_heads
## src.chatterbox.models.t3.modules.perceiver:AttentionQKV.scaled_dot_product_attention
- calls: dropout
- calls: einsum
- calls: float
- calls: masked_fill
- calls: softmax
## src.chatterbox.models.t3.modules.perceiver:AttentionQKV.split_heads
- calls: permute
- calls: view
## src.chatterbox.models.t3.modules.perceiver:Perceiver.__init__
- calls: AttentionBlock2
- calls: Parameter
- calls: __init__
- calls: empty
- calls: sqrt
- calls: super
- calls: uniform_
## src.chatterbox.models.t3.modules.perceiver:Perceiver.forward
- calls: attn
- calls: expand
## src.chatterbox.models.t3.modules.perceiver:RelativePositionBias.__init__
- calls: Embedding
- calls: __init__
- calls: super
## src.chatterbox.models.t3.modules.perceiver:RelativePositionBias._relative_position_bucket
- calls: abs
- calls: float
- calls: full_like
- calls: log
- calls: long
- calls: max
- calls: min
- calls: where
- calls: zeros_like
## src.chatterbox.models.t3.modules.perceiver:RelativePositionBias.forward
- calls: _relative_position_bucket
- calls: arange
- calls: rearrange
- calls: relative_attention_bias
## src.chatterbox.models.t3.t3:<module>
- calls: getLogger
## src.chatterbox.models.t3.t3:AttrDict.__init__
- calls: __init__
- calls: super
## src.chatterbox.models.t3.t3:T3.__init__
- calls: Embedding
- calls: LearnedPositionEmbeddings
- calls: Linear
- calls: LlamaConfig
- calls: LlamaModel
- calls: T3CondEnc
- calls: T3Config
- calls: __init__
- calls: setattr
- calls: super
## src.chatterbox.models.t3.t3:T3.forward
- calls: AttrDict
- calls: _ensure_BOT_EOT
- calls: forward
- calls: item
- calls: prepare_input_embeds
- calls: range
- calls: size
- calls: speech_head
- calls: text_head
- calls: zeros
## src.chatterbox.models.t3.t3:T3.inference
- calls: AlignmentStreamAnalyzer
- calls: MinPLogitsWarper
- calls: RepetitionPenaltyLogitsProcessor
- calls: T3HuggingfaceBackend
- calls: TopPLogitsWarper
- calls: _ensure_BOT_EOT
- calls: all
- calls: atleast_2d
- calls: cat
- calls: close
- calls: empty
- calls: full
- calls: get_fixed_embedding
- calls: hasattr
- calls: inference_mode
- calls: int
- calls: min_p_warper
- calls: multinomial
- calls: ones_like
- calls: patched_model
- calls: prepare_input_embeds
- calls: range
- calls: repetition_penalty_processor
- calls: size
- calls: softmax
- calls: speech_emb
- calls: squeeze
- calls: to
- calls: top_p_warper
- calls: tqdm
- calls: view
## src.chatterbox.models.t3.t3:T3.loss
- calls: arange
- calls: cross_entropy
- calls: forward
- calls: masked_fill
- calls: max
- calls: size
## src.chatterbox.models.t3.t3:T3.prepare_conditioning
- calls: cond_enc
- calls: speech_emb
- calls: speech_pos_emb
## src.chatterbox.models.t3.t3:T3.prepare_input_embeds
- calls: cat
- calls: expand
- calls: prepare_conditioning
- calls: repeat
- calls: size
- calls: speech_emb
- calls: speech_pos_emb
- calls: text_emb
- calls: text_pos_emb
- calls: zeros_like
## src.chatterbox.models.t3.t3:_ensure_BOT_EOT
- calls: int
- calls: size
- calls: sum
## src.chatterbox.models.tokenizers.tokenizer:<module>
- calls: getLogger
## src.chatterbox.models.tokenizers.tokenizer:EnTokenizer.__init__
- calls: check_vocabset_sot_eot
- calls: from_file
## src.chatterbox.models.tokenizers.tokenizer:EnTokenizer.check_vocabset_sot_eot
- calls: get_vocab
## src.chatterbox.models.tokenizers.tokenizer:EnTokenizer.decode
- calls: cpu
- calls: decode
- calls: isinstance
- calls: numpy
- calls: replace
## src.chatterbox.models.tokenizers.tokenizer:EnTokenizer.encode
- calls: encode
- calls: replace
## src.chatterbox.models.tokenizers.tokenizer:EnTokenizer.text_to_tokens
- calls: IntTensor
- calls: encode
- calls: unsqueeze
## src.chatterbox.models.voice_encoder.melspec:_amp_to_db
- calls: log10
- calls: maximum
## src.chatterbox.models.voice_encoder.melspec:_db_to_amp
- calls: power
## src.chatterbox.models.voice_encoder.melspec:_normalize
- calls: log10
## src.chatterbox.models.voice_encoder.melspec:_stft
- calls: stft
## src.chatterbox.models.voice_encoder.melspec:mel_basis
- calls: lru_cache
- calls: mel
## src.chatterbox.models.voice_encoder.melspec:melspectrogram
- calls: _amp_to_db
- calls: _normalize
- calls: _stft
- calls: abs
- calls: astype
- calls: dot
- calls: len
- calls: max
- calls: mel_basis
- calls: preemphasis
## src.chatterbox.models.voice_encoder.melspec:preemphasis
- calls: clip
- calls: lfilter
## src.chatterbox.models.voice_encoder.voice_encoder:VoiceEncoder.__init__
- calls: LSTM
- calls: Linear
- calls: Parameter
- calls: VoiceEncConfig
- calls: __init__
- calls: flatten_parameters
- calls: super
- calls: tensor
## src.chatterbox.models.voice_encoder.voice_encoder:VoiceEncoder.device
- calls: next
- calls: parameters
## src.chatterbox.models.voice_encoder.voice_encoder:VoiceEncoder.embeds_from_mels
- calls: all
- calls: asarray
- calls: inference
- calls: inference_mode
- calls: isinstance
- calls: numpy
- calls: pack
- calls: to
- calls: utt_to_spk_embed
## src.chatterbox.models.voice_encoder.voice_encoder:VoiceEncoder.embeds_from_wavs
- calls: embeds_from_mels
- calls: melspectrogram
- calls: resample
- calls: trim
## src.chatterbox.models.voice_encoder.voice_encoder:VoiceEncoder.forward
- calls: Exception
- calls: lstm
- calls: max
- calls: min
- calls: norm
- calls: proj
- calls: relu
## src.chatterbox.models.voice_encoder.voice_encoder:VoiceEncoder.inference
- calls: all
- calls: cat
- calls: ceil
- calls: chunk
- calls: concatenate
- calls: cpu
- calls: cumsum
- calls: full
- calls: get_frame_step
- calls: get_num_wins
- calls: int
- calls: is_tensor
- calls: len
- calls: max
- calls: mean
- calls: norm
- calls: range
- calls: self
- calls: size
- calls: stack
- calls: to
- calls: tolist
- calls: zip
## src.chatterbox.models.voice_encoder.voice_encoder:VoiceEncoder.utt_to_spk_embed
- calls: mean
- calls: norm
## src.chatterbox.models.voice_encoder.voice_encoder:VoiceEncoder.voice_similarity
- calls: utt_to_spk_embed
## src.chatterbox.models.voice_encoder.voice_encoder:get_frame_step
- calls: int
- calls: round
## src.chatterbox.models.voice_encoder.voice_encoder:get_num_wins
- calls: divmod
- calls: max
## src.chatterbox.models.voice_encoder.voice_encoder:pack
- calls: array
- calls: as_tensor
- calls: enumerate
- calls: full
- calls: isinstance
- calls: len
- calls: max
- calls: size
## src.chatterbox.models.voice_encoder.voice_encoder:stride_as_partials
- calls: as_strided
- calls: astype
- calls: concatenate
- calls: full
- calls: get_frame_step
- calls: get_num_wins
- calls: len
## src.chatterbox.text_utils:_split_cjk_text
- calls: append
- calls: len
- calls: search
## src.chatterbox.text_utils:_split_spaced_text
- calls: append
- calls: len
- calls: split
- calls: strip
## src.chatterbox.text_utils:detect_language
- calls: findall
- calls: len
- calls: sub
## src.chatterbox.text_utils:merge_short_sentences
- calls: append
- calls: detect_language
- calls: len
- calls: max
- calls: strip
## src.chatterbox.text_utils:split_by_word_boundary
- calls: _split_cjk_text
- calls: _split_spaced_text
- calls: append
- calls: detect_language
- calls: extend
- calls: get_punctuation_pattern
- calls: len
- calls: split
## src.chatterbox.text_utils:split_text_into_segments
- calls: append
- calls: debug
- calls: detect_language
- calls: extend
- calls: get_sentence_separators
- calls: len
- calls: merge_short_sentences
- calls: split
- calls: split_by_word_boundary
- calls: strip
## src.chatterbox.tts:ChatterboxTTS.__init__
- calls: PerthImplicitWatermarker
## src.chatterbox.tts:ChatterboxTTS._clean_artifacts
- calls: NamedTemporaryFile
- calls: RuntimeError
- calls: close
- calls: exists
- calls: getsize
- calls: join
- calls: print
- calls: run
- calls: unlink
## src.chatterbox.tts:ChatterboxTTS._clean_audio_segments_batch
- calls: NamedTemporaryFile
- calls: _clean_artifacts
- calls: append
- calls: enumerate
- calls: exists
- calls: load
- calls: print
- calls: save
- calls: unlink
## src.chatterbox.tts:ChatterboxTTS._generate_long_text_async
- calls: _clean_audio_segments_batch
- calls: _generate_segments_async
- calls: append
- calls: cat
- calls: create_silence
- calls: enumerate
- calls: extend
- calls: len
- calls: parse_pause_tags
- calls: round
- calls: split_text_into_segments
- calls: squeeze
- calls: strip
- calls: unsqueeze
## src.chatterbox.tts:ChatterboxTTS._generate_segments_async
- calls: Queue
- calls: ThreadPoolExecutor
- calls: as_completed
- calls: create_silence
- calls: empty
- calls: enumerate
- calls: get
- calls: len
- calls: min
- calls: result
- calls: submit
## src.chatterbox.tts:ChatterboxTTS._generate_segments_async.generate_worker
- calls: _generate_single_segment
- calls: create_silence
- calls: punc_norm
- calls: put
- calls: str
- calls: strip
## src.chatterbox.tts:ChatterboxTTS._generate_single_segment
- calls: apply_watermark
- calls: cpu
- calls: detach
- calls: drop_invalid_tokens
- calls: from_numpy
- calls: inference
- calls: inference_mode
- calls: numpy
- calls: pad
- calls: punc_norm
- calls: squeeze
- calls: text_to_tokens
- calls: to
- calls: unsqueeze
## src.chatterbox.tts:ChatterboxTTS.from_local
- calls: EnTokenizer
- calls: Path
- calls: S3Gen
- calls: T3
- calls: VoiceEncoder
- calls: cls
- calls: device
- calls: eval
- calls: exists
- calls: getenv
- calls: keys
- calls: load
- calls: load_file
- calls: load_state_dict
- calls: str
- calls: to
## src.chatterbox.tts:ChatterboxTTS.from_pretrained
- calls: Path
- calls: from_local
- calls: hf_hub_download
- calls: is_available
- calls: is_built
- calls: print
## src.chatterbox.tts:ChatterboxTTS.generate
- calls: NamedTemporaryFile
- calls: T3Cond
- calls: _clean_artifacts
- calls: _generate_long_text_async
- calls: _generate_single_segment
- calls: append
- calls: cat
- calls: create_silence
- calls: exists
- calls: len
- calls: load
- calls: ones
- calls: parse_pause_tags
- calls: prepare_conditionals
- calls: print
- calls: save
- calls: squeeze
- calls: strip
- calls: to
- calls: unlink
- calls: unsqueeze
## src.chatterbox.tts:ChatterboxTTS.generate_batch
- calls: T3Cond
- calls: append
- calls: apply_watermark
- calls: cpu
- calls: detach
- calls: drop_invalid_tokens
- calls: from_numpy
- calls: inference
- calls: inference_mode
- calls: max
- calls: numpy
- calls: ones
- calls: pad
- calls: prepare_conditionals
- calls: punc_norm
- calls: squeeze
- calls: stack
- calls: text_to_tokens
- calls: to
- calls: unsqueeze
## src.chatterbox.tts:ChatterboxTTS.prepare_conditionals
- calls: Conditionals
- calls: T3Cond
- calls: atleast_2d
- calls: embed_ref
- calls: embeds_from_wavs
- calls: forward
- calls: from_numpy
- calls: load
- calls: mean
- calls: ones
- calls: resample
- calls: to
## src.chatterbox.tts:Conditionals.load
- calls: T3Cond
- calls: cls
- calls: device
- calls: isinstance
- calls: load
## src.chatterbox.tts:Conditionals.save
- calls: dict
- calls: save
## src.chatterbox.tts:Conditionals.to
- calls: is_tensor
- calls: items
- calls: to
## src.chatterbox.tts:create_silence
- calls: int
- calls: zeros
## src.chatterbox.tts:parse_pause_tags
- calls: append
- calls: end
- calls: finditer
- calls: float
- calls: group
- calls: int
- calls: max
- calls: round
- calls: start
- calls: strip
- calls: sub
## src.chatterbox.tts:parse_pause_tags._repl
- calls: get
- calls: group
## src.chatterbox.tts:punc_norm
- calls: any
- calls: endswith
- calls: islower
- calls: join
- calls: len
- calls: replace
- calls: rstrip
- calls: split
- calls: upper
## src.chatterbox.vc:ChatterboxVC.__init__
- calls: PerthImplicitWatermarker
- calls: is_tensor
- calls: items
- calls: to
## src.chatterbox.vc:ChatterboxVC.from_local
- calls: Path
- calls: S3Gen
- calls: cls
- calls: device
- calls: eval
- calls: exists
- calls: load
- calls: load_file
- calls: load_state_dict
- calls: to
## src.chatterbox.vc:ChatterboxVC.from_pretrained
- calls: Path
- calls: from_local
- calls: hf_hub_download
- calls: is_available
- calls: is_built
- calls: print
## src.chatterbox.vc:ChatterboxVC.generate
- calls: apply_watermark
- calls: cpu
- calls: detach
- calls: float
- calls: from_numpy
- calls: inference
- calls: inference_mode
- calls: load
- calls: numpy
- calls: set_target_voice
- calls: squeeze
- calls: to
- calls: tokenizer
- calls: unsqueeze
## src.chatterbox.vc:ChatterboxVC.set_target_voice
- calls: embed_ref
- calls: load
## start:<module>
- calls: wrapper_main
## start:prompt_menu
- calls: enumerate
- calls: input
- calls: int
- calls: isdigit
- calls: len
- calls: print
- calls: strip
## start:wrapper_main
- calls: main
- calls: main_with_resume
- calls: prompt_menu
- calls: run_chunk_repair_tool
- calls: run_combine_only_mode
- calls: test_chunking
## tools.analyze_attention_implementation:<module>
- calls: Path
- calls: insert
- calls: main
- calls: str
## tools.analyze_attention_implementation:analyze_current_attention_config
- calls: getattr
- calls: hasattr
- calls: print
- calls: type
## tools.analyze_attention_implementation:benchmark_attention_implementations
- calls: cat
- calls: hasattr
- calls: inference
- calls: inference_mode
- calls: prepare_conditionals
- calls: print
- calls: str
- calls: strip
- calls: tensor
- calls: text_to_tokens
- calls: time
## tools.analyze_attention_implementation:check_flash_attention_availability
- calls: int
- calls: print
- calls: split
## tools.analyze_attention_implementation:create_attention_optimization_plan
- calls: append
- calls: print
## tools.analyze_attention_implementation:main
- calls: Path
- calls: analyze_current_attention_config
- calls: benchmark_attention_implementations
- calls: check_flash_attention_availability
- calls: create_attention_optimization_plan
- calls: dump
- calls: exists
- calls: get_device_name
- calls: is_available
- calls: load_optimized_model
- calls: open
- calls: prewarm_model_with_voice
- calls: print
- calls: print_exc
- calls: strftime
## tools.analyze_book_json_for_batching:<module>
- calls: Path
- calls: insert
- calls: main
- calls: str
## tools.analyze_book_json_for_batching:analyze_batching_potential
- calls: Counter
- calls: dict
- calls: len
- calls: max
- calls: print
- calls: sorted
- calls: sum
- calls: values
## tools.analyze_book_json_for_batching:calculate_batch_benefit
- calls: len
- calls: min
## tools.analyze_book_json_for_batching:create_batching_plan
- calls: append
- calls: copy
- calls: items
- calls: len
- calls: min
- calls: print
- calls: strftime
- calls: sum
## tools.analyze_book_json_for_batching:group_chunks_by_tts_params
- calls: BatchGroup
- calls: append
- calls: calculate_batch_benefit
- calls: defaultdict
- calls: dict
- calls: items
- calls: len
- calls: print
- calls: sorted
- calls: sum
- calls: tuple
## tools.analyze_book_json_for_batching:main
- calls: Path
- calls: analyze_batching_potential
- calls: create_batching_plan
- calls: exists
- calls: exit
- calls: group_chunks_by_tts_params
- calls: len
- calls: parse_book_json
- calls: print
- calls: print_analysis_report
- calls: save_analysis_results
## tools.analyze_book_json_for_batching:parse_book_json
- calls: ChunkInfo
- calls: append
- calls: enumerate
- calls: get
- calls: int
- calls: isinstance
- calls: items
- calls: len
- calls: load
- calls: open
- calls: print
- calls: split
- calls: str
- calls: strip
- calls: type
## tools.analyze_book_json_for_batching:print_analysis_report
- calls: enumerate
- calls: items
- calls: len
- calls: print
- calls: sorted
## tools.analyze_book_json_for_batching:save_analysis_results
- calls: dump
- calls: open
- calls: print
- calls: str
## tools.audio_emotion_scanner:<module>
- calls: Path
- calls: basicConfig
- calls: exit
- calls: insert
- calls: main
- calls: str
## tools.audio_emotion_scanner:AudioEmotionScanner.__init__
- calls: SentimentIntensityAnalyzer
## tools.audio_emotion_scanner:AudioEmotionScanner.analyze_transcript_segments
- calls: EmotionalSegment
- calls: append
- calls: classify_emotion
- calls: classify_speech_pattern
- calls: len
- calls: polarity_scores
- calls: strip
## tools.audio_emotion_scanner:AudioEmotionScanner.chunk_audio
- calls: append
- calls: info
- calls: int
- calls: len
- calls: load
- calls: min
## tools.audio_emotion_scanner:AudioEmotionScanner.classify_speech_pattern
- calls: lower
- calls: search
- calls: strip
## tools.audio_emotion_scanner:AudioEmotionScanner.extract_audio_segment
- calls: dirname
- calls: error
- calls: int
- calls: len
- calls: linspace
- calls: load
- calls: makedirs
- calls: max
- calls: write
## tools.audio_emotion_scanner:AudioEmotionScanner.extract_best_segments
- calls: Path
- calls: append
- calls: defaultdict
- calls: dict
- calls: enumerate
- calls: extract_audio_segment
- calls: info
- calls: items
- calls: mkdir
- calls: str
## tools.audio_emotion_scanner:AudioEmotionScanner.load_whisper_model
- calls: collect
- calls: empty_cache
- calls: error
- calls: info
- calls: is_available
- calls: load_model
- calls: load_whisper_model
- calls: memory_allocated
## tools.audio_emotion_scanner:AudioEmotionScanner.save_analysis_results
- calls: Path
- calls: append
- calls: defaultdict
- calls: dump
- calls: enumerate
- calls: info
- calls: items
- calls: len
- calls: mkdir
- calls: open
- calls: round
- calls: upper
- calls: write
## tools.audio_emotion_scanner:AudioEmotionScanner.scan_audio_file
- calls: abs
- calls: analyze_transcript_segments
- calls: append
- calls: chunk_audio
- calls: collect
- calls: defaultdict
- calls: dict
- calls: empty_cache
- calls: enumerate
- calls: extend
- calls: info
- calls: is_available
- calls: items
- calls: len
- calls: load_whisper_model
- calls: save_analysis_results
- calls: sort
- calls: transcribe_chunk
## tools.audio_emotion_scanner:AudioEmotionScanner.transcribe_chunk
- calls: TranscriptSegment
- calls: append
- calls: collect
- calls: empty_cache
- calls: endswith
- calls: error
- calls: get
- calls: index
- calls: is_available
- calls: join
- calls: len
- calls: rstrip
- calls: strip
- calls: transcribe
## tools.audio_emotion_scanner:main
- calls: ArgumentParser
- calls: AudioEmotionScanner
- calls: add_argument
- calls: exception
- calls: extract_best_segments
- calls: items
- calls: len
- calls: parse_args
- calls: print
- calls: scan_audio_file
## tools.combine_only:<module>
- calls: len
- calls: quick_combine
- calls: run_combine_only_mode
## tools.combine_only:_perform_combine_operation
- calls: add_metadata_to_m4b
- calls: combine_audio_chunks
- calls: convert_to_m4b
- calls: exists
- calls: find_book_files
- calls: int
- calls: print
- calls: stat
- calls: str
- calls: time
- calls: timedelta
- calls: unlink
## tools.combine_only:combine_audio_for_book
- calls: Path
- calls: _perform_combine_operation
- calls: exists
- calls: get_audio_files_in_directory
- calls: get_wav_duration
- calls: int
- calls: len
- calls: print
- calls: str
- calls: sum
- calls: timedelta
- calls: verify_chunk_sequence
## tools.combine_only:list_available_books_for_combine
- calls: append
- calls: exists
- calls: get_audio_files_in_directory
- calls: get_wav_duration
- calls: int
- calls: is_dir
- calls: iterdir
- calls: len
- calls: str
- calls: sum
- calls: timedelta
## tools.combine_only:quick_combine
- calls: combine_audio_chunks
- calls: convert_to_m4b
- calls: exists
- calls: get_audio_files_in_directory
- calls: len
- calls: print
- calls: rename
## tools.combine_only:run_combine_only_mode
- calls: _perform_combine_operation
- calls: enumerate
- calls: exists
- calls: get_audio_files_in_directory
- calls: get_wav_duration
- calls: glob
- calls: input
- calls: int
- calls: is_dir
- calls: iterdir
- calls: len
- calls: list
- calls: lower
- calls: print
- calls: sorted
- calls: str
- calls: strip
- calls: sum
- calls: timedelta
- calls: verify_chunk_sequence
## tools.combine_only:verify_chunk_sequence
- calls: append
- calls: group
- calls: int
- calls: match
- calls: max
- calls: range
- calls: sort
## tools.config_audit:<module>
- calls: main
## tools.config_audit:extract_flags
- calls: add
- calls: isinstance
- calls: isupper
- calls: parse
- calls: read_text
- calls: set
- calls: str
- calls: walk
## tools.config_audit:main
- calls: Path
- calls: append
- calls: dumps
- calls: exists
- calls: extract_flags
- calls: get
- calls: items
- calls: join
- calls: len
- calls: list
- calls: mkdir
- calls: print
- calls: resolve
- calls: scan_usage
- calls: set
- calls: sorted
- calls: write_text
## tools.config_audit:scan_usage
- calls: add
- calls: any
- calls: read_text
- calls: relative_to
- calls: rglob
- calls: set
- calls: str
## tools.cuda_kernel_profiler:<module>
- calls: Path
- calls: insert
- calls: main
- calls: str
## tools.cuda_kernel_profiler:CudaKernelProfiler.__init__
- calls: _get_device
## tools.cuda_kernel_profiler:CudaKernelProfiler._get_device
- calls: RuntimeError
- calls: current_device
- calls: is_available
## tools.cuda_kernel_profiler:CudaKernelProfiler._get_gpu_utilization
- calls: CudaUtilizationSnapshot
- calls: float
- calls: int
- calls: perf_counter
- calls: print
- calls: run
- calls: split
- calls: strip
## tools.cuda_kernel_profiler:CudaKernelProfiler._monitor_utilization
- calls: _get_gpu_utilization
- calls: append
- calls: sleep
## tools.cuda_kernel_profiler:CudaKernelProfiler.analyze_utilization
- calls: len
- calls: max
- calls: min
- calls: sum
## tools.cuda_kernel_profiler:CudaKernelProfiler.generate_optimization_recommendations
- calls: append
- calls: get
## tools.cuda_kernel_profiler:CudaKernelProfiler.print_summary
- calls: enumerate
- calls: print
## tools.cuda_kernel_profiler:CudaKernelProfiler.profile_inference_workload
- calls: analyze_utilization
- calls: autocast
- calls: empty_cache
- calls: hasattr
- calls: mm
- calls: perf_counter
- calls: print
- calls: randn
- calls: range
- calls: start_monitoring
- calls: stop_monitoring
- calls: synchronize
- calls: t
## tools.cuda_kernel_profiler:CudaKernelProfiler.run_comprehensive_profile
- calls: KernelProfilingResult
- calls: analyze_utilization
- calls: enumerate
- calls: extend
- calls: generate_optimization_recommendations
- calls: get
- calls: len
- calls: load_optimized_model
- calls: prewarm_model_with_voice
- calls: print
- calls: profile_inference_workload
- calls: sleep
## tools.cuda_kernel_profiler:CudaKernelProfiler.save_profile_results
- calls: asdict
- calls: dump
- calls: open
- calls: print
- calls: strftime
## tools.cuda_kernel_profiler:CudaKernelProfiler.start_monitoring
- calls: Thread
- calls: start
## tools.cuda_kernel_profiler:CudaKernelProfiler.stop_monitoring
- calls: copy
- calls: join
## tools.cuda_kernel_profiler:main
- calls: ArgumentParser
- calls: CudaKernelProfiler
- calls: add_argument
- calls: get_device_name
- calls: is_available
- calls: list_voice_samples
- calls: parse_args
- calls: print
- calls: print_exc
- calls: print_summary
- calls: run_comprehensive_profile
- calls: save_profile_results
## tools.emotion_extractor:<module>
- calls: Path
- calls: exit
- calls: insert
- calls: main
- calls: str
## tools.emotion_extractor:EmotionExtractor.__init__
- calls: FileNotFoundError
- calls: Path
- calls: exists
## tools.emotion_extractor:EmotionExtractor.analyze_audio_quality
- calls: abs
- calls: len
- calls: load
- calls: max
- calls: mean
- calls: print
- calls: rms
- calls: spectral_centroid
- calls: zero_crossing_rate
## tools.emotion_extractor:EmotionExtractor.combine_emotional_samples
- calls: Path
- calls: append
- calls: array
- calls: extend
- calls: int
- calls: items
- calls: len
- calls: load
- calls: mkdir
- calls: print
- calls: str
- calls: write
## tools.emotion_extractor:EmotionExtractor.generate_sample_report
- calls: Path
- calls: defaultdict
- calls: enumerate
- calls: items
- calls: len
- calls: open
- calls: print
- calls: sorted
- calls: upper
- calls: write
## tools.emotion_extractor:EmotionExtractor.load_chunk_data
- calls: EmotionalSegment
- calls: append
- calls: classify_emotion
- calls: exists
- calls: get
- calls: len
- calls: load
- calls: open
- calls: print
- calls: str
## tools.emotion_extractor:EmotionExtractor.select_best_segments
- calls: analyze_audio_quality
- calls: append
- calls: defaultdict
- calls: enumerate
- calls: items
- calls: len
- calls: print
- calls: sort
## tools.emotion_extractor:EmotionExtractor.select_best_segments.score_segment
- calls: abs
## tools.emotion_extractor:main
- calls: ArgumentParser
- calls: EmotionExtractor
- calls: add_argument
- calls: combine_emotional_samples
- calls: generate_sample_report
- calls: len
- calls: load_chunk_data
- calls: parse_args
- calls: print
- calls: select_best_segments
## tools.emotional_audio_enhancer:<module>
- calls: basicConfig
- calls: main
## tools.emotional_audio_enhancer:EmotionalAudioEnhancer.__del__
- calls: rmtree
## tools.emotional_audio_enhancer:EmotionalAudioEnhancer.__init__
- calls: BooleanVar
- calls: DoubleVar
- calls: IntVar
- calls: StringVar
- calls: geometry
- calls: mkdtemp
- calls: setup_ui
- calls: title
## tools.emotional_audio_enhancer:EmotionalAudioEnhancer.apply_compression
- calls: get
- calls: run
- calls: update_status
## tools.emotional_audio_enhancer:EmotionalAudioEnhancer.apply_eq
- calls: get
- calls: run
- calls: str
- calls: update_status
## tools.emotional_audio_enhancer:EmotionalAudioEnhancer.apply_formant_shift
- calls: get
- calls: run
- calls: update_status
## tools.emotional_audio_enhancer:EmotionalAudioEnhancer.apply_pitch_shift
- calls: get
- calls: run
- calls: str
- calls: update_status
## tools.emotional_audio_enhancer:EmotionalAudioEnhancer.apply_reverb
- calls: get
- calls: run
- calls: str
- calls: update_status
## tools.emotional_audio_enhancer:EmotionalAudioEnhancer.apply_tempo_change
- calls: get
- calls: run
- calls: str
- calls: update_status
## tools.emotional_audio_enhancer:EmotionalAudioEnhancer.apply_tremolo
- calls: get
- calls: run
- calls: str
- calls: update_status
## tools.emotional_audio_enhancer:EmotionalAudioEnhancer.apply_vibrato
- calls: get
- calls: run
- calls: str
- calls: update_status
## tools.emotional_audio_enhancer:EmotionalAudioEnhancer.check_audio_tools
- calls: append
- calls: run
- calls: showwarning
## tools.emotional_audio_enhancer:EmotionalAudioEnhancer.cleanup_temp_files
- calls: join
- calls: listdir
- calls: remove
## tools.emotional_audio_enhancer:EmotionalAudioEnhancer.create_tooltip
- calls: bind
## tools.emotional_audio_enhancer:EmotionalAudioEnhancer.create_tooltip.on_enter
- calls: Label
- calls: Toplevel
- calls: pack
- calls: wm_geometry
- calls: wm_overrideredirect
## tools.emotional_audio_enhancer:EmotionalAudioEnhancer.create_tooltip.on_leave
- calls: destroy
- calls: hasattr
## tools.emotional_audio_enhancer:EmotionalAudioEnhancer.load_preset
- calls: askopenfilename
- calls: items
- calls: load
- calls: open
- calls: set
- calls: showerror
- calls: showinfo
- calls: str
## tools.emotional_audio_enhancer:EmotionalAudioEnhancer.preview_audio
- calls: Popen
- calls: get
- calls: showinfo
- calls: showwarning
## tools.emotional_audio_enhancer:EmotionalAudioEnhancer.process_audio
- calls: apply_compression
- calls: apply_eq
- calls: apply_formant_shift
- calls: apply_pitch_shift
- calls: apply_reverb
- calls: apply_tempo_change
- calls: apply_tremolo
- calls: apply_vibrato
- calls: cleanup_temp_files
- calls: config
- calls: copy2
- calls: error
- calls: get
- calls: join
- calls: set
- calls: showerror
- calls: showinfo
- calls: str
- calls: sum
- calls: update_status
- calls: values
## tools.emotional_audio_enhancer:EmotionalAudioEnhancer.reset_settings
- calls: set
- calls: update_emotion_presets
- calls: values
## tools.emotional_audio_enhancer:EmotionalAudioEnhancer.save_preset
- calls: asksavefilename
- calls: dump
- calls: get
- calls: items
- calls: open
- calls: showinfo
## tools.emotional_audio_enhancer:EmotionalAudioEnhancer.select_input_file
- calls: Path
- calls: askopenfilename
- calls: get
- calls: set
- calls: str
## tools.emotional_audio_enhancer:EmotionalAudioEnhancer.select_output_file
- calls: asksavefilename
- calls: set
## tools.emotional_audio_enhancer:EmotionalAudioEnhancer.setup_ui
- calls: Button
- calls: Checkbutton
- calls: Entry
- calls: Frame
- calls: Label
- calls: LabelFrame
- calls: Progressbar
- calls: Radiobutton
- calls: Scale
- calls: check_audio_tools
- calls: config
- calls: create_tooltip
- calls: enumerate
- calls: get
- calls: grid
- calls: isinstance
- calls: pack
- calls: update_display
## tools.emotional_audio_enhancer:EmotionalAudioEnhancer.setup_ui.update_display
- calls: config
- calls: float
- calls: int
- calls: isinstance
## tools.emotional_audio_enhancer:EmotionalAudioEnhancer.start_processing
- calls: Thread
- calls: config
- calls: get
- calls: set
- calls: showerror
- calls: start
## tools.emotional_audio_enhancer:EmotionalAudioEnhancer.update_emotion_presets
- calls: get
- calls: items
- calls: set
## tools.emotional_audio_enhancer:EmotionalAudioEnhancer.update_status
- calls: after
- calls: config
- calls: info
## tools.emotional_audio_enhancer:main
- calls: EmotionalAudioEnhancer
- calls: Style
- calls: Tk
- calls: geometry
- calls: mainloop
- calls: protocol
- calls: theme_use
- calls: update_idletasks
- calls: winfo_height
- calls: winfo_screenheight
- calls: winfo_screenwidth
- calls: winfo_width
## tools.emotional_audio_enhancer:main.on_closing
- calls: cleanup_temp_files
- calls: destroy
## tools.exporters.t3_fx_export:<module>
- calls: Path
- calls: SystemExit
- calls: insert
- calls: main
- calls: resolve
- calls: str
## tools.exporters.t3_fx_export:BlockWrapper.__init__
- calls: __init__
- calls: super
## tools.exporters.t3_fx_export:BlockWrapper.forward
- calls: block
- calls: isinstance
## tools.exporters.t3_fx_export:RoPETracer.is_leaf_module
- calls: is_leaf_module
- calls: super
- calls: type
## tools.exporters.t3_fx_export:_find_ckpt_dir
- calls: Path
- calls: exists
- calls: expanduser
- calls: getenv
- calls: home
- calls: iterdir
- calls: sorted
- calls: stat
- calls: strip
## tools.exporters.t3_fx_export:_get_llama_layers
- calls: RuntimeError
- calls: append
- calls: children
- calls: endswith
- calls: getattr
- calls: hasattr
- calls: isinstance
- calls: len
- calls: list
- calls: lower
- calls: modules
- calls: type
## tools.exporters.t3_fx_export:_load_t3
- calls: FileNotFoundError
- calls: Path
- calls: T3
- calls: _find_ckpt_dir
- calls: endswith
- calls: eval
- calls: float
- calls: get
- calls: isinstance
- calls: len
- calls: load_file
- calls: load_state_dict
- calls: lower
- calls: print
- calls: relative_to
- calls: str
- calls: to
- calls: walk
## tools.exporters.t3_fx_export:main
- calls: ArgumentParser
- calls: IndexError
- calls: Path
- calls: _get_llama_layers
- calls: _load_t3
- calls: add_argument
- calls: dumps
- calls: getattr
- calls: items
- calls: join
- calls: len
- calls: makedirs
- calls: numel
- calls: op_histogram
- calls: parameters
- calls: parse_args
- calls: print
- calls: splitlines
- calls: str
- calls: sum
- calls: trace_block
- calls: type
- calls: write_text
## tools.exporters.t3_fx_export:op_histogram
- calls: dict
- calls: get
- calls: get_submodule
- calls: getattr
- calls: items
- calls: sorted
- calls: str
- calls: type
## tools.exporters.t3_fx_export:trace_block
- calls: BlockWrapper
- calls: GraphModule
- calls: RoPETracer
- calls: arange
- calls: eval
- calls: expand
- calls: no_grad
- calls: randn
- calls: to
- calls: trace
- calls: unsqueeze
- calls: wrapper
## tools.feature_run_logger:<module>
- calls: Path
- calls: main
- calls: resolve
## tools.feature_run_logger:_parse_self_qualname
- calls: len
- calls: split
- calls: startswith
## tools.feature_run_logger:_resolve_attr_chain
- calls: getattr
## tools.feature_run_logger:get_input_value
- calls: getattr
- calls: meth
## tools.feature_run_logger:instrument_window
- calls: append
- calls: get
- calls: set
- calls: setdefault
- calls: split
- calls: update
## tools.feature_run_logger:instrument_window.wrapped_init
- calls: MethodType
- calls: _parse_self_qualname
- calls: _resolve_attr_chain
- calls: callable
- calls: connect
- calls: dumps
- calls: get
- calls: getattr
- calls: hasattr
- calls: items
- calls: keys
- calls: list
- calls: make_wrapper
- calls: mkdir
- calls: original_init
- calls: print
- calls: resolve
- calls: setattr
- calls: sorted
- calls: str
- calls: values
- calls: write_text
## tools.feature_run_logger:instrument_window.wrapped_init.make_wrapper
- calls: getattr
## tools.feature_run_logger:instrument_window.wrapped_init.make_wrapper._wrapper
- calls: _orig
- calls: append
- calls: currentIndex
- calls: dumps
- calls: exists
- calls: findChildren
- calls: flush
- calls: get_input_value
- calls: getattr
- calls: getprofile
- calls: len
- calls: loads
- calls: mkdir
- calls: open
- calls: parse_input_expr
- calls: print
- calls: read_text
- calls: repr
- calls: resolve
- calls: set
- calls: setprofile
- calls: sorted
- calls: tabText
- calls: time
- calls: union
- calls: write
- calls: write_text
## tools.feature_run_logger:instrument_window.wrapped_init.make_wrapper._wrapper._prof
- calls: Path
- calls: _should_keep
- calls: add
- calls: relative_to
- calls: resolve
- calls: str
## tools.feature_run_logger:instrument_window.wrapped_init.make_wrapper._wrapper._should_keep
- calls: Path
- calls: resolve
## tools.feature_run_logger:main
- calls: SystemExit
- calls: callable
- calls: dir
- calls: exists
- calls: getattr
- calls: hasattr
- calls: import_module
- calls: instrument_window
- calls: isinstance
- calls: issubclass
- calls: loads
- calls: main
- calls: read_text
## tools.feature_run_logger:main._wrap_rbc
- calls: dumps
- calls: getprofile
- calls: len
- calls: mkdir
- calls: open
- calls: orig_rbc
- calls: print
- calls: repr
- calls: resolve
- calls: set
- calls: setprofile
- calls: sorted
- calls: str
- calls: time
- calls: write
- calls: write_text
## tools.feature_run_logger:main._wrap_rbc._keep
- calls: Path
- calls: resolve
## tools.feature_run_logger:main._wrap_rbc._prof
- calls: Path
- calls: _keep
- calls: add
- calls: relative_to
- calls: resolve
- calls: str
## tools.feature_run_logger:parse_input_expr
- calls: endswith
- calls: len
- calls: split
- calls: startswith
## tools.feature_spider:<module>
- calls: Path
- calls: main
- calls: resolve
## tools.feature_spider:build_import_graph
- calls: add
- calls: append
- calls: isinstance
- calls: list
- calls: parse
- calls: pop
- calls: read_text
- calls: rel
- calls: resolve
- calls: resolve_import
- calls: set
- calls: setdefault
- calls: str
- calls: walk
## tools.feature_spider:list_py_files
- calls: Path
- calls: any
- calls: append
- calls: endswith
- calls: walk
## tools.feature_spider:main
- calls: ArgumentParser
- calls: add_argument
- calls: append
- calls: build_import_graph
- calls: dumps
- calls: exists
- calls: items
- calls: keys
- calls: list
- calls: list_py_files
- calls: mkdir
- calls: parse_args
- calls: parse_gui_connections
- calls: print
- calls: rel
- calls: resolve
- calls: set
- calls: sorted
- calls: startswith
- calls: to_dot
- calls: values
- calls: write_text
## tools.feature_spider:module_to_path
- calls: Path
- calls: exists
- calls: replace
- calls: with_suffix
## tools.feature_spider:parse_gui_connections
- calls: append
- calls: compile
- calls: finditer
- calls: group
- calls: read_text
- calls: setdefault
## tools.feature_spider:rel
- calls: relative_to
- calls: resolve
- calls: str
## tools.feature_spider:resolve_import
- calls: append
- calls: getattr
- calls: isinstance
- calls: join
- calls: module_to_path
- calls: range
- calls: rel
- calls: split
- calls: strip
## tools.feature_spider:to_dot
- calls: append
- calls: items
- calls: join
- calls: replace
## tools.generate_from_json:<module>
- calls: Path
- calls: append
- calls: main
- calls: str
## tools.generate_from_json:main
- calls: Path
- calls: ThreadPoolExecutor
- calls: append
- calls: as_completed
- calls: ensure_voice_sample_compatibility
- calls: enumerate
- calls: exists
- calls: get
- calls: glob
- calls: input
- calls: int
- calls: is_available
- calls: len
- calls: list_voice_samples
- calls: load_chunks
- calls: load_optimized_model
- calls: log_chunk_progress
- calls: prewarm_model_with_voice
- calls: print
- calls: result
- calls: setup_book_directories
- calls: str
- calls: strip
- calls: submit
- calls: time
- calls: timedelta
- calls: unlink
## tools.gui_static_map:<module>
- calls: Path
- calls: main
- calls: resolve
## tools.gui_static_map:GUISpy.visit_Assign
- calls: generic_visit
- calls: isinstance
- calls: qualname_from_attr
## tools.gui_static_map:GUISpy.visit_Call
- calls: append
- calls: generic_visit
- calls: isinstance
- calls: qualname_from_attr
## tools.gui_static_map:GUISpy.visit_FunctionDef
- calls: generic_visit
## tools.gui_static_map:SlotAnalyzer.__init__
- calls: set
## tools.gui_static_map:SlotAnalyzer.generic_visit
- calls: iter_child_nodes
- calls: setattr
- calls: visit
## tools.gui_static_map:SlotAnalyzer.visit_Call
- calls: add
- calls: generic_visit
- calls: getattr
- calls: isinstance
- calls: qualname_from_attr
- calls: startswith
## tools.gui_static_map:build_feature_map
- calls: GUISpy
- calls: SlotAnalyzer
- calls: append
- calls: get
- calls: parse
- calls: read_text
- calls: sorted
- calls: split
- calls: str
- calls: visit
## tools.gui_static_map:main
- calls: build_feature_map
- calls: dumps
- calls: exists
- calls: mkdir
- calls: print
- calls: write_text
## tools.gui_static_map:qualname_from_attr
- calls: append
- calls: isinstance
- calls: join
- calls: reversed
## tools.gui_walker:<module>
- calls: main
- calls: setdefault
## tools.gui_walker:log
- calls: append
- calls: print
## tools.gui_walker:main
- calls: QApplication
- calls: _PkgStubFinder
- calls: count
- calls: currentWidget
- calls: dir
- calls: findChildren
- calls: getattr
- calls: import_module
- calls: insert
- calls: instance
- calls: isinstance
- calls: issubclass
- calls: len
- calls: log
- calls: main_cls
- calls: mouseClick
- calls: processEvents
- calls: qWait
- calls: range
- calls: save_log
- calls: setCurrentIndex
- calls: show
- calls: tabText
- calls: text
## tools.gui_walker:main._PkgStubFinder.find_spec
- calls: ModuleSpec
- calls: _PkgStubLoader
- calls: startswith
## tools.gui_walker:main._PkgStubLoader.create_module
- calls: ModuleType
- calls: getattr
## tools.gui_walker:main._PkgStubLoader.exec_module
- calls: setattr
- calls: startswith
## tools.gui_walker:save_log
- calls: Path
- calls: join
- calls: mkdir
- calls: resolve
- calls: write_text
## tools.headless_performance_test:<module>
- calls: Path
- calls: insert
- calls: main
- calls: str
## tools.headless_performance_test:HeadlessPerformanceTester.__init__
- calls: Path
- calls: _get_device
- calls: basicConfig
- calls: getLogger
- calls: getenv
- calls: int
## tools.headless_performance_test:HeadlessPerformanceTester._clear_memory
- calls: collect
- calls: empty_cache
## tools.headless_performance_test:HeadlessPerformanceTester._get_device
- calls: current_device
- calls: hasattr
- calls: is_available
## tools.headless_performance_test:HeadlessPerformanceTester._get_voice_file
- calls: list_voice_samples
- calls: lower
## tools.headless_performance_test:HeadlessPerformanceTester._get_vram_usage
- calls: memory_allocated
## tools.headless_performance_test:HeadlessPerformanceTester._measure_memory_fragmentation
- calls: memory_allocated
- calls: memory_reserved
## tools.headless_performance_test:HeadlessPerformanceTester._measure_tensor_contiguity
- calls: is_contiguous
- calls: named_parameters
## tools.headless_performance_test:HeadlessPerformanceTester._run_single_inference
- calls: Path
- calls: append
- calls: error
- calls: exists
- calls: len
- calls: mkdir
- calls: perf_counter
- calls: process_one_chunk
- calls: punc_norm
- calls: split
- calls: str
- calls: unlink
## tools.headless_performance_test:HeadlessPerformanceTester.print_summary
- calls: len
- calls: print
- calls: sorted
## tools.headless_performance_test:HeadlessPerformanceTester.run_full_test_suite
- calls: extend
- calls: info
- calls: test_batching_configurations
- calls: test_memory_optimizations
- calls: test_torch_compile_configurations
## tools.headless_performance_test:HeadlessPerformanceTester.save_results
- calls: asdict
- calls: dump
- calls: info
- calls: open
- calls: strftime
## tools.headless_performance_test:HeadlessPerformanceTester.test_batching_configurations
- calls: info
## tools.headless_performance_test:HeadlessPerformanceTester.test_memory_optimizations
- calls: info
## tools.headless_performance_test:HeadlessPerformanceTester.test_torch_compile_configurations
- calls: PerformanceResult
- calls: _clear_memory
- calls: _get_voice_file
- calls: _get_vram_usage
- calls: _measure_memory_fragmentation
- calls: _measure_tensor_contiguity
- calls: _run_single_inference
- calls: append
- calls: compile
- calls: error
- calls: extend
- calls: get
- calls: hasattr
- calls: info
- calls: len
- calls: load_optimized_model
- calls: max
- calls: perf_counter
- calls: prewarm_model_with_voice
- calls: range
- calls: sum
## tools.headless_performance_test:main
- calls: ArgumentParser
- calls: HeadlessPerformanceTester
- calls: add_argument
- calls: parse_args
- calls: print_summary
- calls: run_full_test_suite
- calls: save_results
- calls: str
- calls: test_batching_configurations
- calls: test_memory_optimizations
- calls: test_torch_compile_configurations
## tools.measure_token_memory:<module>
- calls: Path
- calls: insert
- calls: main
- calls: str
## tools.measure_token_memory:analyze_queue_capacity
- calls: append
- calls: int
- calls: len
- calls: mean
- calls: min
- calls: print
## tools.measure_token_memory:generate_test_tokens
- calls: append
- calls: cat
- calls: cpu
- calls: drop_invalid_tokens
- calls: enumerate
- calls: get_memory_usage
- calls: inference
- calls: inference_mode
- calls: len
- calls: measure_tensor_size
- calls: prepare_conditionals
- calls: print
- calls: strip
- calls: tensor
- calls: text_to_tokens
## tools.measure_token_memory:get_memory_usage
- calls: Process
- calls: memory_info
- calls: virtual_memory
## tools.measure_token_memory:main
- calls: analyze_queue_capacity
- calls: append
- calls: dump
- calls: generate_test_tokens
- calls: get_device_name
- calls: get_memory_usage
- calls: is_available
- calls: len
- calls: list_voice_samples
- calls: load_optimized_model
- calls: open
- calls: prewarm_model_with_voice
- calls: print
- calls: simulate_queue_transfer_overhead
## tools.measure_token_memory:measure_tensor_size
- calls: element_size
- calls: is_tensor
- calls: list
- calls: numel
- calls: str
## tools.measure_token_memory:simulate_queue_transfer_overhead
- calls: Event
- calls: cuda
- calls: elapsed_time
- calls: empty_cache
- calls: len
- calls: print
- calls: record
- calls: synchronize
## tools.ort_gpu_diagnose:<module>
- calls: SystemExit
- calls: main
## tools.ort_gpu_diagnose:find_shadowing_modules
- calls: append
- calls: join
- calls: startswith
- calls: walk
## tools.ort_gpu_diagnose:main
- calls: ArgumentParser
- calls: add_argument
- calls: maybe_run_onnx_test
- calls: parse_args
- calls: print_next_steps_hint
- calls: show_python_env
- calls: show_shadowing
- calls: try_import_onnxruntime
- calls: try_nvidia_smi
- calls: try_torch_cuda
## tools.ort_gpu_diagnose:maybe_run_onnx_test
- calls: append
- calls: dirname
- calls: join
- calls: print
- calls: print_header
- calls: run
- calls: str
## tools.ort_gpu_diagnose:print_header
- calls: print
## tools.ort_gpu_diagnose:print_next_steps_hint
- calls: dedent
- calls: print
- calls: print_header
- calls: strip
## tools.ort_gpu_diagnose:show_python_env
- calls: get
- calls: getsitepackages
- calls: next
- calls: print
- calls: print_header
- calls: replace
## tools.ort_gpu_diagnose:show_shadowing
- calls: abspath
- calls: append
- calls: commonpath
- calls: find_shadowing_modules
- calls: get
- calls: getcwd
- calls: print
- calls: print_header
## tools.ort_gpu_diagnose:try_import_onnxruntime
- calls: find_spec
- calls: get_all_providers
- calls: get_available_providers
- calls: getattr
- calls: hasattr
- calls: print
- calls: print_header
- calls: repr
## tools.ort_gpu_diagnose:try_nvidia_smi
- calls: check_output
- calls: enumerate
- calls: len
- calls: print
- calls: print_header
- calls: repr
- calls: splitlines
- calls: which
## tools.ort_gpu_diagnose:try_torch_cuda
- calls: device_count
- calls: get_device_name
- calls: getattr
- calls: is_available
- calls: print
- calls: print_header
- calls: repr
## tools.path_checker:<module>
- calls: Path
- calls: append
- calls: main
- calls: str
## tools.path_checker:main
- calls: check_existing_audiobook_paths
- calls: enumerate
- calls: len
- calls: print
## tools.quick_batching_test:<module>
- calls: Path
- calls: insert
- calls: quick_batch_test
- calls: str
## tools.quick_batching_test:quick_batch_test
- calls: append
- calls: empty_cache
- calls: hasattr
- calls: inference
- calls: inference_mode
- calls: len
- calls: load_optimized_model
- calls: prewarm_model_with_voice
- calls: print
- calls: sum
- calls: time
- calls: tokenize_batch
- calls: tokenize_single
## tools.quick_batching_test:quick_batch_test.tokenize_batch
- calls: append
- calls: cat
- calls: full
- calls: max
- calls: squeeze
- calls: stack
- calls: tokenize_single
## tools.quick_batching_test:quick_batch_test.tokenize_single
- calls: cat
- calls: strip
- calls: tensor
- calls: text_to_tokens
## tools.run_tts_once:<module>
- calls: Path
- calls: insert
- calls: main
- calls: resolve
- calls: str
## tools.run_tts_once:default_texts
- calls: len
- calls: max
- calls: min
## tools.run_tts_once:main
- calls: Path
- calls: append
- calls: default_texts
- calls: dumps
- calls: enumerate
- calls: exists
- calls: exit
- calls: float
- calls: generate
- calls: get_autocast
- calls: getattr
- calls: hasattr
- calls: int
- calls: is_available
- calls: len
- calls: load_optimized_model
- calls: max
- calls: no_grad
- calls: parse_args
- calls: prepare_conditionals
- calls: print
- calls: range
- calls: read_text
- calls: round
- calls: set_trt_env
- calls: splitlines
- calls: strip
- calls: sum
- calls: time
## tools.run_tts_once:parse_args
- calls: ArgumentParser
- calls: add_argument
- calls: parse_args
## tools.run_tts_once:set_trt_env
- calls: pop
## tools.runtime_summarize:<module>
- calls: main
## tools.runtime_summarize:main
- calls: Path
- calls: add
- calls: dumps
- calls: exists
- calls: get
- calls: items
- calls: list
- calls: loads
- calls: open
- calls: print
- calls: resolve
- calls: set
- calls: sorted
- calls: write_text
## tools.safe_archiver:<module>
- calls: main
## tools.safe_archiver:apply
- calls: append
- calls: dumps
- calls: exists
- calls: mkdir
- calls: move
- calls: str
- calls: write_text
## tools.safe_archiver:load_candidates
- calls: exists
- calls: loads
- calls: read_text
## tools.safe_archiver:load_reached
- calls: exists
- calls: loads
- calls: read_text
- calls: set
## tools.safe_archiver:main
- calls: ArgumentParser
- calls: Path
- calls: add_argument
- calls: apply
- calls: len
- calls: load_candidates
- calls: load_reached
- calls: parse_args
- calls: print
- calls: resolve
- calls: restore
## tools.safe_archiver:restore
- calls: exists
- calls: get
- calls: loads
- calls: mkdir
- calls: move
- calls: read_text
- calls: str
## tools.spider_ci:<module>
- calls: main
## tools.spider_ci:detect_cycles
- calls: dfs
- calls: keys
- calls: list
## tools.spider_ci:detect_cycles.dfs
- calls: append
- calls: dfs
- calls: get
- calls: index
- calls: pop
## tools.spider_ci:load_graph
- calls: exists
- calls: loads
- calls: read_text
## tools.spider_ci:main
- calls: ArgumentParser
- calls: Path
- calls: SystemExit
- calls: add_argument
- calls: detect_cycles
- calls: dumps
- calls: len
- calls: load_graph
- calls: mkdir
- calls: parse_args
- calls: print
- calls: resolve
- calls: sum
- calls: values
- calls: write_text
## tools.spider_run:<module>
- calls: Path
- calls: main
- calls: resolve
## tools.spider_run:main
- calls: ArgumentParser
- calls: add_argument
- calls: copy
- calls: exists
- calls: get
- calls: join
- calls: lower
- calls: mkdir
- calls: parse_args
- calls: pop
- calls: print
- calls: run
- calls: str
- calls: strip
- calls: unlink
## tools.spider_run:run
- calls: call
- calls: join
- calls: print
## tools.test_attention_optimizations:<module>
- calls: Path
- calls: insert
- calls: main
- calls: str
## tools.test_attention_optimizations:benchmark_attention_implementation
- calls: cat
- calls: collect
- calls: empty_cache
- calls: hasattr
- calls: inference
- calls: inference_mode
- calls: memory_allocated
- calls: prepare_conditionals
- calls: print
- calls: str
- calls: strip
- calls: tensor
- calls: text_to_tokens
- calls: time
## tools.test_attention_optimizations:install_flash_attention
- calls: print
- calls: run
## tools.test_attention_optimizations:main
- calls: Path
- calls: dump
- calls: exists
- calls: get
- calls: get_device_name
- calls: install_flash_attention
- calls: is_available
- calls: load_optimized_model
- calls: open
- calls: prewarm_model_with_voice
- calls: print
- calls: print_exc
- calls: strftime
- calls: test_grouped_query_attention
- calls: test_sdpa_attention
## tools.test_attention_optimizations:test_grouped_query_attention
- calls: benchmark_attention_implementation
- calls: print
## tools.test_attention_optimizations:test_sdpa_attention
- calls: benchmark_attention_implementation
- calls: print
## tools.test_batched_inference:<module>
- calls: Path
- calls: insert
- calls: main
- calls: str
## tools.test_batched_inference:analyze_batch_results
- calls: append
- calls: float
- calls: get
- calls: len
- calls: max
- calls: min
- calls: print
- calls: sum
## tools.test_batched_inference:benchmark_batched_inference
- calls: collect
- calls: empty_cache
- calls: hasattr
- calls: inference
- calls: inference_mode
- calls: len
- calls: memory_allocated
- calls: str
- calls: time
- calls: tokenize_text_batch
## tools.test_batched_inference:benchmark_sequential_inference
- calls: append
- calls: cat
- calls: collect
- calls: empty_cache
- calls: enumerate
- calls: hasattr
- calls: inference
- calls: inference_mode
- calls: len
- calls: memory_allocated
- calls: str
- calls: strip
- calls: tensor
- calls: text_to_tokens
- calls: time
## tools.test_batched_inference:load_batching_plan
- calls: exists
- calls: load
- calls: open
- calls: print
## tools.test_batched_inference:main
- calls: Path
- calls: analyze_batch_results
- calls: append
- calls: dump
- calls: enumerate
- calls: exists
- calls: exit
- calls: get
- calls: isinstance
- calls: len
- calls: load
- calls: load_batching_plan
- calls: load_optimized_model
- calls: open
- calls: prepare_text_batches
- calls: prewarm_model_with_voice
- calls: print
- calls: run_batch_comparison
- calls: str
- calls: strftime
## tools.test_batched_inference:prepare_text_batches
- calls: append
- calls: enumerate
- calls: len
- calls: print
## tools.test_batched_inference:run_batch_comparison
- calls: benchmark_batched_inference
- calls: benchmark_sequential_inference
- calls: len
- calls: print
## tools.test_batched_inference:tokenize_text_batch
- calls: append
- calls: cat
- calls: full
- calls: max
- calls: squeeze
- calls: stack
- calls: strip
- calls: tensor
- calls: text_to_tokens
## tools.test_compile_fix:<module>
- calls: Path
- calls: insert
- calls: main
- calls: str
## tools.test_compile_fix:clear_memory
- calls: collect
- calls: empty_cache
- calls: is_available
## tools.test_compile_fix:get_test_voice
- calls: list_voice_samples
## tools.test_compile_fix:main
- calls: clear_memory
- calls: get_test_voice
- calls: hasattr
- calls: is_available
- calls: load_optimized_model
- calls: lower
- calls: prewarm_model_with_voice
- calls: print
- calls: print_exc
- calls: run_quick_inference_test
- calls: str
- calls: type
## tools.test_compile_fix:run_quick_inference_test
- calls: hasattr
- calls: perf_counter
- calls: print
- calls: type
## tools.test_cuda_integration:<module>
- calls: Path
- calls: insert
- calls: main
- calls: str
## tools.test_cuda_integration:clear_memory
- calls: collect
- calls: empty_cache
- calls: is_available
## tools.test_cuda_integration:get_test_voice
- calls: list_voice_samples
## tools.test_cuda_integration:main
- calls: test_cuda_optimizer_integration
## tools.test_cuda_integration:test_cuda_optimizer_integration
- calls: apply_optimizations
- calls: clear_memory
- calls: create_cuda_optimizer
- calls: create_optimized_tensor
- calls: current_device
- calls: get_device_name
- calls: get_optimization_summary
- calls: get_test_voice
- calls: get_tts_optimizer
- calls: is_available
- calls: load_optimized_model
- calls: optimize_tensor_memory_layout
- calls: prewarm_model_with_voice
- calls: print
- calls: print_exc
- calls: randn
- calls: restore_original_methods
## tools.test_dual_queue_pipeline:<module>
- calls: Path
- calls: insert
- calls: main
- calls: str
## tools.test_dual_queue_pipeline:DualQueueManager.__init__
- calls: Event
- calls: Queue
## tools.test_dual_queue_pipeline:DualQueueManager.get_queue_status
- calls: empty
- calls: full
- calls: qsize
## tools.test_dual_queue_pipeline:DualQueueManager.switch_queues
- calls: append
- calls: print
- calls: set
- calls: time
## tools.test_dual_queue_pipeline:analyze_pipeline_performance
- calls: len
- calls: max
- calls: min
- calls: print
- calls: sum
## tools.test_dual_queue_pipeline:load_test_content
- calls: FileNotFoundError
- calls: Path
- calls: exists
- calls: len
- calls: open
- calls: print
- calls: read
- calls: stat
- calls: str
## tools.test_dual_queue_pipeline:main
- calls: DualQueueManager
- calls: Thread
- calls: analyze_pipeline_performance
- calls: dump
- calls: get_device_name
- calls: is_available
- calls: join
- calls: len
- calls: load_optimized_model
- calls: load_test_content
- calls: open
- calls: prepare_text_chunks
- calls: prewarm_model_with_voice
- calls: print
- calls: print_exc
- calls: s3gen_worker
- calls: set
- calls: start
- calls: strftime
- calls: sum
- calls: t3_worker
- calls: time
## tools.test_dual_queue_pipeline:monitor_gpu_utilization
- calls: append
- calls: int
- calls: is_set
- calls: print
- calls: run
- calls: sleep
- calls: strip
- calls: time
## tools.test_dual_queue_pipeline:prepare_text_chunks
- calls: append
- calls: enumerate
- calls: isinstance
- calls: len
- calls: print
- calls: sentence_chunk_text
- calls: split
- calls: strip
## tools.test_dual_queue_pipeline:s3gen_worker
- calls: append
- calls: cuda
- calls: empty
- calls: empty_cache
- calls: get
- calls: inference
- calls: inference_mode
- calls: is_set
- calls: len
- calls: print
- calls: range
- calls: task_done
- calls: time
## tools.test_dual_queue_pipeline:t3_worker
- calls: append
- calls: cat
- calls: cpu
- calls: drop_invalid_tokens
- calls: enumerate
- calls: full
- calls: inference
- calls: inference_mode
- calls: is_set
- calls: len
- calls: prepare_conditionals
- calls: print
- calls: put
- calls: strip
- calls: switch_queues
- calls: tensor
- calls: text_to_tokens
- calls: time
## tools.test_flash_attention:<module>
- calls: Path
- calls: insert
- calls: str
- calls: test_flash_attention_vs_eager
## tools.test_flash_attention:benchmark_attention_implementation
- calls: cat
- calls: collect
- calls: empty_cache
- calls: hasattr
- calls: inference
- calls: inference_mode
- calls: memory_allocated
- calls: prepare_conditionals
- calls: print
- calls: str
- calls: strip
- calls: tensor
- calls: text_to_tokens
- calls: time
## tools.test_flash_attention:load_model_with_attention
- calls: TTS_Engine
- calls: hasattr
- calls: print
## tools.test_flash_attention:test_flash_attention_vs_eager
- calls: Path
- calls: benchmark_attention_implementation
- calls: collect
- calls: dump
- calls: empty_cache
- calls: exists
- calls: get
- calls: get_device_name
- calls: is_available
- calls: load_optimized_model
- calls: open
- calls: prewarm_model_with_voice
- calls: print
- calls: print_exc
- calls: strftime
## tools.test_kv_cache_optimization:<module>
- calls: Path
- calls: insert
- calls: main
- calls: str
## tools.test_kv_cache_optimization:analyze_kv_cache_usage
- calls: append
- calls: cat
- calls: collect
- calls: element_size
- calls: empty_cache
- calls: hasattr
- calls: inference_mode
- calls: isinstance
- calls: len
- calls: memory_allocated
- calls: min
- calls: numel
- calls: prepare_conditionals
- calls: print
- calls: range
- calls: str
- calls: strip
- calls: t3_model
- calls: tensor
- calls: text_to_tokens
- calls: time
## tools.test_kv_cache_optimization:benchmark_contiguous_cache_inference
- calls: print
## tools.test_kv_cache_optimization:benchmark_standard_inference
- calls: cat
- calls: collect
- calls: empty_cache
- calls: inference
- calls: inference_mode
- calls: prepare_conditionals
- calls: print
- calls: strip
- calls: tensor
- calls: text_to_tokens
- calls: time
## tools.test_kv_cache_optimization:main
- calls: Path
- calls: analyze_kv_cache_usage
- calls: dump
- calls: exists
- calls: get
- calls: get_device_name
- calls: is_available
- calls: load_optimized_model
- calls: open
- calls: prewarm_model_with_voice
- calls: print
- calls: print_exc
- calls: recommend_kv_optimizations
- calls: strftime
- calls: test_cache_memory_layout
## tools.test_kv_cache_optimization:recommend_kv_optimizations
- calls: append
- calls: get
- calls: len
- calls: max
- calls: print
- calls: sum
## tools.test_kv_cache_optimization:test_cache_memory_layout
- calls: benchmark_contiguous_cache_inference
- calls: benchmark_standard_inference
- calls: print
## tools.test_kv_cache_optimization:test_kv_cache_preallocation
- calls: benchmark_standard_inference
- calls: print
## tools.test_s3gen_cpu_performance:<module>
- calls: Path
- calls: insert
- calls: main
- calls: str
## tools.test_s3gen_cpu_performance:analyze_pipeline_potential
- calls: get
- calls: len
- calls: max
- calls: print
- calls: sum
## tools.test_s3gen_cpu_performance:clear_memory
- calls: collect
- calls: empty_cache
- calls: is_available
## tools.test_s3gen_cpu_performance:create_test_speech_tokens
- calls: append
- calls: cat
- calls: drop_invalid_tokens
- calls: enumerate
- calls: inference
- calls: inference_mode
- calls: len
- calls: prepare_conditionals
- calls: print
- calls: strip
- calls: tensor
- calls: text_to_tokens
- calls: time
## tools.test_s3gen_cpu_performance:get_memory_usage
- calls: Process
- calls: get_device_properties
- calls: is_available
- calls: memory_allocated
- calls: memory_info
- calls: memory_reserved
- calls: virtual_memory
## tools.test_s3gen_cpu_performance:get_test_voice
- calls: list_voice_samples
## tools.test_s3gen_cpu_performance:main
- calls: analyze_pipeline_potential
- calls: clear_memory
- calls: create_test_speech_tokens
- calls: dump
- calls: get_device_name
- calls: get_test_voice
- calls: is_available
- calls: len
- calls: load_optimized_model
- calls: open
- calls: prewarm_model_with_voice
- calls: print
- calls: str
- calls: strftime
- calls: test_s3gen_cpu_performance
- calls: test_s3gen_gpu_performance
## tools.test_s3gen_cpu_performance:test_s3gen_cpu_performance
- calls: append
- calls: cpu
- calls: enumerate
- calls: get_memory_usage
- calls: hasattr
- calls: inference
- calls: inference_mode
- calls: is_tensor
- calls: items
- calls: len
- calls: print
- calls: time
- calls: to
## tools.test_s3gen_cpu_performance:test_s3gen_gpu_performance
- calls: append
- calls: enumerate
- calls: get_memory_usage
- calls: hasattr
- calls: inference
- calls: inference_mode
- calls: len
- calls: print
- calls: time
- calls: to
## tools.test_sequence_batching:<module>
- calls: Path
- calls: insert
- calls: main
- calls: str
## tools.test_sequence_batching:benchmark_individual_processing
- calls: append
- calls: enumerate
- calls: generate
- calls: get
- calls: len
- calls: print
- calls: time
## tools.test_sequence_batching:benchmark_sequence_batching
- calls: analyze_batching_potential
- calls: create_sequence_batch_processor
- calls: len
- calls: print
- calls: process_chunks_with_sequence_batching
- calls: time
## tools.test_sequence_batching:clear_memory
- calls: collect
- calls: empty_cache
- calls: is_available
## tools.test_sequence_batching:compare_performance
- calls: print
## tools.test_sequence_batching:create_test_chunks
- calls: append
- calls: copy
- calls: len
- calls: range
## tools.test_sequence_batching:get_test_voice
- calls: list_voice_samples
## tools.test_sequence_batching:main
- calls: benchmark_individual_processing
- calls: benchmark_sequence_batching
- calls: clear_memory
- calls: compare_performance
- calls: create_test_chunks
- calls: dump
- calls: get_device_name
- calls: get_test_voice
- calls: is_available
- calls: items
- calls: len
- calls: load_optimized_model
- calls: open
- calls: prewarm_model_with_voice
- calls: print
- calls: sleep
- calls: str
- calls: strftime
## tools.test_sequential_pipeline:<module>
- calls: Path
- calls: insert
- calls: main
- calls: str
## tools.test_sequential_pipeline:clear_t3_from_memory
- calls: collect
- calls: empty_cache
- calls: get_memory_usage
- calls: hasattr
- calls: print
## tools.test_sequential_pipeline:get_memory_usage
- calls: Process
- calls: is_available
- calls: memory_allocated
- calls: memory_info
- calls: memory_reserved
- calls: virtual_memory
## tools.test_sequential_pipeline:main
- calls: Path
- calls: append
- calls: clear_t3_from_memory
- calls: dump
- calls: exists
- calls: get_device_name
- calls: is_available
- calls: isinstance
- calls: len
- calls: load_optimized_model
- calls: open
- calls: phase_1_t3_processing
- calls: phase_2_s3gen_processing
- calls: prewarm_model_with_voice
- calls: print
- calls: print_exc
- calls: read
- calls: sentence_chunk_text
- calls: strftime
- calls: time
## tools.test_sequential_pipeline:monitor_gpu_simple
- calls: int
- calls: run
- calls: strip
## tools.test_sequential_pipeline:phase_1_t3_processing
- calls: append
- calls: cat
- calls: cpu
- calls: drop_invalid_tokens
- calls: enumerate
- calls: get_memory_usage
- calls: inference
- calls: inference_mode
- calls: len
- calls: monitor_gpu_simple
- calls: prepare_conditionals
- calls: print
- calls: strip
- calls: sum
- calls: tensor
- calls: text_to_tokens
- calls: time
## tools.test_sequential_pipeline:phase_2_s3gen_processing
- calls: append
- calls: cuda
- calls: empty_cache
- calls: enumerate
- calls: inference
- calls: inference_mode
- calls: len
- calls: locals
- calls: monitor_gpu_simple
- calls: print
- calls: sum
- calls: time
## tools.test_unified_device_mode:<module>
- calls: Path
- calls: insert
- calls: main
- calls: str
## tools.test_unified_device_mode:analyze_model_devices
- calls: hasattr
- calls: items
- calls: len
- calls: list
- calls: next
- calls: parameters
- calls: print
- calls: set
- calls: str
- calls: values
## tools.test_unified_device_mode:check_device_configuration
- calls: getenv
- calls: items
- calls: print
## tools.test_unified_device_mode:clear_memory
- calls: collect
- calls: empty_cache
- calls: is_available
## tools.test_unified_device_mode:get_test_voice
- calls: list_voice_samples
## tools.test_unified_device_mode:main
- calls: analyze_model_devices
- calls: check_device_configuration
- calls: clear_memory
- calls: get_device_name
- calls: get_test_voice
- calls: getenv
- calls: is_available
- calls: load_optimized_model
- calls: lower
- calls: prewarm_model_with_voice
- calls: print
- calls: test_basic_inference
- calls: test_batch_inference
## tools.test_unified_device_mode:test_basic_inference
- calls: generate
- calls: hasattr
- calls: prepare_conditionals
- calls: print
- calls: print_exc
- calls: time
## tools.test_unified_device_mode:test_batch_inference
- calls: generate_batch
- calls: len
- calls: print
- calls: print_exc
- calls: time
## tools.trace_pipeline_flow:<module>
- calls: Path
- calls: insert
- calls: main
- calls: str
## tools.trace_pipeline_flow:analyze_pipeline_bottlenecks
- calls: items
- calls: print
- calls: sort
- calls: sum
- calls: values
## tools.trace_pipeline_flow:main
- calls: Path
- calls: analyze_pipeline_bottlenecks
- calls: dump
- calls: exists
- calls: get_device_name
- calls: is_available
- calls: items
- calls: keys
- calls: len
- calls: load_optimized_model
- calls: max
- calls: open
- calls: prewarm_model_with_voice
- calls: print
- calls: print_exc
- calls: sorted
- calls: strftime
- calls: sum
- calls: trace_multiple_chunks
- calls: trace_single_chunk_pipeline
- calls: values
## tools.trace_pipeline_flow:monitor_gpu
- calls: int
- calls: run
- calls: split
- calls: strip
## tools.trace_pipeline_flow:trace_multiple_chunks
- calls: append
- calls: enumerate
- calls: len
- calls: max
- calls: min
- calls: monitor_gpu
- calls: print
- calls: sum
- calls: time
- calls: trace_single_chunk_pipeline
## tools.trace_pipeline_flow:trace_single_chunk_pipeline
- calls: append
- calls: cat
- calls: cpu
- calls: detach
- calls: drop_invalid_tokens
- calls: inference
- calls: inference_mode
- calls: monitor_gpu
- calls: numpy
- calls: prepare_conditionals
- calls: print
- calls: squeeze
- calls: strip
- calls: sum
- calls: tensor
- calls: text_to_tokens
- calls: time
- calls: to
- calls: values
## tools.trace_t3_inference:<module>
- calls: Path
- calls: insert
- calls: main
- calls: str
## tools.trace_t3_inference:main
- calls: Path
- calls: append
- calls: dump
- calls: enumerate
- calls: exists
- calls: get_device_name
- calls: is_available
- calls: items
- calls: keys
- calls: len
- calls: load_optimized_model
- calls: open
- calls: prewarm_model_with_voice
- calls: print
- calls: print_exc
- calls: sort
- calls: sorted
- calls: strftime
- calls: sum
- calls: trace_t3_inference_detailed
- calls: values
## tools.trace_t3_inference:monitor_gpu
- calls: int
- calls: run
- calls: split
- calls: strip
## tools.trace_t3_inference:patched_t3_inference_with_timing
- calls: AlignmentStreamAnalyzer
- calls: MinPLogitsWarper
- calls: RepetitionPenaltyLogitsProcessor
- calls: T3HuggingfaceBackend
- calls: TopPLogitsWarper
- calls: _ensure_BOT_EOT
- calls: all
- calls: append
- calls: atleast_2d
- calls: cat
- calls: close
- calls: empty
- calls: full
- calls: get
- calls: get_fixed_embedding
- calls: hasattr
- calls: int
- calls: locals
- calls: min_p_warper
- calls: monitor_gpu
- calls: multinomial
- calls: ones_like
- calls: patched_model
- calls: prepare_input_embeds
- calls: print
- calls: range
- calls: repetition_penalty_processor
- calls: size
- calls: softmax
- calls: speech_emb
- calls: squeeze
- calls: time
- calls: to
- calls: top_p_warper
- calls: view
## tools.trace_t3_inference:trace_t3_inference_detailed
- calls: cat
- calls: patched_t3_inference_with_timing
- calls: prepare_conditionals
- calls: print
- calls: strip
- calls: tensor
- calls: text_to_tokens
## tools.tts_trt_benchmark:<module>
- calls: Path
- calls: insert
- calls: main
- calls: resolve
- calls: str
## tools.tts_trt_benchmark:main
- calls: Path
- calls: dumps
- calls: exists
- calls: exit
- calls: parse_args
- calls: print
- calls: round
- calls: run_once
- calls: summarize
## tools.tts_trt_benchmark:main.summarize
- calls: get
## tools.tts_trt_benchmark:parse_args
- calls: ArgumentParser
- calls: add_argument
- calls: parse_args
## tools.tts_trt_benchmark:run_once
- calls: RuntimeError
- calls: copy
- calls: endswith
- calls: find
- calls: len
- calls: loads
- calls: pop
- calls: reversed
- calls: rfind
- calls: run
- calls: splitlines
- calls: startswith
- calls: str
- calls: strip
## tools.xtts_finetune_extractor:<module>
- calls: Path
- calls: basicConfig
- calls: exit
- calls: insert
- calls: main
- calls: print
- calls: str
## tools.xtts_finetune_extractor:SentimentIntensityAnalyzer.polarity_scores
- calls: lower
- calls: max
- calls: min
- calls: sum
## tools.xtts_finetune_extractor:XTTSFinetuneExtractor.__init__
- calls: FileNotFoundError
- calls: Path
- calls: SentimentIntensityAnalyzer
- calls: exists
## tools.xtts_finetune_extractor:XTTSFinetuneExtractor.analyze_audio_file
- calls: XTTSAudioFile
- calls: assess_audio_quality
- calls: classify_emotion
- calls: len
- calls: load
- calls: polarity_scores
- calls: warning
## tools.xtts_finetune_extractor:XTTSFinetuneExtractor.analyze_directory_structure
- calls: Path
- calls: any
- calls: append
- calls: endswith
- calls: info
- calls: items
- calls: keys
- calls: len
- calls: lower
- calls: rglob
- calls: rstrip
- calls: str
- calls: walk
## tools.xtts_finetune_extractor:XTTSFinetuneExtractor.assess_audio_quality
- calls: abs
- calls: append
- calls: len
- calls: max
- calls: mean
- calls: min
- calls: rms
- calls: spectral_centroid
- calls: zero_crossing_rate
## tools.xtts_finetune_extractor:XTTSFinetuneExtractor.create_voice_samples
- calls: Path
- calls: append
- calls: array
- calls: extend
- calls: info
- calls: int
- calls: items
- calls: len
- calls: load
- calls: mkdir
- calls: str
- calls: warning
- calls: write
## tools.xtts_finetune_extractor:XTTSFinetuneExtractor.extract_audio_files
- calls: Path
- calls: analyze_audio_file
- calls: append
- calls: enumerate
- calls: info
- calls: keys
- calls: len
## tools.xtts_finetune_extractor:XTTSFinetuneExtractor.generate_report
- calls: Path
- calls: defaultdict
- calls: enumerate
- calls: info
- calls: items
- calls: len
- calls: mean
- calls: open
- calls: title
- calls: upper
- calls: write
## tools.xtts_finetune_extractor:XTTSFinetuneExtractor.load_metadata
- calls: endswith
- calls: info
- calls: isinstance
- calls: items
- calls: len
- calls: load
- calls: open
- calls: reader
- calls: split
- calls: strip
- calls: warning
## tools.xtts_finetune_extractor:XTTSFinetuneExtractor.select_best_samples
- calls: append
- calls: defaultdict
- calls: info
- calls: items
- calls: len
- calls: sort
## tools.xtts_finetune_extractor:XTTSFinetuneExtractor.select_best_samples.score_file
- calls: abs
## tools.xtts_finetune_extractor:main
- calls: ArgumentParser
- calls: Path
- calls: XTTSFinetuneExtractor
- calls: add_argument
- calls: analyze_directory_structure
- calls: create_voice_samples
- calls: exception
- calls: extract_audio_files
- calls: generate_report
- calls: get
- calls: items
- calls: len
- calls: load_metadata
- calls: parse_args
- calls: print
- calls: select_best_samples
## utils.generate_from_json:<module>
- calls: Path
- calls: append
- calls: main
- calls: str
## utils.generate_from_json:main
- calls: Path
- calls: ThreadPoolExecutor
- calls: append
- calls: as_completed
- calls: ensure_voice_sample_compatibility
- calls: enumerate
- calls: exists
- calls: get
- calls: glob
- calls: input
- calls: int
- calls: is_available
- calls: len
- calls: list_voice_samples
- calls: load_chunks
- calls: load_optimized_model
- calls: log_chunk_progress
- calls: prepare_conditionals
- calls: print
- calls: result
- calls: setup_book_directories
- calls: str
- calls: strip
- calls: submit
- calls: time
- calls: timedelta
- calls: unlink
## wrapper.chunk_loader:load_chunks
- calls: get
- calls: isinstance
- calls: load
- calls: open
## wrapper.chunk_loader:load_metadata
- calls: get
- calls: isinstance
- calls: load
- calls: open
- calls: print
## wrapper.chunk_loader:save_chunks
- calls: OrderedDict
- calls: append
- calls: copy
- calls: deepcopy
- calls: dump
- calls: isinstance
- calls: items
- calls: open
- calls: print
- calls: replace
- calls: sub
## wrapper.chunk_player:play_chunk_audio
- calls: exists
- calls: print
- calls: run
## wrapper.chunk_revisions:accept_revision
- calls: Path
- calls: exists
- calls: mkdir
- calls: move
- calls: print
- calls: str
## wrapper.chunk_search:search_chunks
- calls: append
- calls: lower
## wrapper.chunk_synthesizer:find_voice_file_by_name
- calls: list_voice_samples
- calls: lower
- calls: print
## wrapper.chunk_synthesizer:get_original_voice_from_filename
- calls: Path
- calls: glob
- calls: group
- calls: print
- calls: search
## wrapper.chunk_synthesizer:get_original_voice_from_log
- calls: Path
- calls: exists
- calls: open
- calls: print
- calls: split
- calls: startswith
- calls: strip
## wrapper.chunk_synthesizer:get_tts_params_for_chunk
- calls: get
- calls: get_float_input
- calls: print
## wrapper.chunk_synthesizer:get_tts_params_for_chunk.get_float_input
- calls: float
- calls: input
- calls: print
- calls: strip
## wrapper.chunk_synthesizer:synthesize_chunk
- calls: BytesIO
- calls: Path
- calls: apply_smart_fade_memory
- calls: cpu
- calls: detach
- calls: detect_voice_for_book
- calls: dim
- calls: empty_cache
- calls: ensure_voice_sample_compatibility
- calls: export
- calls: find_voice_file_by_name
- calls: from_wav
- calls: generate
- calls: get
- calls: get_tts_params_for_chunk
- calls: is_available
- calls: list_voice_samples
- calls: load_optimized_model
- calls: no_grad
- calls: numpy
- calls: prewarm_model_with_voice
- calls: print
- calls: print_exc
- calls: process_audio_with_trimming_and_silence
- calls: seek
- calls: smart_audio_validation_memory
- calls: squeeze
- calls: str
- calls: trim_audio_endpoint
- calls: unsqueeze
- calls: write
## wrapper.chunk_tool:run_chunk_repair_tool
- calls: Path
- calls: accept_revision
- calls: enumerate
- calls: exists
- calls: float
- calls: get
- calls: get_float_input
- calls: input
- calls: int
- calls: isdigit
- calls: len
- calls: load_chunks
- calls: lower
- calls: play_chunk_audio
- calls: print
- calls: save_chunks
- calls: search_chunks
- calls: select_book_for_repair
- calls: split
- calls: str
- calls: strip
- calls: synthesize_chunk
## wrapper.chunk_tool:run_chunk_repair_tool.get_float_input
- calls: float
- calls: input
- calls: print
- calls: strip
## wrapper.chunk_tool:select_book_for_repair
- calls: Path
- calls: any
- calls: append
- calls: enumerate
- calls: exists
- calls: glob
- calls: input
- calls: int
- calls: is_dir
- calls: iterdir
- calls: len
- calls: print
- calls: replace
- calls: strip
