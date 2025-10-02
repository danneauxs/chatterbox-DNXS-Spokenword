# speed.chatterbox_gui

> ChatterboxTTS GUI Interface

## Public API

### Classes
- **NoScrollSpinBox**  
  Methods: wheelEvent
- **NoScrollDoubleSpinBox**  
  Methods: wheelEvent
- **StructuredStatusPanel** — Structured status panel widget for TTS operations  
  Methods: setup_ui, update_status, reset
- **ChunkingTestWindow** — Popup window to display chunking test results  
  Methods: set_chunking_results, copy_to_clipboard
- **ProcessThread** — Thread to run background processes without blocking GUI  
  Methods: parse_and_emit_status, parse_chunk_progress, run
- **ChatterboxMainWindow**  
  Methods: closeEvent, test_audio_system_startup, create_convert_book_tab, handle_micro_batching_toggle, handle_vader_toggle, reload_tab1_from_config, create_config_tab, create_resume_tab, create_combine_tab, create_prepare_text_tab, create_test_chunking_tab, create_repair_tool_tab, create_json_generate_tab, create_output_area_widget, create_output_area, browse_book_folder, populate_text_files, browse_voice_file, play_voice_sample, stop_voice_sample, handle_asr_toggle, analyze_system, update_asr_models, apply_preset, browse_combine_book, browse_prepare_text, browse_json_file, update_status_display, start_conversion, run_book_conversion, refresh_incomplete_books, resume_processing, combine_audio, on_combine_finished, prepare_text, on_text_prep_finished, test_chunking, refresh_repair_books, load_chunks_for_repair, detect_and_update_voice_info, refresh_available_voices, search_chunks_for_repair, select_chunk_for_repair, update_repair_chunk_display, save_chunk_changes, play_original_chunk, resynthesize_chunk, play_revised_chunk, accept_chunk_revision, generate_from_json, browse_m4b_file, regenerate_m4b, on_conversion_finished, reset_config_defaults, save_original_config_values, setup_config_change_tracking, mark_config_changed, check_unsaved_config_changes, on_tab_changed, save_config_to_file, play_m4b_file, detect_and_update_device_status, log_output, update_tab1_status_panel, update_tab8_status_panel, refresh_json_voices, browse_json_file, generate_from_json, json_generation_finished, play_json_audio, pause_json_audio, stop_json_audio, rewind_json_audio, ff_json_audio, json_slider_pressed, json_slider_released, create_voice_analyzer_tab, try_install_voice_analyzer_deps, build_voice_analyzer_gui, setup_analyzer_scores_tab, setup_analyzer_plots_tab, setup_analyzer_recommendations_tab, setup_analyzer_comparison_tab, setup_analyzer_autofix_tab, add_analyzer_files, remove_analyzer_file, clear_analyzer_files, on_analyzer_file_selected, analyze_selected_voice, analyze_all_voices, start_voice_analysis, update_analyzer_result_display, create_score_widget, clear_analyzer_scores_grid, clear_analyzer_displays, update_analyzer_ui_state, select_all_analyzer_fixes, select_recommended_analyzer_fixes, clear_all_analyzer_fixes, update_analyzer_fix_ui_state, apply_analyzer_fixes, export_analyzer_plot, export_analyzer_report, update_analyzer_visualization, update_analyzer_comparison_plot, create_audio_output_analyzer_tab, setup_output_quality_tab, setup_output_technical_tab, setup_output_standards_tab, setup_output_chapter_tab, setup_output_comparison_tab, add_output_files, remove_output_file, clear_output_files, on_output_file_selected, analyze_selected_output, analyze_all_outputs, start_output_analysis, analyze_audiobook_file, estimate_bitrate, update_output_result_display, create_output_score_widget, clear_output_quality_grid, clear_output_displays, update_output_comparison_plot, update_output_analyzer_ui_state, export_output_report, export_output_plot
- **GUIOutput**  
  Methods: write, flush

