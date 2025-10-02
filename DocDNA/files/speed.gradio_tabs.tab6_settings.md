# speed.gradio_tabs.tab6_settings

> Gradio Tab 6: Settings

## Public API

### Classes
- **ConfigManager** — Manages configuration reloading and validation.  
  Methods: load_current_config, reload_config, save_config_value, get_config_categories

### Functions
- **create_config_editor** — Create configuration editor interface.
- **create_config_backup** — Create configuration backup interface.
- **create_chunking_test** — Create chunking test interface.
- **create_system_info** — Create system information display.
- **create_settings_tab** — Create the main settings tab interface.
- **create_settings_tab_interface** — Main entry point for the settings tab.
- **load_current_config** — Load current configuration values.
- **reload_config** — Reload the configuration module.
- **save_config_value** — Save a configuration value (in-memory for now).
- **get_config_categories** — Group configuration keys by category based on prefixes and naming.
- **reload_config**
- **save_all_changes**
- **create_backup**
- **restore_backup**
- **run_chunking_test** — Run the chunking test
- **get_system_info**

## Imports (local guesses)
- config, contextlib, gradio, importlib, io, json, modules.text_processor, os, pathlib, sys, typing