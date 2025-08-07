#!/usr/bin/env python3
"""
Gradio Tab 6: Settings
Configuration management with live reload functionality
"""

import gradio as gr
import os
import sys
import json
import importlib
from pathlib import Path
from typing import Dict, Any, Tuple, List

# Import configuration
try:
    from config import config
    CONFIG_MODULE = config
    CONFIG_AVAILABLE = True
    print("✅ Config module loaded successfully")
except ImportError as e:
    print(f"⚠️  Config not available: {e}")
    CONFIG_AVAILABLE = False
    CONFIG_MODULE = None

class ConfigManager:
    """Manages configuration reloading and validation."""
    
    def __init__(self):
        self.config_file_path = Path("config/config.py")
        self.current_config = {}
        self.load_current_config()
    
    def load_current_config(self):
        """Load current configuration values."""
        if not CONFIG_AVAILABLE:
            return
        
        # Extract current config values
        config_attrs = [attr for attr in dir(CONFIG_MODULE) if not attr.startswith('_')]
        
        for attr in config_attrs:
            value = getattr(CONFIG_MODULE, attr)
            # Only include simple types that can be edited
            if isinstance(value, (int, float, str, bool, Path)):
                self.current_config[attr] = value
    
    def reload_config(self) -> Tuple[bool, str]:
        """
        Reload the configuration module.
        
        Returns:
            Tuple of (success, message)
        """
        try:
            # Reload the config module
            if CONFIG_MODULE:
                importlib.reload(CONFIG_MODULE)
                
                # Update current config
                self.load_current_config()
                
                return True, "✅ Configuration reloaded successfully!"
        except Exception as e:
            return False, f"❌ Error reloading config: {str(e)}"
    
    def save_config_value(self, key: str, value: Any) -> Tuple[bool, str]:
        """
        Save a configuration value (in-memory for now).
        
        Args:
            key: Configuration key
            value: New value
            
        Returns:
            Tuple of (success, message)
        """
        try:
            if CONFIG_MODULE and hasattr(CONFIG_MODULE, key):
                # Set the value in the module
                setattr(CONFIG_MODULE, key, value)
                self.current_config[key] = value
                return True, f"✅ {key} updated to {value}"
            else:
                return False, f"❌ Configuration key '{key}' not found"
        except Exception as e:
            return False, f"❌ Error updating {key}: {str(e)}"
    
    def get_config_categories(self) -> Dict[str, List[str]]:
        """Group configuration keys by category based on prefixes and naming."""
        categories = {
            "Core Directories": [],
            "Text Processing": [],
            "Performance": [],
            "TTS Parameters": [],
            "Audio Quality": [],
            "VADER Sentiment": [],
            "File Paths": []
        }
        
        for key in self.current_config.keys():
            key_lower = key.lower()
            
            if any(x in key_lower for x in ['dir', 'root', 'path', 'folder']):
                categories["Core Directories"].append(key)
            elif any(x in key_lower for x in ['chunk', 'word', 'text']):
                categories["Text Processing"].append(key)
            elif any(x in key_lower for x in ['worker', 'thread', 'vram', 'memory', 'performance']):
                categories["Performance"].append(key)
            elif any(x in key_lower for x in ['tts_param', 'temperature', 'cfg', 'exaggeration']):
                categories["TTS Parameters"].append(key)
            elif any(x in key_lower for x in ['audio', 'quality', 'validation', 'threshold']):
                categories["Audio Quality"].append(key)
            elif any(x in key_lower for x in ['vader', 'sentiment']):
                categories["VADER Sentiment"].append(key)
            else:
                categories["File Paths"].append(key)
        
        # Remove empty categories
        return {cat: keys for cat, keys in categories.items() if keys}

def create_config_editor(config_manager: ConfigManager):
    """Create configuration editor interface."""
    
    with gr.Column():
        gr.Markdown("## 🔧 Configuration Editor")
        gr.Markdown("*Edit configuration values and reload the system*")
        
        # Reload button
        reload_btn = gr.Button("🔄 Reload Configuration", variant="primary")
        reload_status = gr.Textbox(
            label="Status",
            value="Ready to reload configuration",
            interactive=False
        )
        
        # Configuration categories
        categories = config_manager.get_config_categories()
        
        config_inputs = {}
        
        for category, keys in categories.items():
            with gr.Accordion(f"📁 {category}", open=False):
                for key in keys:
                    current_value = config_manager.current_config.get(key, "")
                    
                    # Create appropriate input based on value type
                    if isinstance(current_value, bool):
                        config_inputs[key] = gr.Checkbox(
                            label=key,
                            value=current_value,
                            info=f"Current: {current_value}"
                        )
                    elif isinstance(current_value, int):
                        config_inputs[key] = gr.Number(
                            label=key,
                            value=current_value,
                            precision=0,
                            info=f"Current: {current_value}"
                        )
                    elif isinstance(current_value, float):
                        config_inputs[key] = gr.Number(
                            label=key,
                            value=current_value,
                            precision=3,
                            info=f"Current: {current_value}"
                        )
                    else:
                        config_inputs[key] = gr.Textbox(
                            label=key,
                            value=str(current_value),
                            info=f"Current: {current_value}"
                        )
        
        # Save all button
        save_all_btn = gr.Button("💾 Save All Changes", variant="secondary")
        save_status = gr.Textbox(
            label="Save Status",
            value="No changes to save",
            interactive=False
        )
        
        # Reload functionality
        def reload_config():
            success, message = config_manager.reload_config()
            
            if success:
                # Update all input values with reloaded config
                updates = {}
                for key, input_component in config_inputs.items():
                    new_value = config_manager.current_config.get(key, "")
                    updates[input_component] = gr.update(value=new_value, info=f"Current: {new_value}")
                
                return message, *updates.values()
            else:
                return message, *[gr.update() for _ in config_inputs]
        
        # Save all functionality  
        def save_all_changes(*values):
            results = []
            all_success = True
            
            for i, (key, input_component) in enumerate(config_inputs.items()):
                value = values[i]
                success, message = config_manager.save_config_value(key, value)
                results.append(message)
                if not success:
                    all_success = False
            
            if all_success:
                return "✅ All configuration changes saved successfully!"
            else:
                return f"⚠️ Some changes failed:\n" + "\n".join(results)
        
        # Wire up the reload button
        reload_outputs = [reload_status] + list(config_inputs.values())
        reload_btn.click(
            fn=reload_config,
            outputs=reload_outputs
        )
        
        # Wire up the save button
        save_all_btn.click(
            fn=save_all_changes,
            inputs=list(config_inputs.values()),
            outputs=[save_status]
        )

