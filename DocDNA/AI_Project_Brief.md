# AI Project Brief

This document summarizes the repository in a way an AI agent can load quickly without scanning every file each time.

## High-Level Overview

- **Modules discovered**: 143
- **Framework signals**: argparse(16)
- **Side-effect signals**: subprocess(20), sys_exit(11), env_reads(4), file_io(2)

## Suggested Load Order (Topological, best-effort)

 > Uses local import relationships; `<cycle>` indicates a dependency cycle.
- tools.emotion_extractor
- modules.dual_model_optimizer
- tools.tts_trt_benchmark
- src.chatterbox.models.s3gen.s3gen
- src.chatterbox.models.s3gen.decoder
- src.chatterbox.models.s3gen.flow
- src.chatterbox.models.voice_encoder.voice_encoder
- tools.runtime_summarize
- modules.vram_bandwidth_monitor
- src.chatterbox.models.t3.__init__
- tools.safe_archiver
- src.chatterbox.models.voice_encoder.melspec
- tools.gui_static_map
- src.chatterbox.__init__
- tools.cuda_kernel_profiler
- gradio_tabs.__init__
- src.chatterbox.models.s3gen.transformer.positionwise_feed_forward
- tools.test_batched_inference
- src.chatterbox.models.s3gen.f0_predictor
- tools.test_compile_fix
- src.chatterbox.models.s3gen.utils.class_utils
- modules.token_usage_logger
- src.chatterbox.models.s3gen.matcha.flow_matching
- src.chatterbox.models.s3gen.matcha.decoder
- tools.test_dual_queue_pipeline
- modules.dual_tts_engine
- src.chatterbox.models.s3gen.__init__
- scripts.make_backup
- launch
- tools.trace_t3_inference
- tools.test_sequence_batching
- tools.exporters.t3_fx_export
- tools.gui_walker
- src.chatterbox.models.s3gen.transformer.subsampling
- modules.advanced_optimizations
- src.chatterbox.models.s3gen.utils.mask
- tools.analyze_book_json_for_batching
- tools.test_cuda_integration
- src.chatterbox.models.t3.modules.learned_pos_emb
- tools.test_kv_cache_optimization
- modules.onnx_optimizer
- src.chatterbox.models.s3gen.hifigan
- tools.test_sequential_pipeline
- modules.dual_t3_engine
- src.chatterbox.models.s3gen.matcha.transformer
- tools.path_checker
- tools.generate_from_json
- tools.spider_ci
- tools.headless_performance_test
- tools.audio_emotion_scanner
- src.chatterbox.models.s3gen.flow_matching
- modules.t3_minimal_export
- src.chatterbox.models.s3gen.xvector
- src.chatterbox.models.s3gen.transformer.upsample_encoder
- tools.xtts_finetune_extractor
- tools.feature_run_logger
- src.chatterbox.models.voice_encoder.__init__
- src.chatterbox.models.s3tokenizer.s3tokenizer
- tools.spider_run
- src.chatterbox.models.s3gen.transformer.convolution
- src.chatterbox.models.t3.modules.perceiver
- tools.measure_token_memory
- tools.analyze_attention_implementation
- src.chatterbox.models.s3gen.const
- modules.gpu_bandwidth_monitor
- src.chatterbox.models.tokenizers.__init__
- tools.run_tts_once
- src.chatterbox.models.s3gen.transformer.encoder_layer
- tools.test_attention_optimizations
- src.chatterbox.models.s3gen.transformer.__init__
- src.chatterbox.models.s3gen.transformer.activation
- Voice_Samples.mel
- start
- tools.trace_pipeline_flow
- modules.batch_processor
- chatterbox_gui
- config.__init__
- src.chatterbox.models.s3gen.transformer.attention
- tools.ort_gpu_diagnose
- tools.quick_batching_test
- tools.test_flash_attention
- tools.test_s3gen_cpu_performance
- gradio_launcher
- src.chatterbox.text_utils
- src.chatterbox.vc
- modules.bandwidth_monitor
- src.chatterbox.models.voice_encoder.config
- tools.config_audit
- gradio_app
- src.chatterbox.models.t3.modules.t3_config
- tools.test_unified_device_mode
- src.chatterbox.models.s3tokenizer.__init__
- src.chatterbox.models.s3gen.utils.mel
- modules.token_calculator
- tools.emotional_audio_enhancer
- src.chatterbox.models.s3gen.transformer.embedding
- tools.feature_spider
- src.chatterbox.models.s3gen.matcha.text_encoder
- src.chatterbox.models.t3.inference.alignment_stream_analyzer
- src.chatterbox.models.t3.inference.t3_hf_backend
- modules.sequence_batch_processor
- src.chatterbox.models.t3.llama_configs
- modules.cuda_optimizer
- modules.t3_standalone_export
- main_launcher
- modules.token_analyzer
- modules.simple_token_logger
- gradio_main_interface
- src.chatterbox.models.tokenizers.tokenizer
- src.chatterbox.models.t3.t3
- src.chatterbox.models.t3.modules.cond_enc
- interface
- wrapper.chunk_tool
- utils.generate_from_json
- gradio_tabs.tab1_convert_book
- gradio_tabs.tab6_settings
- gradio_tabs.tab5_prepare_text
- gradio_tabs.tab4_combine_audio
- gradio_tabs.tab7_chunk_tools
- gradio_tabs.tab8_json_generate
- gradio_tabs.tab2_configuration
- modules.resume_handler
- modules.system_detector
- modules.path_validator
- wrapper.chunk_synthesizer
- wrapper.chunk_player
- wrapper.chunk_revisions
- wrapper.chunk_editor
- wrapper.chunk_search
- modules.gui_json_generator
- tools.combine_only
- <cycle>
- modules.audio_processor
- modules.file_manager
- modules.voice_detector
- modules.asr_manager
- wrapper.chunk_loader
- modules.terminal_logger
- config.config
- modules.tts_engine
- modules.progress_tracker
- modules.text_processor
- modules.real_tts_optimizer
- src.chatterbox.tts

## Potential Entrypoints

- Voice_Samples.mel, chatterbox_gui, gradio_app, gradio_launcher, gradio_main_interface, gradio_tabs.tab1_convert_book, gradio_tabs.tab2_configuration, gradio_tabs.tab4_combine_audio, gradio_tabs.tab5_prepare_text, gradio_tabs.tab7_chunk_tools, gradio_tabs.tab8_json_generate, interface, launch, main_launcher, modules.asr_manager, modules.batch_processor, modules.dual_model_optimizer, modules.gui_json_generator, modules.system_detector, modules.t3_minimal_export, modules.t3_standalone_export, scripts.make_backup, start, tools.analyze_attention_implementation, tools.analyze_book_json_for_batching, tools.audio_emotion_scanner, tools.combine_only, tools.config_audit, tools.cuda_kernel_profiler, tools.emotion_extractor, tools.emotional_audio_enhancer, tools.exporters.t3_fx_export, tools.feature_run_logger, tools.feature_spider, tools.generate_from_json, tools.gui_static_map, tools.gui_walker, tools.headless_performance_test, tools.measure_token_memory, tools.ort_gpu_diagnose, tools.path_checker, tools.quick_batching_test, tools.run_tts_once, tools.runtime_summarize, tools.safe_archiver, tools.spider_ci, tools.spider_run, tools.test_attention_optimizations, tools.test_batched_inference, tools.test_compile_fix, tools.test_cuda_integration, tools.test_dual_queue_pipeline, tools.test_flash_attention, tools.test_kv_cache_optimization, tools.test_s3gen_cpu_performance, tools.test_sequence_batching, tools.test_sequential_pipeline, tools.test_unified_device_mode, tools.trace_pipeline_flow, tools.trace_t3_inference, tools.tts_trt_benchmark, tools.xtts_finetune_extractor, utils.generate_from_json

## Roots & Leaves (by local imports)