### Functions
- **main**
- **wheelEvent**
- **wheelEvent**
- **setup_ui**
- **update_status** — Update status panel fields
- **reset** — Reset all fields to default state
- **set_chunking_results** — Set the chunking test results
- **copy_to_clipboard** — Copy results to clipboard
- **parse_and_emit_status** — Parse clean status text and emit structured data
- **parse_chunk_progress** — Parse chunk progress from stdout text
- **run**
- **closeEvent** — Handle GUI close event - cleanup audio playback
- **test_audio_system_startup** — Test audio system on startup and show status
- **create_convert_book_tab** — Tab 1: Convert a book (GenTTS) - Main functionality
- **handle_micro_batching_toggle**
- **handle_vader_toggle** — When VADER is turned off, also turn off micro-batching (Tab 2) and config flags.
- **reload_tab1_from_config**
- **create_config_tab** — Tab 2: Configuration Settings
- **create_resume_tab** — Tab 3: Resume from specific chunk
- **create_combine_tab** — Tab 4: Combine audio chunks
- **create_prepare_text_tab** — Tab 5: Prepare text file for chunking
- **create_test_chunking_tab** — Tab 6: Test chunking logic
- **create_repair_tool_tab** — Tab 7: Chunk repair tool
- **create_json_generate_tab** — Tab 8: Generate from JSON with voice selection and playback controls
- **create_output_area_widget** — Create output/log area as a widget for splitter
- **create_output_area** — Legacy method for backwards compatibility
- **browse_book_folder**
- **populate_text_files** — Populate text file combo box when book folder is selected
- **browse_voice_file**
- **play_voice_sample** — Play the selected voice sample
- **stop_voice_sample** — Stop voice sample playback
- **handle_asr_toggle** — Show/hide ASR configuration when ASR is toggled
- **analyze_system** — Analyze system capabilities and display summary
- **update_asr_models** — Update ASR model display based on selected level
- **apply_preset**
- **browse_combine_book**
- **browse_prepare_text**
- **browse_json_file**
- **update_status_display** — Update the status display - now uses TTS generation status panel
- **start_conversion** — Button click handler - validates inputs and starts conversion
- **run_book_conversion** — Execute the actual book conversion with all GUI parameters
- **refresh_incomplete_books** — Refresh list of incomplete books
- **resume_processing** — Resume processing selected book
- **combine_audio** — Combine audio chunks
- **on_combine_finished** — Handle combine completion
- **prepare_text** — Prepare text for chunking
- **on_text_prep_finished** — Handle text preparation completion
- **test_chunking** — Test chunking logic and show results in popup window
- **refresh_repair_books** — Refresh the list of available books for repair
- **load_chunks_for_repair** — Load chunks for the selected book
- **detect_and_update_voice_info** — Detect and display voice information for the current book
- **refresh_available_voices** — Refresh voice candidates for current book (not all voices)
- **search_chunks_for_repair** — Search for chunks containing the specified text
- **select_chunk_for_repair** — Select a chunk for editing
- **update_repair_chunk_display** — Update the chunk editor display with current chunk data
- **save_chunk_changes** — Save changes to the current chunk
- **play_original_chunk** — Play the original audio for the current chunk
- **resynthesize_chunk** — Resynthesize the current chunk with updated parameters
- **play_revised_chunk** — Play the revised audio for the current chunk
- **accept_chunk_revision** — Accept the revision by replacing original with revised audio
- **generate_from_json** — Generate audio from JSON
- **browse_m4b_file** — Browse and select a WAV or M4B file for regeneration or playback
- **regenerate_m4b** — Regenerate M4B file with new speed setting from WAV or M4B file
- **on_conversion_finished** — Handle conversion completion
- **reset_config_defaults** — Reload Tab 2 values from the saved config (defaults = current saved config).
- **save_original_config_values** — Save original config values to track changes
- **setup_config_change_tracking** — Connect all config widgets to change tracking
- **mark_config_changed** — Mark config as having unsaved changes
- **check_unsaved_config_changes** — Check if there are unsaved config changes and prompt user
- **on_tab_changed** — Handle tab change - check for unsaved config changes when leaving config tab
- **save_config_to_file** — Save current GUI settings to config file
- **play_m4b_file** — Open audio file in system default player with priority system
- **detect_and_update_device_status** — Detect and update device status in the GUI using comprehensive CUDA checking
- **log_output** — Add message to output log with ANSI code filtering
- **update_tab1_status_panel** — Update Tab 1 structured status panel with parsed data
- **update_tab8_status_panel** — Update Tab 8 structured status panel with parsed data
- **refresh_json_voices** — Refresh the list of all available voices for JSON generation
- **browse_json_file** — Browse for JSON chunks file
- **generate_from_json** — Generate audiobook from JSON file with selected voice
- **json_generation_finished** — Handle completion of JSON generation
- **play_json_audio** — Play the generated audiobook
- **pause_json_audio** — Pause/Resume audio playback
- **stop_json_audio** — Stop audio playback
- **rewind_json_audio** — Rewind 10 seconds (simplified implementation)
- **ff_json_audio** — Fast forward 10 seconds (simplified implementation)
- **json_slider_pressed** — Handle slider press for seeking
- **json_slider_released** — Handle slider release for seeking
- **create_voice_analyzer_tab** — Tab 9: Voice Sample Analyzer for TTS Suitability
- **try_install_voice_analyzer_deps** — Try to auto-install voice analyzer dependencies
- **build_voice_analyzer_gui** — Build the complete voice analyzer GUI directly in the tab
- **setup_analyzer_scores_tab** — Setup the scores display tab
- **setup_analyzer_plots_tab** — Setup the visualization tab with matplotlib
- **setup_analyzer_recommendations_tab** — Setup the recommendations tab
- **setup_analyzer_comparison_tab** — Setup the comparison tab
- **setup_analyzer_autofix_tab** — Setup the auto-fix tab with comprehensive audio processing fixes
- **add_analyzer_files** — Add voice sample files
- **remove_analyzer_file** — Remove selected file
- **clear_analyzer_files** — Clear all files
- **on_analyzer_file_selected** — Handle file selection
- **analyze_selected_voice** — Analyze selected voice file
- **analyze_all_voices** — Analyze all voice files
- **start_voice_analysis** — Start voice analysis
- **update_analyzer_result_display** — Update the display with analysis result
- **create_score_widget** — Create a score display widget
- **clear_analyzer_scores_grid** — Clear the scores grid
- **clear_analyzer_displays** — Clear all result displays
- **update_analyzer_ui_state** — Update UI element states
- **select_all_analyzer_fixes** — Select all fix checkboxes
- **select_recommended_analyzer_fixes** — Select recommended fixes based on current analysis
- **clear_all_analyzer_fixes** — Clear all fix checkboxes
- **update_analyzer_fix_ui_state** — Update the fix UI state based on selections
- **apply_analyzer_fixes** — Apply selected audio fixes using the comprehensive Auto-Fix system
- **export_analyzer_plot** — Export current analysis plot
- **export_analyzer_report** — Export current analysis report
- **update_analyzer_visualization** — Update the analysis plots
- **update_analyzer_comparison_plot** — Update comparison plot for multiple samples
- **create_audio_output_analyzer_tab** — Tab 10: Audio Output Analyzer for finished audiobooks
- **setup_output_quality_tab** — Setup the quality scores tab for output analysis
- **setup_output_technical_tab** — Setup the technical analysis tab
- **setup_output_standards_tab** — Setup the production standards compliance tab
- **setup_output_chapter_tab** — Setup the chapter analysis tab
- **setup_output_comparison_tab** — Setup the output comparison tab
- **add_output_files** — Add audiobook files for analysis
- **remove_output_file** — Remove selected audiobook file
- **clear_output_files** — Clear all audiobook files
- **on_output_file_selected** — Handle audiobook file selection
- **analyze_selected_output** — Analyze selected audiobook file
- **analyze_all_outputs** — Analyze all audiobook files
- **start_output_analysis** — Start audiobook output analysis
- **analyze_audiobook_file** — Comprehensive analysis of audiobook file
- **estimate_bitrate** — Estimate bitrate from file size and duration
- **update_output_result_display** — Update the display with audiobook analysis result
- **create_output_score_widget** — Create a score display widget for output analysis
- **clear_output_quality_grid** — Clear the quality scores grid
- **clear_output_displays** — Clear all output analysis displays
- **update_output_comparison_plot** — Update comparison plot for multiple audiobook files
- **update_output_analyzer_ui_state** — Update UI element states for output analyzer
- **export_output_report** — Export audiobook analysis report
- **export_output_plot** — Export audiobook quality plot
- **write**
- **flush**
- **debug_scroll**
- **progress_callback**

## Imports (local guesses)
- PyQt5.QtCore, PyQt5.QtGui, PyQt5.QtWidgets, collections, config, config.config, contextlib, copy, datetime, gc, importlib, interface, io, librosa, logging, matplotlib.backends.backend_qt5agg, matplotlib.figure, matplotlib.pyplot, modules.file_manager, modules.gui_json_generator, modules.progress_tracker, modules.resume_handler, modules.system_detector, modules.text_processor, modules.tts_engine, modules.voice_detector, numpy, os, pathlib, platform, pygame, re, subprocess, sys, threading, tools.combine_only, torch, traceback, utils.generate_from_json, voice_analyzer.analyzer, voice_analyzer.audio_processor, voice_analyzer.visualizer, winsound, wrapper.chunk_loader, wrapper.chunk_player, wrapper.chunk_revisions, wrapper.chunk_search, wrapper.chunk_synthesizer, wrapper.chunk_tool

## Side-effect signals
- env_reads, subprocess, sys_exit

## Entrypoint
- Contains `if __name__ == '__main__':` block