def create_config_backup():
    """Create configuration backup interface."""
    
    with gr.Column():
        gr.Markdown("## 💾 Configuration Backup")
        gr.Markdown("*Backup and restore configuration settings*")
        
        with gr.Row():
            backup_btn = gr.Button("📦 Create Backup")
            restore_btn = gr.Button("📂 Restore from Backup")
        
        backup_status = gr.Textbox(
            label="Backup Status",
            value="No backup operations performed",
            interactive=False
        )
        
        backup_file = gr.File(
            label="Backup File",
            file_types=[".json"],
            type="filepath"
        )
        
        def create_backup():
            try:
                if not CONFIG_AVAILABLE:
                    return "❌ Configuration not available for backup"
                
                config_data = {}
                config_attrs = [attr for attr in dir(CONFIG_MODULE) if not attr.startswith('_')]
                
                for attr in config_attrs:
                    value = getattr(CONFIG_MODULE, attr)
                    if isinstance(value, (int, float, str, bool)):
                        config_data[attr] = value
                    elif isinstance(value, Path):
                        config_data[attr] = str(value)
                
                backup_path = Path("config_backup.json")
                with open(backup_path, 'w') as f:
                    json.dump(config_data, f, indent=2)
                
                return f"✅ Configuration backed up to {backup_path}"
                
            except Exception as e:
                return f"❌ Backup failed: {str(e)}"
        
        def restore_backup(file_path):
            try:
                if not file_path:
                    return "❌ No backup file selected"
                
                with open(file_path, 'r') as f:
                    backup_data = json.load(f)
                
                restored_count = 0
                for key, value in backup_data.items():
                    if CONFIG_MODULE and hasattr(CONFIG_MODULE, key):
                        setattr(CONFIG_MODULE, key, value)
                        restored_count += 1
                
                return f"✅ Restored {restored_count} configuration values from backup"
                
            except Exception as e:
                return f"❌ Restore failed: {str(e)}"
        
        backup_btn.click(
            fn=create_backup,
            outputs=[backup_status]
        )
        
        restore_btn.click(
            fn=restore_backup,
            inputs=[backup_file],
            outputs=[backup_status]
        )

def create_system_info():
    """Create system information display."""
    
    with gr.Column():
        gr.Markdown("## 📊 System Information")
        
        # Get system info
        def get_system_info():
            info = []
            
            # Config availability
            info.append(f"**Configuration Module**: {'✅ Available' if CONFIG_AVAILABLE else '❌ Not Available'}")
            
            # Python version
            info.append(f"**Python Version**: {sys.version.split()[0]}")
            
            # Working directory
            info.append(f"**Working Directory**: {os.getcwd()}")
            
            # Config file path
            config_path = Path("config/config.py")
            info.append(f"**Config File**: {'✅ Exists' if config_path.exists() else '❌ Missing'} ({config_path})")
            
            # Config count
            if CONFIG_AVAILABLE:
                config_count = len([attr for attr in dir(CONFIG_MODULE) if not attr.startswith('_')])
                info.append(f"**Configuration Items**: {config_count}")
            
            return "\n\n".join(info)
        
        system_info = gr.Markdown(get_system_info())
        
        refresh_btn = gr.Button("🔄 Refresh Info")
        refresh_btn.click(
            fn=get_system_info,
            outputs=[system_info]
        )

def create_settings_tab():
    """Create the main settings tab interface."""
    
    if not CONFIG_AVAILABLE:
        # Show error state
        with gr.Column():
            gr.Markdown("# ⚠️ Configuration Not Available")
            gr.Markdown("""
            The configuration module could not be loaded. This may be due to:
            - Missing config/config.py file
            - Import errors in the configuration
            - Path issues
            
            Please check your installation and try again.
            """)
        return
    
    # Initialize config manager
    config_manager = ConfigManager()
    
    with gr.Column():
        gr.Markdown("# ⚙️ Settings & Configuration")
        gr.Markdown("*Manage ChatterboxTTS configuration and system settings*")
        
        with gr.Tabs():
            # Configuration Editor
            with gr.Tab("🔧 Configuration"):
                create_config_editor(config_manager)
            
            # Backup & Restore
            with gr.Tab("💾 Backup"):
                create_config_backup()
            
            # System Information
            with gr.Tab("📊 System Info"):
                create_system_info()

# Export the main function
def create_settings_tab_interface():
    """Main entry point for the settings tab."""
    return create_settings_tab()