- **Roots (imported by none)**: Voice_Samples.mel, chatterbox_gui, config.__init__, gradio_app, gradio_launcher, gradio_tabs.__init__, launch, modules.advanced_optimizations, modules.bandwidth_monitor, modules.batch_processor, modules.dual_model_optimizer, modules.dual_t3_engine, modules.dual_tts_engine, modules.gpu_bandwidth_monitor, modules.onnx_optimizer, modules.t3_minimal_export, modules.token_calculator, modules.token_usage_logger, modules.vram_bandwidth_monitor, scripts.make_backup, src.chatterbox.__init__, src.chatterbox.models.s3gen.__init__, src.chatterbox.models.s3gen.const, src.chatterbox.models.s3gen.decoder, src.chatterbox.models.s3gen.f0_predictor, src.chatterbox.models.s3gen.flow, src.chatterbox.models.s3gen.flow_matching, src.chatterbox.models.s3gen.hifigan, src.chatterbox.models.s3gen.matcha.decoder, src.chatterbox.models.s3gen.matcha.flow_matching, src.chatterbox.models.s3gen.matcha.text_encoder, src.chatterbox.models.s3gen.matcha.transformer, src.chatterbox.models.s3gen.s3gen, src.chatterbox.models.s3gen.transformer.__init__, src.chatterbox.models.s3gen.transformer.activation, src.chatterbox.models.s3gen.transformer.attention, src.chatterbox.models.s3gen.transformer.convolution, src.chatterbox.models.s3gen.transformer.embedding, src.chatterbox.models.s3gen.transformer.encoder_layer, src.chatterbox.models.s3gen.transformer.positionwise_feed_forward, src.chatterbox.models.s3gen.transformer.subsampling, src.chatterbox.models.s3gen.transformer.upsample_encoder, src.chatterbox.models.s3gen.utils.class_utils, src.chatterbox.models.s3gen.utils.mask, src.chatterbox.models.s3gen.utils.mel, src.chatterbox.models.s3gen.xvector, src.chatterbox.models.s3tokenizer.__init__, src.chatterbox.models.s3tokenizer.s3tokenizer, src.chatterbox.models.t3.__init__, src.chatterbox.models.t3.modules.learned_pos_emb, src.chatterbox.models.t3.modules.perceiver, src.chatterbox.models.t3.modules.t3_config, src.chatterbox.models.tokenizers.__init__, src.chatterbox.models.voice_encoder.__init__, src.chatterbox.models.voice_encoder.config, src.chatterbox.models.voice_encoder.melspec, src.chatterbox.models.voice_encoder.voice_encoder, src.chatterbox.text_utils, src.chatterbox.vc, start, tools.analyze_attention_implementation, tools.analyze_book_json_for_batching, tools.audio_emotion_scanner, tools.config_audit, tools.cuda_kernel_profiler, tools.emotion_extractor, tools.emotional_audio_enhancer, tools.exporters.t3_fx_export, tools.feature_run_logger, tools.feature_spider, tools.generate_from_json, tools.gui_static_map, tools.gui_walker, tools.headless_performance_test, tools.measure_token_memory, tools.ort_gpu_diagnose, tools.path_checker, tools.quick_batching_test, tools.run_tts_once, tools.runtime_summarize, tools.safe_archiver, tools.spider_ci, tools.spider_run, tools.test_attention_optimizations, tools.test_batched_inference, tools.test_compile_fix, tools.test_cuda_integration, tools.test_dual_queue_pipeline, tools.test_flash_attention, tools.test_kv_cache_optimization, tools.test_s3gen_cpu_performance, tools.test_sequence_batching, tools.test_sequential_pipeline, tools.test_unified_device_mode, tools.trace_pipeline_flow, tools.trace_t3_inference, tools.tts_trt_benchmark, tools.xtts_finetune_extractor
- **Leaves (import nothing local)**: Voice_Samples.mel, config.__init__, config.config, gradio_tabs.__init__, launch, modules.advanced_optimizations, modules.bandwidth_monitor, modules.cuda_optimizer, modules.gpu_bandwidth_monitor, modules.onnx_optimizer, modules.sequence_batch_processor, modules.simple_token_logger, modules.token_calculator, modules.token_usage_logger, modules.vram_bandwidth_monitor, scripts.make_backup, src.chatterbox.__init__, src.chatterbox.models.s3gen.__init__, src.chatterbox.models.s3gen.const, src.chatterbox.models.s3gen.decoder, src.chatterbox.models.s3gen.f0_predictor, src.chatterbox.models.s3gen.flow, src.chatterbox.models.s3gen.flow_matching, src.chatterbox.models.s3gen.hifigan, src.chatterbox.models.s3gen.matcha.decoder, src.chatterbox.models.s3gen.matcha.flow_matching, src.chatterbox.models.s3gen.matcha.text_encoder, src.chatterbox.models.s3gen.matcha.transformer, src.chatterbox.models.s3gen.s3gen, src.chatterbox.models.s3gen.transformer.__init__, src.chatterbox.models.s3gen.transformer.activation, src.chatterbox.models.s3gen.transformer.attention, src.chatterbox.models.s3gen.transformer.convolution, src.chatterbox.models.s3gen.transformer.embedding, src.chatterbox.models.s3gen.transformer.encoder_layer, src.chatterbox.models.s3gen.transformer.positionwise_feed_forward, src.chatterbox.models.s3gen.transformer.subsampling, src.chatterbox.models.s3gen.transformer.upsample_encoder, src.chatterbox.models.s3gen.utils.class_utils, src.chatterbox.models.s3gen.utils.mask, src.chatterbox.models.s3gen.utils.mel, src.chatterbox.models.s3gen.xvector, src.chatterbox.models.s3tokenizer.__init__, src.chatterbox.models.s3tokenizer.s3tokenizer, src.chatterbox.models.t3.__init__, src.chatterbox.models.t3.inference.alignment_stream_analyzer, src.chatterbox.models.t3.inference.t3_hf_backend, src.chatterbox.models.t3.llama_configs, src.chatterbox.models.t3.modules.cond_enc, src.chatterbox.models.t3.modules.learned_pos_emb, src.chatterbox.models.t3.modules.perceiver, src.chatterbox.models.t3.modules.t3_config, src.chatterbox.models.t3.t3, src.chatterbox.models.tokenizers.__init__, src.chatterbox.models.tokenizers.tokenizer, src.chatterbox.models.voice_encoder.__init__, src.chatterbox.models.voice_encoder.config, src.chatterbox.models.voice_encoder.melspec, src.chatterbox.models.voice_encoder.voice_encoder, src.chatterbox.text_utils, src.chatterbox.vc, tools.analyze_book_json_for_batching, tools.audio_emotion_scanner, tools.config_audit, tools.emotion_extractor, tools.emotional_audio_enhancer, tools.feature_run_logger, tools.feature_spider, tools.gui_static_map, tools.gui_walker, tools.ort_gpu_diagnose, tools.runtime_summarize, tools.safe_archiver, tools.spider_ci, tools.spider_run, tools.tts_trt_benchmark, tools.xtts_finetune_extractor, wrapper.chunk_editor, wrapper.chunk_loader, wrapper.chunk_player, wrapper.chunk_search

## Module Summaries

### Voice_Samples.mel
- Side-effect signals: sys_exit
- Functions: process_audio_file, main
- Imports (local guess): librosa, os, pydub, shutil, soundfile, sys
- Details: files/Voice_Samples.mel.md
### chatterbox_gui
> ChatterboxTTS GUI Interface
- Side-effect signals: env_reads, subprocess, sys_exit
- Classes: NoScrollSpinBox, NoScrollDoubleSpinBox, StructuredStatusPanel, ChunkingTestWindow, ProcessThread, ChatterboxMainWindow, GUIOutput
- Functions: main, wheelEvent, wheelEvent, setup_ui, update_status, reset, set_chunking_results, copy_to_clipboard, parse_and_emit_status, parse_chunk_progress, run, init_token_logging, closeEvent, test_audio_system_startup, create_convert_book_tab, handle_micro_batching_toggle, handle_vader_toggle, reload_tab1_from_config, create_config_tab, create_resume_tab, create_combine_tab, create_prepare_text_tab, create_test_chunking_tab, create_repair_tool_tab, create_json_generate_tab, create_output_area_widget, create_output_area, browse_book_folder, populate_text_files, browse_voice_file, play_voice_sample, stop_voice_sample, handle_asr_toggle, analyze_system, update_asr_models, apply_preset, browse_combine_book, browse_prepare_text, browse_json_file, update_status_display, start_conversion, run_book_conversion, refresh_incomplete_books, resume_processing, combine_audio, combine_audio_wav_only, on_combine_finished, on_combine_wav_finished, prepare_text, on_text_prep_finished, test_chunking, refresh_repair_books, load_chunks_for_repair, detect_and_update_voice_info, refresh_available_voices, search_chunks_for_repair, search_chunks_by_number, select_chunk_for_repair, update_repair_chunk_display, save_chunk_changes, play_original_chunk, resynthesize_chunk, play_revised_chunk, accept_chunk_revision, generate_from_json, browse_m4b_file, regenerate_m4b, on_conversion_finished, reset_config_defaults, save_original_config_values, setup_config_change_tracking, mark_config_changed, check_unsaved_config_changes, on_tab_changed, save_config_to_file, play_m4b_file, detect_and_update_device_status, log_output, update_tab1_status_panel, update_tab8_status_panel, refresh_json_voices, browse_json_file, generate_from_json, json_generation_finished, play_json_audio, pause_json_audio, stop_json_audio, rewind_json_audio, ff_json_audio, json_slider_pressed, json_slider_released, create_voice_analyzer_tab, try_install_voice_analyzer_deps, build_voice_analyzer_gui, setup_analyzer_scores_tab, setup_analyzer_plots_tab, setup_analyzer_recommendations_tab, setup_analyzer_comparison_tab, setup_analyzer_autofix_tab, add_analyzer_files, remove_analyzer_file, clear_analyzer_files, on_analyzer_file_selected, analyze_selected_voice, analyze_all_voices, start_voice_analysis, update_analyzer_result_display, create_score_widget, clear_analyzer_scores_grid, clear_analyzer_displays, update_analyzer_ui_state, select_all_analyzer_fixes, select_recommended_analyzer_fixes, clear_all_analyzer_fixes, update_analyzer_fix_ui_state, apply_analyzer_fixes, export_analyzer_plot, export_analyzer_report, update_analyzer_visualization, update_analyzer_comparison_plot, create_audio_output_analyzer_tab, setup_output_quality_tab, setup_output_technical_tab, setup_output_standards_tab, setup_output_chapter_tab, setup_output_comparison_tab, add_output_files, remove_output_file, clear_output_files, on_output_file_selected, analyze_selected_output, analyze_all_outputs, start_output_analysis, analyze_audiobook_file, estimate_bitrate, update_output_result_display, create_output_score_widget, clear_output_quality_grid, clear_output_displays, update_output_comparison_plot, update_output_analyzer_ui_state, export_output_report, export_output_plot, write, flush, debug_scroll, progress_callback
- Imports (local guess): PyQt5.QtCore, PyQt5.QtGui, PyQt5.QtWidgets, collections, config, config.config, contextlib, copy, datetime, gc, importlib, interface, io, librosa, logging, matplotlib.backends.backend_qt5agg, matplotlib.figure, matplotlib.pyplot, modules.file_manager, modules.gui_json_generator, modules.progress_tracker, modules.resume_handler, modules.simple_token_logger, modules.system_detector, modules.terminal_logger, modules.text_processor, modules.token_analyzer, modules.tts_engine, modules.voice_detector, numpy, os, pathlib, platform, pygame, re, subprocess, sys, threading, tools.combine_only, torch, traceback, utils.generate_from_json, voice_analyzer.analyzer, voice_analyzer.audio_processor, voice_analyzer.visualizer, winsound, wrapper.chunk_loader, wrapper.chunk_player, wrapper.chunk_revisions, wrapper.chunk_search, wrapper.chunk_synthesizer, wrapper.chunk_tool
- Details: files/chatterbox_gui.md
### config.__init__
- Details: files/config.__init__.md
### config.config
> GenTTS Configuration Module
- Side-effect signals: env_reads
- Imports (local guess): os, pathlib
- Details: files/config.config.md
### gradio_app
> Gradio Interface for ChatterboxTTS Audiobook Pipeline
- Functions: initialize_tts, process_text_to_chunks, generate_chunk_audio, generate_audiobook, create_interface
- Imports (local guess): datetime, gradio, json, logging, modules.audio_processor, modules.file_manager, modules.text_processor, os, pathlib, src.chatterbox.tts, tempfile, torch, torchaudio, traceback, vaderSentiment.vaderSentiment, zipfile
- Details: files/gradio_app.md
### gradio_launcher
> Comprehensive Gradio Launcher for ChatterboxTTS
- Side-effect signals: subprocess, sys_exit
- Classes: GradioLauncher
- Functions: main, print_header, check_python_version, check_working_directory, create_directories, check_package_installed, compare_versions, setup_virtual_environment, install_package, check_and_install_requirements, check_gpu_availability, verify_installation, launch_interface, run
- Imports (local guess): chatterbox, gradio_main_interface, importlib, os, parselmouth, pathlib, pkg_resources, subprocess, sys, time, torch
- Details: files/gradio_launcher.md
### gradio_main_interface
> ChatterboxTTS Gradio Web Interface - Main Entry Point
- Functions: detect_device_status, create_placeholder_tab, create_main_interface, launch_interface
- Imports (local guess): gradio, gradio_tabs.tab1_convert_book, gradio_tabs.tab2_configuration, gradio_tabs.tab4_combine_audio, gradio_tabs.tab5_prepare_text, gradio_tabs.tab6_settings, gradio_tabs.tab7_chunk_tools, gradio_tabs.tab8_json_generate, os, pathlib, sys, torch
- Details: files/gradio_main_interface.md
### gradio_tabs.__init__
> ChatterboxTTS Gradio Tabs Package
- Details: files/gradio_tabs.__init__.md
### gradio_tabs.tab1_convert_book
> Gradio Tab 1: Convert Book
- Functions: parse_progress_stats, get_progress_stats, get_book_folders, get_text_files_in_folder, get_voice_samples, find_generated_audiobook, run_book_conversion, regenerate_m4b_file, list_text_files, play_voice_sample, create_convert_book_tab, handle_voice_upload, get_session_audiobooks, update_audiobook_dropdowns, update_audiobook_dropdowns_after_conversion, update_playback_only, load_selected_audiobook, handle_asr_toggle, analyze_system, update_asr_models, start_conversion, handle_m4b_regeneration, apply_preset, get_current_stats, get_status_and_results, progress_callback, run_conversion_thread
- Imports (local guess): config.config, datetime, gradio, importlib.util, json, modules.file_manager, modules.path_validator, modules.system_detector, modules.tts_engine, os, pathlib, pygame, re, shutil, subprocess, sys, tempfile, threading, time, traceback, typing, warnings
- Details: files/gradio_tabs.tab1_convert_book.md
### gradio_tabs.tab2_configuration
> Gradio Tab 2: Configuration Settings (file-backed)
- Functions: create_configuration_tab, save_configuration, reload_configuration, reset_configuration, field_value_from_file
- Imports (local guess): ast, config, config.config, datetime, gradio, importlib, os, pathlib, re, shutil, tempfile, traceback
- Details: files/gradio_tabs.tab2_configuration.md
### gradio_tabs.tab4_combine_audio
> Gradio Tab 4: Combine Audio
- Functions: get_available_books, get_book_info, run_combine_operation, create_combine_audio_tab, update_book_info, refresh_book_list, get_selected_book_path, start_combine_operation, stop_combine_operation, get_current_status, combine_audio_for_book, get_audio_files_in_directory, get_wav_duration, run_combine_thread
- Imports (local guess): gradio, modules.audio_processor, modules.file_manager, os, pathlib, sys, threading, time, tools.combine_only, typing
- Details: files/gradio_tabs.tab4_combine_audio.md
### gradio_tabs.tab5_prepare_text
> Gradio Tab 5: Prepare Text
- Functions: get_available_text_files, load_text_file_info, start_text_preparation, get_preparation_status, stop_text_preparation, create_prepare_text_tab, refresh_file_list, show_next_steps, generate_enriched_chunks, preparation_worker
- Imports (local guess): config.config, gradio, json, modules.path_validator, modules.tts_engine, os, pathlib, sys, threading, time, typing
- Details: files/gradio_tabs.tab5_prepare_text.md
### gradio_tabs.tab6_settings
> Gradio Tab 6: Settings
- Classes: ConfigManager
- Functions: create_config_editor, create_config_backup, create_chunking_test, create_system_info, create_settings_tab, create_settings_tab_interface, load_current_config, reload_config, save_config_value, get_config_categories, reload_config, save_all_changes, create_backup, restore_backup, run_chunking_test, get_system_info
- Imports (local guess): config, contextlib, gradio, importlib, io, json, modules.text_processor, os, pathlib, sys, typing
- Details: files/gradio_tabs.tab6_settings.md
### gradio_tabs.tab7_chunk_tools
> Gradio Tab 7: Chunk Tools
- Functions: get_available_repair_books, load_book_chunks, search_for_chunks, select_chunk_for_editing, save_chunk_changes, play_original_audio, resynthesize_chunk_audio, play_revised_audio, accept_chunk_revision, create_chunk_tools_tab, refresh_book_list, refresh_voice_candidates, load_chunks, save_chunks, search_chunks, update_chunk, play_chunk_audio, synthesize_chunk, accept_revision, get_likely_voices_for_book, play_audio, resynth_worker, play_audio
- Imports (local guess): config.config, gradio, json, modules.voice_detector, os, pathlib, sys, threading, time, typing, wrapper.chunk_editor, wrapper.chunk_loader, wrapper.chunk_player, wrapper.chunk_revisions, wrapper.chunk_search, wrapper.chunk_synthesizer
- Details: files/gradio_tabs.tab7_chunk_tools.md
### gradio_tabs.tab8_json_generate
> Gradio Tab 8: JSON Generate
- Functions: get_available_json_files, get_available_voices, load_json_file_info, start_json_generation, get_generation_status, stop_json_generation, play_audio, create_json_generate_tab, refresh_json_files, refresh_voice_list, show_download_info, generate_audiobook_from_json, list_voice_samples, generation_worker
- Imports (local guess): config.config, gradio, json, modules.file_manager, modules.gui_json_generator, os, pathlib, subprocess, sys, threading, time, typing
- Details: files/gradio_tabs.tab8_json_generate.md
### interface
> ==============================================================================
- Framework signals: argparse
- Functions: signal_handler, prompt_book_selection, prompt_voice_selection, prompt_tts_params, pipeline_book_processing, main, main_with_resume, get_float_input, get_yes_no_input, get_choice_input
- Imports (local guess): argparse, config.config, modules.audio_processor, modules.file_manager, modules.progress_tracker, modules.resume_handler, modules.system_detector, modules.text_processor, modules.tts_engine, os, pathlib, signal, src.chatterbox.tts, sys, tools.combine_only, torch, traceback, warnings
- Details: files/interface.md
### launch
> ChatterboxTTS Launcher
- Side-effect signals: subprocess, sys_exit
- Functions: main
- Imports (local guess): os, pathlib, subprocess, sys
- Details: files/launch.md
### main_launcher
> GenTTS Wrapper Launcher
- Functions: prompt_menu, prepare_chunk_file, main_with_resume, wrapper_main, get_float_input, get_yes_no_input
- Imports (local guess): config.config, interface, logging, modules.resume_handler, modules.text_processor, modules.tts_engine, pathlib, sys, tools.combine_only, utils.generate_from_json, vaderSentiment.vaderSentiment, wrapper.chunk_loader, wrapper.chunk_tool
- Details: files/main_launcher.md
### modules.advanced_optimizations
> Advanced Optimizations Module
- Side-effect signals: subprocess
- Classes: AdvancedOptimizer
- Functions: set_warmup_mode, get_advanced_optimizer, optimize_model_advanced, diagnose_and_fix_torch_compile, apply_smart_torch_compile, apply_advanced_int8_quantization, apply_memory_optimizations, revert_optimizations
- Imports (local guess): logging, os, pathlib, subprocess, torch, torch._dynamo, triton, typing, warnings
- Details: files/modules.advanced_optimizations.md
### modules.asr_manager
> ASR Manager Module
- Functions: get_real_time_vram_status, calculate_available_vram_for_asr, can_model_fit_gpu, try_load_model_with_fallback, load_asr_model_adaptive, cleanup_asr_model, get_asr_memory_info, convert_device_name
- Imports (local guess): config.config, logging, pathlib, torch, whisper
- Details: files/modules.asr_manager.md
### modules.audio_processor
> ChatterboxTTS Audio Processing & Quality Control Module
- Functions: check_audio_health, detect_tts_hum_artifact, smart_audio_validation, has_mid_energy_drop, detect_spectral_artifacts, evaluate_chunk_quality, validate_output_matches_input, calculate_text_similarity, adjust_parameters_for_retry, handle_problematic_chunks, pause_for_chunk_review, detect_end_artifact, find_end_of_speech, fade_out_wav, apply_smart_fade, apply_smart_fade_memory, smart_audio_validation_memory, add_contextual_silence_memory, smart_fade_out, trim_audio_endpoint, process_audio_with_trimming_and_silence, add_contextual_silence, add_chunk_end_silence, get_wav_duration, get_chunk_audio_duration, normalize_text
- Imports (local guess): config.config, librosa, logging, modules.asr_manager, numpy, os, pathlib, pydub, re, shutil, soundfile, tempfile, time, torch, wave
- Details: files/modules.audio_processor.md
### modules.bandwidth_monitor
> Real-time Memory Bandwidth Monitor for TTS Inference
- Side-effect signals: subprocess
- Classes: RealTimeBandwidthMonitor, TTSBandwidthProfiler
- Functions: monitor_tts_bandwidth, start_monitoring, stop_monitoring, profile_tts_generation
- Imports (local guess): pathlib, psutil, queue, subprocess, threading, time
- Details: files/modules.bandwidth_monitor.md
### modules.batch_processor
- Framework signals: argparse
- Imports (local guess): argparse, json, modules.tts_engine, pathlib, sys
- Details: files/modules.batch_processor.md
### modules.cuda_optimizer
> CUDA Kernel Optimization Module
- Classes: CudaOptimizer
- Functions: create_cuda_optimizer, apply_cuda_optimizations, optimize_tensor_memory_layout, create_optimized_tensor, preallocate_batch_tensors, get_preallocated_tensor, async_batch_inference, pipeline_batch_processing, fused_attention_with_cache, optimize_batch_processing, clear_memory_efficiently, restore_original_settings, get_optimization_summary
- Imports (local guess): gc, logging, torch, torch.nn.functional, typing
- Details: files/modules.cuda_optimizer.md
### modules.dual_model_optimizer
> Dual Model Parallel Inference Optimizer
- Classes: DualModelParallelOptimizer
- Functions: test_dual_model_optimization, load_dual_models, generate_parallel_pair, benchmark_dual_vs_single, process_chunks_parallel, cleanup
- Imports (local guess): asyncio, concurrent.futures, config.config, gc, modules.real_tts_optimizer, pathlib, src.chatterbox.tts, sys, threading, time, torch
- Details: files/modules.dual_model_optimizer.md
### modules.dual_t3_engine
> Dual T3 Parallel Inference Engine
- Classes: WorkItem, TokenResult, AudioResult, TTSWorker, S3GenWorker, DualT3Coordinator
- Functions: load_dual_t3_models, run, stop, run, stop, start, stop, process_chunks
- Imports (local guess): config.config, dataclasses, logging, numpy, pathlib, queue, src.chatterbox.tts, threading, time, torch, typing
- Details: files/modules.dual_t3_engine.md
### modules.dual_tts_engine
> Dual TTS Parallel Inference Engine (Simplified)
- Classes: WorkItem, AudioResult, TTSWorker, DualTTSCoordinator
- Functions: load_dual_tts_models, run, stop, start, stop, process_chunks
- Imports (local guess): config.config, dataclasses, logging, numpy, pathlib, queue, src.chatterbox.models.s3tokenizer, src.chatterbox.tts, threading, time, torch, torch.nn.functional, typing
- Details: files/modules.dual_tts_engine.md
### modules.file_manager
> ChatterboxTTS File Management & Media Processing Module
- Side-effect signals: subprocess
- Functions: is_ffmpeg_available, ffmpeg_error_message, list_voice_samples, ensure_voice_sample_compatibility, run_ffmpeg, convert_to_m4b_with_peak_normalization, convert_to_m4b_with_loudness_normalization, convert_to_m4b_with_simple_normalization, convert_to_m4b, add_metadata_to_m4b, chunk_sort_key, create_concat_file, cleanup_temp_files, sanitize_filename, setup_book_directories, find_book_files, combine_audio_chunks, get_audio_files_in_directory, verify_audio_file, verify_chunk_completeness, export_processing_log, save_chunk_info, apply_batch_binning, load_chunk_info
- Imports (local guess): config.config, json, logging, os, pathlib, re, soundfile, subprocess, time
- Details: files/modules.file_manager.md
### modules.gpu_bandwidth_monitor
> GPU Memory Bandwidth Monitor
- Side-effect signals: subprocess
- Classes: GPUSample, GPUBandwidthMonitor
- Functions: run, stop, get_statistics, print_report
- Imports (local guess): dataclasses, logging, subprocess, threading, time, typing
- Details: files/modules.gpu_bandwidth_monitor.md
### modules.gui_json_generator
> GUI JSON Audio Generation Module
- Functions: generate_audiobook_from_json, get_book_name_from_json_path
- Imports (local guess): concurrent.futures, config.config, datetime, modules.file_manager, modules.progress_tracker, modules.tts_engine, pathlib, src.chatterbox.tts, sys, time, tools.combine_only, torch, wrapper.chunk_loader
- Details: files/modules.gui_json_generator.md
### modules.onnx_optimizer
> ONNX Optimization Module for ChatterboxTTS T3 Model
- Classes: T3ONNXOptimizer, T3InferenceWrapper
- Functions: optimize_model_with_onnx, convert_t3_to_onnx, onnx_inference, benchmark_onnx_vs_pytorch, onnx_wrapped_inference, forward
- Imports (local guess): numpy, onnx, onnxruntime, onnxruntime.tools, os, pathlib, tempfile, time, torch
- Details: files/modules.onnx_optimizer.md
### modules.path_validator
> Path Validation Module
- Functions: detect_problematic_characters, suggest_safe_path, validate_book_path, validate_and_create_audiobook_path, check_existing_audiobook_paths, format_path_warning_html, format_path_warning_text
- Imports (local guess): config.config, modules.file_manager, pathlib, re, typing
- Details: files/modules.path_validator.md
### modules.progress_tracker
> ChatterboxTTS Progress Tracking & Performance Monitoring Module
- Classes: PerformanceTracker
- Functions: setup_logging, log_console, log_run, log_chunk_progress, display_batch_progress, display_final_summary, monitor_vram_usage, monitor_gpu_utilization, optimize_memory_if_needed, display_system_info, log_processing_error, log_processing_warning, create_status_line, update_status_line, export_performance_report, fmt, log_chunk_completion, log_batch_completion, get_performance_summary
- Imports (local guess): config.config, datetime, gc, logging, modules.smart_reload_manager, modules.terminal_logger, modules.tts_engine, pathlib, pynvml, sys, time, torch
- Details: files/modules.progress_tracker.md
### modules.real_tts_optimizer
> Real TTS Performance Optimizer
- Classes: RealTTSOptimizer
- Functions: get_tts_optimizer, optimize_chatterbox_model, optimized_inference, fp32_fallback_mode, apply_optimizations, restore_original_methods, optimized_t3_inference, optimized_s3gen_inference
- Imports (local guess): config.config, contextlib, logging, torch, traceback
- Details: files/modules.real_tts_optimizer.md
### modules.resume_handler
> ChatterboxTTS Resume Handler Module
- Functions: analyze_existing_chunks, suggest_resume_point, validate_resume_point, process_book_folder_resume, resume_book_from_chunk, find_incomplete_books, auto_resume_incomplete, prompt_float
- Imports (local guess): concurrent.futures, config.config, datetime, gc, logging, modules.asr_manager, modules.audio_processor, modules.file_manager, modules.progress_tracker, modules.text_processor, modules.tts_engine, pathlib, re, shutil, src.chatterbox.tts, time, torch, wrapper.chunk_loader
- Details: files/modules.resume_handler.md
### modules.sequence_batch_processor
> True Sequence-Level Batch Processor
- Classes: SequenceBatchProcessor
- Functions: create_sequence_batch_processor, analyze_batching_potential, process_chunks_with_sequence_batching
- Imports (local guess): collections, logging, time, torch, typing
- Details: files/modules.sequence_batch_processor.md
### modules.simple_token_logger
> Simple token usage logger - just writes chunk_number,tokens,its_rate
- Functions: init_token_log, log_chunk
- Imports (local guess): datetime, os
- Details: files/modules.simple_token_logger.md
### modules.system_detector
> System Resource Detection Module
- Functions: get_gpu_memory, get_system_memory, get_cpu_cores, estimate_tts_vram_usage, get_system_profile, categorize_system, get_safe_asr_models, get_safe_cpu_models, recommend_asr_models, print_system_summary
- Imports (local guess): config.config, os, pathlib, psutil, sys, torch
- Details: files/modules.system_detector.md
### modules.t3_minimal_export
> T3 Minimal ONNX Export - Simplified approach with working T3Cond
- Classes: T3WorkingWrapper
- Functions: create_working_t3_cond, export_t3_minimal, forward
- Imports (local guess): gc, modules.t3_standalone_export, numpy, onnxruntime, pathlib, src.chatterbox.models.t3.modules.cond_enc, sys, torch, torch.onnx, traceback
- Details: files/modules.t3_minimal_export.md
### modules.t3_standalone_export
> T3 Standalone ONNX Export - Memory-efficient T3 ONNX conversion
- Classes: T3MinimalWrapper
- Functions: find_cached_model_files, load_t3_minimal, create_minimal_t3_wrapper, export_t3_standalone, forward
- Imports (local guess): gc, glob, logging, numpy, onnxruntime, os, pathlib, safetensors, src.chatterbox.models.t3.modules.cond_enc, src.chatterbox.models.t3.t3, src.chatterbox.models.tokenizers.tokenizer, sys, time, torch, torch.onnx, traceback
- Details: files/modules.t3_standalone_export.md
### modules.terminal_logger
> Terminal Output Logger
- Side-effect signals: file_io
- Classes: TerminalLogger
- Functions: start_terminal_logging, stop_terminal_logging, log_only, set_eta_frequency, set_batch_size, emit_chunk_summary, get_running_avg_its, start_logging, stop_logging, emit_chunk_summary, get_running_avg_its, write, flush, write_file_only, set_eta_frequency, set_batch_size
- Imports (local guess): config.config, datetime, pathlib, re, sys, threading
- Details: files/modules.terminal_logger.md
### modules.text_processor
> ChatterboxTTS Text Processing Module
- Functions: load_abbreviations, create_sample_abbreviations_file, preprocess_abbreviations, smart_punctuate, fix_short_sentence_artifacts, sentence_chunk_text, break_long_sentence_backwards, detect_punctuation_boundary, detect_content_boundaries, reload_abbreviations, test_abbreviations, test_chunking, get_chunk_bucket, analyze_chunk_distribution, calculate_optimization_potential, create_bucketed_chunk_groups, log_chunk_bucketing_stats
- Imports (local guess): config.config, logging, pathlib, re
- Details: files/modules.text_processor.md
### modules.token_analyzer
> Token Analyzer Module
- Classes: TokenAnalyzer
- Functions: get_token_analyzer, analyze_and_optimize_tokens, format_analysis_summary, predict_chunk_tokens, analyze_chunks_json, update_max_tokens_config
- Imports (local guess): config.config, json, logging, numpy, pathlib, re, typing
- Details: files/modules.token_analyzer.md
### modules.token_calculator
> Token Calculator for T3 TTS Analysis
- Classes: TokenAnalysis, TTSTokenCalculator
- Functions: analyze_real_audiobook_chunks, analyze_test_chunks, analyze_chunks, analyze_single_chunk, print_analysis_summary, print_real_audiobook_analysis
- Imports (local guess): dataclasses, json, torch, typing
- Details: files/modules.token_calculator.md
### modules.token_usage_logger
> Token Usage Logger for T3 Performance Analysis
- Classes: TokenUsageLogger
- Functions: initialize_token_logging, start_chunk_logging, log_chunk_tokens, log_chunk_data_direct, print_token_usage_summary, get_token_logger, start_chunk, log_chunk_completion, log_chunk_data, get_log_summary, print_summary
- Imports (local guess): datetime, os, threading, time, typing
- Details: files/modules.token_usage_logger.md
### modules.tts_engine
> TTS Engine Module
- Side-effect signals: file_io
- Functions: clear_voice_cache, store_voice_cache, restore_voice_cache, get_voice_cache_info, find_chunks_json_file, set_seed, monitor_gpu_activity, optimize_memory_usage, monitor_vram_usage, get_optimal_workers, prewarm_model_with_voice, get_best_available_device, load_optimized_model, patch_alignment_layer, process_batch, process_one_chunk, smooth_sentiment_scores, generate_enriched_chunks, create_parameter_microbatches, process_book_folder, process_single_batch, patched_forward, log_run, gen_with_backoff
- Imports (local guess): collections, concurrent.futures, config, config.config, datetime, difflib, gc, glob, io, logging, modules, modules.asr_manager, modules.audio_processor, modules.file_manager, modules.progress_tracker, modules.real_tts_optimizer, modules.terminal_logger, modules.text_processor, modules.voice_detector, numpy, os, pathlib, pydub, random, shutil, soundfile, src.chatterbox.tts, sys, tempfile, threading, time, torch, torchaudio, traceback, types, vaderSentiment.vaderSentiment, wrapper.chunk_loader
- Details: files/modules.tts_engine.md
### modules.voice_detector
> Voice Detection Module
- Functions: get_likely_voices_for_book, detect_voice_for_book, get_voice_from_json, get_voice_from_log, get_voices_from_filenames, get_voice_from_filename, find_voice_file_by_name, add_voice_to_json, remove_voice_comment_from_json
- Imports (local guess): config.config, json, modules.file_manager, pathlib, re
- Details: files/modules.voice_detector.md
### modules.vram_bandwidth_monitor
> VRAM Bandwidth Monitor for T3 Bottleneck Analysis
- Side-effect signals: subprocess
- Classes: VRAMSnapshot, VRAMBandwidthMonitor
- Functions: start_vram_monitoring, stop_vram_monitoring_and_analyze, monitor_t3_bandwidth, start_monitoring, stop_monitoring, print_analysis, wrapper, monitor_loop
- Imports (local guess): dataclasses, datetime, re, subprocess, threading, time, typing
- Details: files/modules.vram_bandwidth_monitor.md
### scripts.make_backup
> One‑click backup bundler
- Framework signals: argparse
- Functions: make_backup, main, add_path
- Imports (local guess): __future__, argparse, datetime, os, pathlib, zipfile
- Details: files/scripts.make_backup.md
### src.chatterbox.__init__
> Chatterbox package init (kept minimal to avoid heavy side effects on import).
- Details: files/src.chatterbox.__init__.md
### src.chatterbox.models.s3gen.__init__
- Details: files/src.chatterbox.models.s3gen.__init__.md
### src.chatterbox.models.s3gen.const
- Details: files/src.chatterbox.models.s3gen.const.md
### src.chatterbox.models.s3gen.decoder
- Classes: Transpose, CausalBlock1D, CausalResnetBlock1D, CausalConv1d, ConditionalDecoder
- Functions: mask_to_bias, forward, forward, forward, initialize_weights, forward
- Imports (local guess): einops, torch, torch.nn, torch.nn.functional
- Details: files/src.chatterbox.models.s3gen.decoder.md
### src.chatterbox.models.s3gen.f0_predictor
- Classes: ConvRNNF0Predictor
- Functions: forward
- Imports (local guess): torch, torch.nn, torch.nn.utils.parametrizations
- Details: files/src.chatterbox.models.s3gen.f0_predictor.md
### src.chatterbox.models.s3gen.flow
- Classes: MaskedDiffWithXvec, CausalMaskedDiffWithXvec
- Functions: forward, inference, inference
- Imports (local guess): logging, omegaconf, random, torch, torch.nn, typing
- Details: files/src.chatterbox.models.s3gen.flow.md
### src.chatterbox.models.s3gen.flow_matching
- Classes: ConditionalCFM, CausalConditionalCFM
- Functions: forward, solve_euler, forward_estimator, compute_loss, forward
- Imports (local guess): omegaconf, threading, torch, torch.nn.functional
- Details: files/src.chatterbox.models.s3gen.flow_matching.md
### src.chatterbox.models.s3gen.hifigan
> HIFI-GAN
- Classes: Snake, ResBlock, SineGen, SourceModuleHnNSF, HiFTGenerator
- Functions: get_padding, init_weights, forward, forward, remove_weight_norm, forward, forward, remove_weight_norm, decode, forward, inference
- Imports (local guess): numpy, scipy.signal, torch, torch.distributions.uniform, torch.nn, torch.nn.functional, torch.nn.utils, torch.nn.utils.parametrizations, typing
- Details: files/src.chatterbox.models.s3gen.hifigan.md
### src.chatterbox.models.s3gen.matcha.decoder
- Classes: SinusoidalPosEmb, Block1D, ResnetBlock1D, Downsample1D, TimestepEmbedding, Upsample1D, ConformerWrapper, Decoder
- Functions: forward, forward, forward, forward, forward, forward, forward, get_block, initialize_weights, forward
- Imports (local guess): conformer, diffusers.models.activations, einops, math, torch, torch.nn, torch.nn.functional, typing
- Details: files/src.chatterbox.models.s3gen.matcha.decoder.md
### src.chatterbox.models.s3gen.matcha.flow_matching
- Classes: BASECFM, CFM
- Functions: forward, solve_euler, compute_loss
- Imports (local guess): abc, torch, torch.nn.functional
- Details: files/src.chatterbox.models.s3gen.matcha.flow_matching.md
### src.chatterbox.models.s3gen.matcha.text_encoder
> from https://github.com/jaywalnut310/glow-tts 
- Classes: LayerNorm, ConvReluNorm, DurationPredictor, RotaryPositionalEmbeddings, MultiHeadAttention, FFN, Encoder, TextEncoder
- Functions: sequence_mask, forward, forward, forward, forward, forward, attention, forward, forward, forward
- Imports (local guess): einops, math, torch, torch.nn
- Details: files/src.chatterbox.models.s3gen.matcha.text_encoder.md
### src.chatterbox.models.s3gen.matcha.transformer
- Classes: SnakeBeta, FeedForward, BasicTransformerBlock
- Functions: forward, forward, set_chunk_feed_forward, forward
- Imports (local guess): diffusers.models.attention, diffusers.models.attention_processor, diffusers.models.lora, diffusers.utils.torch_utils, torch, torch.nn, typing
- Details: files/src.chatterbox.models.s3gen.matcha.transformer.md
### src.chatterbox.models.s3gen.s3gen
- Classes: S3Token2Mel, S3Token2Wav
- Functions: drop_invalid_tokens, get_resampler, device, embed_ref, forward, forward, flow_inference, hift_inference, inference
- Imports (local guess): functools, logging, numpy, omegaconf, torch, torchaudio, typing
- Details: files/src.chatterbox.models.s3gen.s3gen.md
### src.chatterbox.models.s3gen.transformer.__init__
- Details: files/src.chatterbox.models.s3gen.transformer.__init__.md
### src.chatterbox.models.s3gen.transformer.activation
> Swish() activation function for Conformer.
- Classes: Swish, Snake
- Functions: forward, forward
- Imports (local guess): torch, torch.nn
- Details: files/src.chatterbox.models.s3gen.transformer.activation.md
### src.chatterbox.models.s3gen.transformer.attention
> Multi-Head Attention layer definition.
- Classes: MultiHeadedAttention, RelPositionMultiHeadedAttention
- Functions: forward_qkv, forward_attention, forward, rel_shift, forward
- Imports (local guess): math, torch, typing
- Details: files/src.chatterbox.models.s3gen.transformer.attention.md
### src.chatterbox.models.s3gen.transformer.convolution
> ConvolutionModule definition.
- Classes: ConvolutionModule
- Functions: forward
- Imports (local guess): torch, typing
- Details: files/src.chatterbox.models.s3gen.transformer.convolution.md
### src.chatterbox.models.s3gen.transformer.embedding
> Positonal Encoding Module.
- Classes: PositionalEncoding, RelPositionalEncoding, WhisperPositionalEncoding, LearnablePositionalEncoding, NoPositionalEncoding, EspnetRelPositionalEncoding
- Functions: forward, position_encoding, forward, forward, position_encoding, extend_pe, forward, position_encoding
- Imports (local guess): math, numpy, torch, torch.nn.functional, typing
- Details: files/src.chatterbox.models.s3gen.transformer.embedding.md
### src.chatterbox.models.s3gen.transformer.encoder_layer
> Encoder self-attention layer definition.
- Classes: TransformerEncoderLayer, ConformerEncoderLayer
- Functions: forward, forward
- Imports (local guess): torch, typing
- Details: files/src.chatterbox.models.s3gen.transformer.encoder_layer.md
### src.chatterbox.models.s3gen.transformer.positionwise_feed_forward
> Positionwise feed forward layer definition.
- Classes: PositionwiseFeedForward, MoEFFNLayer
- Functions: forward, forward
- Imports (local guess): torch
- Details: files/src.chatterbox.models.s3gen.transformer.positionwise_feed_forward.md
### src.chatterbox.models.s3gen.transformer.subsampling
> Subsampling layer definition.
- Classes: BaseSubsampling, EmbedinigNoSubsampling, LinearNoSubsampling, Conv1dSubsampling2, Conv2dSubsampling4, Conv2dSubsampling6, Conv2dSubsampling8, LegacyLinearNoSubsampling
- Functions: position_encoding, forward, forward, forward, forward, forward, forward, forward
- Imports (local guess): torch, typing
- Details: files/src.chatterbox.models.s3gen.transformer.subsampling.md
### src.chatterbox.models.s3gen.transformer.upsample_encoder
> Encoder definition.
- Classes: Upsample1D, PreLookaheadLayer, UpsampleConformerEncoder
- Functions: forward, forward, output_size, forward, forward_layers, forward_up_layers
- Imports (local guess): torch, torch.nn, typing
- Details: files/src.chatterbox.models.s3gen.transformer.upsample_encoder.md
### src.chatterbox.models.s3gen.utils.class_utils
- Imports (local guess): torch
- Details: files/src.chatterbox.models.s3gen.utils.class_utils.md
### src.chatterbox.models.s3gen.utils.mask
- Functions: subsequent_chunk_mask, add_optional_chunk_mask, make_pad_mask
- Imports (local guess): torch
- Details: files/src.chatterbox.models.s3gen.utils.mask.md
### src.chatterbox.models.s3gen.utils.mel
> mel-spectrogram extraction in Matcha-TTS
- Functions: dynamic_range_compression_torch, spectral_normalize_torch, mel_spectrogram
- Imports (local guess): librosa.filters, numpy, torch
- Details: files/src.chatterbox.models.s3gen.utils.mel.md
### src.chatterbox.models.s3gen.xvector
- Classes: BasicResBlock, FCM, StatsPool, TDNNLayer, CAMLayer, CAMDenseTDNNLayer, CAMDenseTDNNBlock, TransitLayer, DenseLayer, CAMPPlus
- Functions: pad_list, extract_feature, get_nonlinear, statistics_pooling, forward, forward, forward, forward, forward, seg_pooling, bn_function, forward, forward, forward, forward, forward, inference
- Imports (local guess): collections, torch, torch.nn.functional, torch.utils.checkpoint, torchaudio.compliance.kaldi
- Details: files/src.chatterbox.models.s3gen.xvector.md
### src.chatterbox.models.s3tokenizer.__init__
- Functions: drop_invalid_tokens
- Details: files/src.chatterbox.models.s3tokenizer.__init__.md
### src.chatterbox.models.s3tokenizer.s3tokenizer
- Classes: S3Tokenizer
- Functions: pad, forward, log_mel_spectrogram
- Imports (local guess): librosa, numpy, s3tokenizer.model_v2, s3tokenizer.utils, torch, torch.nn.functional, typing
- Details: files/src.chatterbox.models.s3tokenizer.s3tokenizer.md
### src.chatterbox.models.t3.__init__
- Details: files/src.chatterbox.models.t3.__init__.md
### src.chatterbox.models.t3.inference.alignment_stream_analyzer
- Classes: AlignmentAnalysisResult, AlignmentStreamAnalyzer
- Functions: step, close, attention_forward_hook, patched_forward
- Imports (local guess): dataclasses, logging, torch, types
- Details: files/src.chatterbox.models.t3.inference.alignment_stream_analyzer.md
### src.chatterbox.models.t3.inference.t3_hf_backend
- Classes: T3HuggingfaceBackend
- Functions: prepare_inputs_for_generation, forward
- Imports (local guess): torch, transformers, transformers.modeling_outputs, typing
- Details: files/src.chatterbox.models.t3.inference.t3_hf_backend.md
### src.chatterbox.models.t3.llama_configs
- Details: files/src.chatterbox.models.t3.llama_configs.md
### src.chatterbox.models.t3.modules.cond_enc
- Classes: T3Cond, T3CondEnc
- Functions: to, save, load, forward
- Imports (local guess): dataclasses, torch, typing
- Details: files/src.chatterbox.models.t3.modules.cond_enc.md
### src.chatterbox.models.t3.modules.learned_pos_emb
- Classes: LearnedPositionEmbeddings
- Functions: forward, get_fixed_embedding
- Imports (local guess): torch, typing
- Details: files/src.chatterbox.models.t3.modules.learned_pos_emb.md
### src.chatterbox.models.t3.modules.perceiver
- Classes: RelativePositionBias, AttentionQKV, AttentionBlock2, Perceiver
- Functions: forward, setup_flash_config, forward, scaled_dot_product_attention, flash_attention, split_heads, combine_heads, forward, forward
- Imports (local guess): einops, math, torch, torch.nn.functional
- Details: files/src.chatterbox.models.t3.modules.perceiver.md
### src.chatterbox.models.t3.modules.t3_config
- Classes: T3Config
- Functions: n_channels
- Details: files/src.chatterbox.models.t3.modules.t3_config.md
### src.chatterbox.models.t3.t3
- Classes: AttrDict, T3
- Functions: device, prepare_conditioning, prepare_input_embeds, forward, loss, inference
- Imports (local guess): logging, os, torch, torch.nn.functional, tqdm, transformers, transformers.generation.logits_process, typing
- Details: files/src.chatterbox.models.t3.t3.md
### src.chatterbox.models.tokenizers.__init__
- Details: files/src.chatterbox.models.tokenizers.__init__.md
### src.chatterbox.models.tokenizers.tokenizer
- Classes: EnTokenizer
- Functions: check_vocabset_sot_eot, text_to_tokens, encode, decode
- Imports (local guess): logging, tokenizers, torch
- Details: files/src.chatterbox.models.tokenizers.tokenizer.md
### src.chatterbox.models.voice_encoder.__init__
- Details: files/src.chatterbox.models.voice_encoder.__init__.md
### src.chatterbox.models.voice_encoder.config
- Classes: VoiceEncConfig
- Details: files/src.chatterbox.models.voice_encoder.config.md
### src.chatterbox.models.voice_encoder.melspec
- Functions: mel_basis, preemphasis, melspectrogram
- Imports (local guess): functools, librosa, numpy, scipy
- Details: files/src.chatterbox.models.voice_encoder.melspec.md
### src.chatterbox.models.voice_encoder.voice_encoder
- Classes: VoiceEncoder
- Functions: pack, get_num_wins, get_frame_step, stride_as_partials, device, forward, inference, utt_to_spk_embed, voice_similarity, embeds_from_mels, embeds_from_wavs
- Imports (local guess): librosa, numpy, numpy.lib.stride_tricks, torch, torch.nn.functional, typing
- Details: files/src.chatterbox.models.voice_encoder.voice_encoder.md
### src.chatterbox.text_utils
> Text processing utility functions
- Functions: detect_language, get_sentence_separators, get_punctuation_pattern, split_by_word_boundary, merge_short_sentences, split_text_into_segments
- Imports (local guess): logging, re, typing
- Details: files/src.chatterbox.text_utils.md
### src.chatterbox.tts
- Side-effect signals: subprocess
- Classes: Conditionals, ChatterboxTTS
- Functions: punc_norm, parse_pause_tags, create_silence, to, save, load, from_local, from_pretrained, prepare_conditionals, generate, generate_batch, generate_worker
- Imports (local guess): concurrent.futures, config.config, dataclasses, huggingface_hub, librosa, numpy, os, pathlib, perth, queue, re, safetensors.torch, subprocess, tempfile, threading, torch, torch.nn.functional, torchaudio
- Details: files/src.chatterbox.tts.md
### src.chatterbox.vc
- Classes: ChatterboxVC
- Functions: from_local, from_pretrained, set_target_voice, generate
- Imports (local guess): huggingface_hub, librosa, pathlib, perth, safetensors.torch, torch
- Details: files/src.chatterbox.vc.md
### start
- Functions: prompt_menu, wrapper_main
- Imports (local guess): main_launcher, modules.text_processor, wrapper.chunk_tool
- Details: files/start.md
### tools.analyze_attention_implementation
> Attention Implementation Analyzer
- Functions: check_flash_attention_availability, analyze_current_attention_config, benchmark_attention_implementations, create_attention_optimization_plan, main
- Imports (local guess): flash_attn, gc, json, modules.tts_engine, os, pathlib, sys, time, torch, traceback, transformers
- Details: files/tools.analyze_attention_implementation.md
### tools.analyze_book_json_for_batching
> Book JSON Batching Analyzer
- Side-effect signals: sys_exit
- Classes: ChunkInfo, BatchGroup
- Functions: parse_book_json, group_chunks_by_tts_params, calculate_batch_benefit, analyze_batching_potential, print_analysis_report, create_batching_plan, save_analysis_results, main
- Imports (local guess): collections, dataclasses, json, pathlib, sys, time, torch, typing
- Details: files/tools.analyze_book_json_for_batching.md
### tools.audio_emotion_scanner
> Audio Emotion Scanner for ChatterboxTTS
- Framework signals: argparse
- Side-effect signals: sys_exit
- Classes: TranscriptSegment, EmotionalSegment, AudioEmotionScanner
- Functions: main, load_whisper_model, chunk_audio, transcribe_chunk, classify_speech_pattern, classify_emotion, analyze_transcript_segments, extract_audio_segment, scan_audio_file, save_analysis_results, extract_best_segments
- Imports (local guess): argparse, collections, dataclasses, gc, json, librosa, logging, numpy, os, pathlib, re, soundfile, sys, torch, typing, vaderSentiment.vaderSentiment, whisper
- Details: files/tools.audio_emotion_scanner.md
### tools.combine_only
> Combine Only Tool
- Functions: combine_audio_for_book, run_combine_only_mode, verify_chunk_sequence, list_available_books_for_combine, quick_combine
- Imports (local guess): config.config, datetime, logging, modules.audio_processor, modules.file_manager, modules.progress_tracker, pathlib, re, shutil, subprocess, sys, time
- Details: files/tools.combine_only.md
### tools.config_audit
> Config Audit: map config flags to usage sites to find unused toggles.
- Functions: extract_flags, scan_usage, main
- Imports (local guess): __future__, ast, json, pathlib, typing
- Details: files/tools.config_audit.md
### tools.cuda_kernel_profiler
> CUDA Kernel Utilization Profiler and Optimizer
- Framework signals: argparse
- Side-effect signals: subprocess
- Classes: CudaUtilizationSnapshot, KernelProfilingResult, CudaKernelProfiler
- Functions: main, start_monitoring, stop_monitoring, analyze_utilization, profile_inference_workload, generate_optimization_recommendations, run_comprehensive_profile, save_profile_results, print_summary
- Imports (local guess): argparse, config.config, dataclasses, gc, json, modules.file_manager, modules.tts_engine, os, pathlib, psutil, signal, subprocess, sys, threading, time, torch, traceback, typing
- Details: files/tools.cuda_kernel_profiler.md
### tools.emotion_extractor
> Emotion Extractor for ChatterboxTTS
- Framework signals: argparse
- Side-effect signals: sys_exit
- Classes: EmotionalSegment, EmotionExtractor
- Functions: main, classify_emotion, load_chunk_data, analyze_audio_quality, select_best_segments, combine_emotional_samples, generate_sample_report, score_segment
- Imports (local guess): argparse, collections, dataclasses, json, librosa, numpy, os, pathlib, soundfile, sys, typing
- Details: files/tools.emotion_extractor.md
### tools.emotional_audio_enhancer
> Emotional Audio Enhancer for ChatterboxTTS
- Side-effect signals: subprocess
- Classes: EmotionalAudioEnhancer
- Functions: main, setup_ui, create_tooltip, select_input_file, select_output_file, update_emotion_presets, check_audio_tools, start_processing, process_audio, apply_pitch_shift, apply_formant_shift, apply_compression, apply_eq, apply_tempo_change, apply_reverb, apply_tremolo, apply_vibrato, update_status, cleanup_temp_files, preview_audio, reset_settings, save_preset, load_preset, on_closing, on_enter, on_leave, update_display
- Imports (local guess): json, logging, os, pathlib, shutil, subprocess, tempfile, threading, tkinter, typing
- Details: files/tools.emotional_audio_enhancer.md
### tools.exporters.t3_fx_export
> Phase 1: FX trace + operator inventory for one T3 decoder block.
- Framework signals: argparse
- Classes: BlockWrapper, RoPETracer
- Functions: trace_block, op_histogram, main, forward, is_leaf_module
- Imports (local guess): __future__, argparse, config.config, json, os, pathlib, safetensors.torch, src.chatterbox.models.t3, src.chatterbox.models.t3.llama_configs, sys, torch, torch.fx, typing
- Details: files/tools.exporters.t3_fx_export.md
### tools.feature_run_logger
> Feature Run Logger: instrument GUI action slots to log actual UI values at press time.
- Functions: parse_input_expr, get_input_value, instrument_window, main, wrapped_init, make_wrapper
- Imports (local guess): PyQt5, PyQt5.QtWidgets, __future__, importlib, json, pathlib, sys, threading, time, types
- Details: files/tools.feature_run_logger.md
### tools.feature_spider
> Feature Spider: Static repo explorer for Chatterbox
- Framework signals: argparse
- Functions: rel, list_py_files, module_to_path, resolve_import, build_import_graph, to_dot, parse_gui_connections, main
- Imports (local guess): __future__, argparse, ast, json, os, pathlib, re, typing
- Details: files/tools.feature_spider.md
### tools.generate_from_json
> ChatterboxTTS JSON-Based Audio Generation Utility
- Functions: main
- Imports (local guess): chatterbox.tts, concurrent.futures, config.config, datetime, modules.file_manager, modules.progress_tracker, modules.tts_engine, pathlib, sys, time, torch, wrapper.chunk_loader
- Details: files/tools.generate_from_json.md
### tools.gui_static_map
> GUI Static Map: Analyze chatterbox_gui.py to map buttons → slots → inputs → external calls.
- Classes: GUISpy, SlotAnalyzer
- Functions: qualname_from_attr, build_feature_map, main, visit_Assign, visit_Call, visit_FunctionDef, visit_Call, generic_visit
- Imports (local guess): __future__, ast, json, pathlib, typing
- Details: files/tools.gui_static_map.md
### tools.gui_walker
> GUI Walker: enumerates and clicks GUI actions under SPIDER_DRY_RUN=1.
- Classes: _PkgStubLoader, _PkgStubFinder, _SIA
- Functions: log, save_log, main, create_module, exec_module, find_spec, polarity_scores
- Imports (local guess): PyQt5, PyQt5.QtTest, PyQt5.QtWidgets, __future__, importlib, importlib.machinery, os, pathlib, sys, time, types
- Details: files/tools.gui_walker.md
### tools.headless_performance_test
> Headless Performance Testing Framework for Chatterbox TTS
- Framework signals: argparse
- Side-effect signals: env_reads
- Classes: PerformanceResult, HeadlessPerformanceTester
- Functions: main, test_torch_compile_configurations, test_batching_configurations, test_memory_optimizations, run_full_test_suite, save_results, print_summary
- Imports (local guess): argparse, config.config, dataclasses, gc, json, logging, modules.file_manager, modules.terminal_logger, modules.tts_engine, os, pathlib, psutil, src.chatterbox.tts, subprocess, sys, time, torch, typing
- Details: files/tools.headless_performance_test.md
### tools.measure_token_memory
> Speech Token Memory Footprint Analysis
- Functions: get_memory_usage, measure_tensor_size, generate_test_tokens, analyze_queue_capacity, simulate_queue_transfer_overhead, main
- Imports (local guess): gc, json, modules.file_manager, modules.tts_engine, numpy, os, pathlib, psutil, src.chatterbox.tts, sys, torch
- Details: files/tools.measure_token_memory.md
### tools.ort_gpu_diagnose
> ORT/Torch GPU environment diagnostic.
- Framework signals: argparse
- Side-effect signals: subprocess
- Functions: print_header, find_shadowing_modules, show_python_env, show_shadowing, try_import_onnxruntime, try_torch_cuda, try_nvidia_smi, maybe_run_onnx_test, print_next_steps_hint, main
- Imports (local guess): __future__, argparse, importlib, importlib.util, onnxruntime, os, shutil, site, subprocess, sys, textwrap, torch, typing
- Details: files/tools.ort_gpu_diagnose.md
### tools.path_checker
> Path Checker Tool
- Functions: main
- Imports (local guess): config.config, modules.path_validator, pathlib, sys
- Details: files/tools.path_checker.md
### tools.quick_batching_test
> Quick Batching Test
- Functions: quick_batch_test, tokenize_single, tokenize_batch
- Imports (local guess): gc, json, modules.tts_engine, pathlib, sys, time, torch
- Details: files/tools.quick_batching_test.md
### tools.run_tts_once
- Framework signals: argparse
- Side-effect signals: env_reads, sys_exit
- Functions: parse_args, set_trt_env, default_texts, main
- Imports (local guess): argparse, json, modules.tts_engine, os, pathlib, sys, time, torch
- Details: files/tools.run_tts_once.md
### tools.runtime_summarize
> Summarize runtime trace produced by sitecustomize tracer.
- Functions: main
- Imports (local guess): __future__, json, pathlib
- Details: files/tools.runtime_summarize.md
### tools.safe_archiver
> Safe Archiver: move dead-code candidates to archive/ with a manifest.
- Framework signals: argparse
- Functions: load_candidates, load_reached, apply, restore, main
- Imports (local guess): __future__, argparse, json, pathlib, shutil
- Details: files/tools.safe_archiver.md
### tools.spider_ci
> Spider CI Check: run feature spider and simple assertions.
- Framework signals: argparse
- Functions: load_graph, detect_cycles, main, dfs
- Imports (local guess): __future__, argparse, json, pathlib
- Details: files/tools.spider_ci.md
### tools.spider_run
> One-shot Feature Spider Runner
- Framework signals: argparse
- Side-effect signals: subprocess
- Functions: run, main
- Imports (local guess): __future__, argparse, os, pathlib, subprocess, sys
- Details: files/tools.spider_run.md
### tools.test_attention_optimizations
> Test Attention Optimizations
- Side-effect signals: subprocess
- Functions: benchmark_attention_implementation, test_sdpa_attention, test_grouped_query_attention, install_flash_attention, main
- Imports (local guess): flash_attn, gc, json, modules.tts_engine, os, pathlib, subprocess, sys, time, torch, traceback
- Details: files/tools.test_attention_optimizations.md
### tools.test_batched_inference
> Batched T3 Inference Tester
- Side-effect signals: sys_exit
- Functions: load_batching_plan, prepare_text_batches, tokenize_text_batch, benchmark_sequential_inference, benchmark_batched_inference, run_batch_comparison, analyze_batch_results, main
- Imports (local guess): gc, json, modules.tts_engine, pathlib, sys, time, torch, typing
- Details: files/tools.test_batched_inference.md
### tools.test_compile_fix
> Quick test script to verify torch.compile fix impact
- Functions: clear_memory, get_test_voice, run_quick_inference_test, main
- Imports (local guess): gc, modules.file_manager, modules.tts_engine, os, pathlib, sys, time, torch, traceback
- Details: files/tools.test_compile_fix.md
### tools.test_cuda_integration
> Test CUDA Optimizer Integration
- Functions: clear_memory, get_test_voice, test_cuda_optimizer_integration, main
- Imports (local guess): gc, modules.cuda_optimizer, modules.file_manager, modules.real_tts_optimizer, modules.tts_engine, os, pathlib, sys, time, torch, traceback
- Details: files/tools.test_cuda_integration.md
### tools.test_dual_queue_pipeline
> Dual Queue Pipeline Performance Test
- Side-effect signals: subprocess
- Classes: DualQueueManager
- Functions: load_test_content, prepare_text_chunks, t3_worker, s3gen_worker, monitor_gpu_utilization, analyze_pipeline_performance, main, switch_queues, get_queue_status
- Imports (local guess): collections, gc, json, modules.text_processor, modules.tts_engine, os, pathlib, psutil, queue, src.chatterbox.tts, subprocess, sys, threading, time, torch, traceback
- Details: files/tools.test_dual_queue_pipeline.md
### tools.test_flash_attention
> Flash Attention 2 Testing
- Functions: benchmark_attention_implementation, load_model_with_attention, test_flash_attention_vs_eager
- Imports (local guess): gc, json, modules.tts_engine, os, pathlib, sys, time, torch, traceback
- Details: files/tools.test_flash_attention.md
### tools.test_kv_cache_optimization
> KV Cache Optimization Testing
- Functions: analyze_kv_cache_usage, test_kv_cache_preallocation, test_cache_memory_layout, benchmark_standard_inference, benchmark_contiguous_cache_inference, recommend_kv_optimizations, main
- Imports (local guess): gc, json, modules.tts_engine, os, pathlib, sys, time, torch, traceback
- Details: files/tools.test_kv_cache_optimization.md
### tools.test_s3gen_cpu_performance
> S3Gen CPU vs GPU Performance Test
- Functions: clear_memory, get_test_voice, get_memory_usage, create_test_speech_tokens, test_s3gen_gpu_performance, test_s3gen_cpu_performance, analyze_pipeline_potential, main
- Imports (local guess): gc, json, modules.file_manager, modules.tts_engine, os, pathlib, psutil, src.chatterbox.tts, sys, time, torch
- Details: files/tools.test_s3gen_cpu_performance.md
### tools.test_sequence_batching
> Test True Sequence-Level Batching
- Functions: clear_memory, get_test_voice, create_test_chunks, benchmark_individual_processing, benchmark_sequence_batching, compare_performance, main
- Imports (local guess): gc, json, modules.file_manager, modules.sequence_batch_processor, modules.tts_engine, os, pathlib, sys, time, torch
- Details: files/tools.test_sequence_batching.md
### tools.test_sequential_pipeline
> Sequential Pipeline Performance Test
- Side-effect signals: subprocess
- Functions: get_memory_usage, monitor_gpu_simple, phase_1_t3_processing, clear_t3_from_memory, phase_2_s3gen_processing, main
- Imports (local guess): gc, json, modules.text_processor, modules.tts_engine, os, pathlib, psutil, src.chatterbox.tts, subprocess, sys, time, torch, traceback
- Details: files/tools.test_sequential_pipeline.md
### tools.test_unified_device_mode
> Test Unified Device Mode Implementation
- Functions: clear_memory, get_test_voice, check_device_configuration, analyze_model_devices, test_basic_inference, test_batch_inference, main
- Imports (local guess): config.config, gc, modules.file_manager, modules.tts_engine, os, pathlib, sys, time, torch, traceback
- Details: files/tools.test_unified_device_mode.md
### tools.trace_pipeline_flow
> Pipeline Flow Tracer
- Side-effect signals: subprocess
- Functions: monitor_gpu, trace_single_chunk_pipeline, analyze_pipeline_bottlenecks, trace_multiple_chunks, main
- Imports (local guess): gc, json, modules.tts_engine, os, pathlib, src.chatterbox.tts, subprocess, sys, time, torch, traceback
- Details: files/tools.trace_pipeline_flow.md
### tools.trace_t3_inference
> T3 Inference Breakdown Tracer
- Side-effect signals: subprocess
- Functions: monitor_gpu, patched_t3_inference_with_timing, trace_t3_inference_detailed, main
- Imports (local guess): gc, json, modules.tts_engine, os, pathlib, src.chatterbox.models.t3.inference.alignment_stream_analyzer, src.chatterbox.models.t3.inference.t3_hf_backend, src.chatterbox.models.t3.t3, subprocess, sys, time, torch, traceback, transformers.generation.logits_process
- Details: files/tools.trace_t3_inference.md
### tools.tts_trt_benchmark
- Framework signals: argparse
- Side-effect signals: subprocess, sys_exit
- Functions: parse_args, run_once, main, summarize
- Imports (local guess): argparse, json, os, pathlib, subprocess, sys
- Details: files/tools.tts_trt_benchmark.md
### tools.xtts_finetune_extractor
> XTTS-Finetune Audio Extractor for ChatterboxTTS
- Framework signals: argparse
- Side-effect signals: sys_exit
- Classes: XTTSAudioFile, XTTSFinetuneExtractor, SentimentIntensityAnalyzer
- Functions: main, analyze_directory_structure, load_metadata, analyze_audio_file, assess_audio_quality, classify_emotion, extract_audio_files, select_best_samples, create_voice_samples, generate_report, polarity_scores, score_file
- Imports (local guess): argparse, collections, csv, dataclasses, json, librosa, logging, numpy, os, pathlib, re, soundfile, sys, typing, vaderSentiment.vaderSentiment
- Details: files/tools.xtts_finetune_extractor.md
### utils.generate_from_json
> Direct Audio Generation from JSON Tool
- Functions: main
- Imports (local guess): chatterbox.tts, concurrent.futures, config.config, datetime, modules.file_manager, modules.progress_tracker, modules.tts_engine, pathlib, sys, time, torch, wrapper.chunk_loader
- Details: files/utils.generate_from_json.md
### wrapper.chunk_editor
- Functions: update_chunk
- Details: files/wrapper.chunk_editor.md
### wrapper.chunk_loader
- Functions: load_chunks, load_metadata, save_chunks
- Imports (local guess): collections, copy, json, re
- Details: files/wrapper.chunk_loader.md
### wrapper.chunk_player
- Side-effect signals: subprocess
- Functions: play_chunk_audio
- Imports (local guess): os, subprocess
- Details: files/wrapper.chunk_player.md
### wrapper.chunk_revisions
- Functions: accept_revision
- Imports (local guess): config.config, os, pathlib, shutil
- Details: files/wrapper.chunk_revisions.md
### wrapper.chunk_search
- Functions: search_chunks
- Details: files/wrapper.chunk_search.md
### wrapper.chunk_synthesizer
- Functions: get_original_voice_from_log, get_original_voice_from_filename, find_voice_file_by_name, get_tts_params_for_chunk, synthesize_chunk, get_float_input
- Imports (local guess): config.config, io, modules.audio_processor, modules.file_manager, modules.tts_engine, modules.voice_detector, pathlib, pydub, re, soundfile, time, torch, traceback
- Details: files/wrapper.chunk_synthesizer.md
### wrapper.chunk_tool
> ChatterboxTTS Interactive Chunk Management Tool
- Functions: select_book_for_repair, run_chunk_repair_tool, get_float_input
- Imports (local guess): config.config, os, pathlib, wrapper.chunk_editor, wrapper.chunk_loader, wrapper.chunk_player, wrapper.chunk_revisions, wrapper.chunk_search, wrapper.chunk_synthesizer
- Details: files/wrapper.chunk_tool.md