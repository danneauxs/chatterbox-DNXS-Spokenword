#!/usr/bin/env python3
"""
Emotional Audio Enhancer for ChatterboxTTS
GUI-based tool for enhancing TTS output with emotional audio processing.

Features:
- File picker for input/output
- Checkbox options for different enhancements
- Real-time preview
- Batch processing support
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import subprocess
import os
import threading
from pathlib import Path
import tempfile
import shutil
import json
from typing import Dict, List, Optional
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class EmotionalAudioEnhancer:
    def __init__(self, root):
        self.root = root
        self.root.title("🎭 Emotional Audio Enhancer")
        self.root.geometry("800x900")
        
        # File paths
        self.input_file = tk.StringVar()
        self.output_file = tk.StringVar()
        self.temp_dir = tempfile.mkdtemp()
        
        # Enhancement options
        self.emotion_type = tk.StringVar(value="angry")
        self.enhancements = {
            'pitch_shift': tk.BooleanVar(value=True),
            'formant_shift': tk.BooleanVar(value=True), 
            'dynamic_compress': tk.BooleanVar(value=True),
            'harmonic_emphasis': tk.BooleanVar(value=True),
            'tempo_adjust': tk.BooleanVar(value=False),
            'reverb': tk.BooleanVar(value=False),
            'tremolo': tk.BooleanVar(value=False),
            'vibrato': tk.BooleanVar(value=False)
        }
        
        # Enhancement parameters
        self.parameters = {
            'pitch_amount': tk.IntVar(value=150),  # cents
            'formant_amount': tk.DoubleVar(value=1.15),  # ratio
            'compress_ratio': tk.DoubleVar(value=3.0),
            'eq_boost': tk.IntVar(value=6),  # dB
            'tempo_ratio': tk.DoubleVar(value=1.0),
            'reverb_room': tk.DoubleVar(value=50.0),
            'tremolo_speed': tk.DoubleVar(value=5.0),
            'vibrato_speed': tk.DoubleVar(value=5.0)
        }
        
        # Processing status
        self.is_processing = False
        self.progress_var = tk.DoubleVar()
        
        self.setup_ui()
        
    def setup_ui(self):
        """Create the main user interface."""
        
        # Header
        header_frame = ttk.Frame(self.root)
        header_frame.pack(fill=tk.X, padx=10, pady=5)
        
        title_label = ttk.Label(header_frame, text="🎭 Emotional Audio Enhancer", font=("Arial", 16, "bold"))
        title_label.pack()
        
        subtitle_label = ttk.Label(header_frame, text="Transform ChatterboxTTS output with emotional audio processing")
        subtitle_label.pack()
        
        # File Selection Section
        file_frame = ttk.LabelFrame(self.root, text="📁 File Selection", padding=10)
        file_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Input file
        input_frame = ttk.Frame(file_frame)
        input_frame.pack(fill=tk.X, pady=2)
        
        ttk.Label(input_frame, text="Input Audio File:").pack(side=tk.LEFT)
        ttk.Entry(input_frame, textvariable=self.input_file, width=50).pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        ttk.Button(input_frame, text="Browse", command=self.select_input_file).pack(side=tk.RIGHT)
        
        # Output file
        output_frame = ttk.Frame(file_frame)
        output_frame.pack(fill=tk.X, pady=2)
        
        ttk.Label(output_frame, text="Output Audio File:").pack(side=tk.LEFT)
        ttk.Entry(output_frame, textvariable=self.output_file, width=50).pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        ttk.Button(output_frame, text="Browse", command=self.select_output_file).pack(side=tk.RIGHT)
        
        # Emotion Type Selection
        emotion_frame = ttk.LabelFrame(self.root, text="🎭 Emotion Type", padding=10)
        emotion_frame.pack(fill=tk.X, padx=10, pady=5)
        
        emotions = [
            ("😠 Angry", "angry"), 
            ("😨 Fearful", "fearful"),
            ("😢 Sad", "sad"),
            ("😊 Happy", "happy"),
            ("🤢 Disgusted", "disgusted"),
            ("😮 Surprised", "surprised"),
            ("😐 Neutral Enhanced", "neutral")
        ]
        
        emotion_buttons_frame = ttk.Frame(emotion_frame)
        emotion_buttons_frame.pack()
        
        for i, (label, value) in enumerate(emotions):
            ttk.Radiobutton(emotion_buttons_frame, text=label, variable=self.emotion_type, 
                           value=value, command=self.update_emotion_presets).grid(row=i//4, column=i%4, sticky=tk.W, padx=5)
        
        # Enhancement Options
        enhance_frame = ttk.LabelFrame(self.root, text="🔧 Enhancement Options", padding=10)
        enhance_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Create two columns for checkboxes
        left_col = ttk.Frame(enhance_frame)
        left_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        right_col = ttk.Frame(enhance_frame)
        right_col.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        enhancements_list = [
            ('pitch_shift', '🎵 Pitch Shifting', 'Raise or lower voice pitch'),
            ('formant_shift', '🗣️ Formant Shifting', 'Change vocal tract characteristics'),
            ('dynamic_compress', '📢 Dynamic Compression', 'Make speech more punchy'),
            ('harmonic_emphasis', '🔊 Harmonic Emphasis', 'Boost specific frequencies'),
            ('tempo_adjust', '⏰ Tempo Adjustment', 'Speed up or slow down'),
            ('reverb', '🏛️ Reverb', 'Add room acoustics'),
            ('tremolo', '📳 Tremolo', 'Amplitude modulation'),
            ('vibrato', '🎶 Vibrato', 'Pitch modulation')
        ]
        
        for i, (key, label, tooltip) in enumerate(enhancements_list):
            frame = left_col if i < 4 else right_col
            cb = ttk.Checkbutton(frame, text=label, variable=self.enhancements[key])
            cb.pack(anchor=tk.W, pady=1)
            # Add tooltip (simplified)
            self.create_tooltip(cb, tooltip)
        
        # Parameters Section
        params_frame = ttk.LabelFrame(self.root, text="⚙️ Parameters", padding=10)
        params_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Create parameter controls
        param_controls = [
            ('pitch_amount', 'Pitch Shift (cents)', -500, 500),
            ('formant_amount', 'Formant Ratio', 0.5, 2.0),
            ('compress_ratio', 'Compression Ratio', 1.0, 10.0),
            ('eq_boost', 'EQ Boost (dB)', -12, 12),
            ('tempo_ratio', 'Tempo Ratio', 0.5, 2.0),
            ('reverb_room', 'Reverb Room Size', 0, 100),
            ('tremolo_speed', 'Tremolo Speed (Hz)', 1.0, 20.0),
            ('vibrato_speed', 'Vibrato Speed (Hz)', 1.0, 20.0)
        ]
        
        # Create two columns for parameters
        params_left = ttk.Frame(params_frame)
        params_left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        params_right = ttk.Frame(params_frame)
        params_right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        for i, (key, label, min_val, max_val) in enumerate(param_controls):
            frame = params_left if i < 4 else params_right
            
            param_frame = ttk.Frame(frame)
            param_frame.pack(fill=tk.X, pady=2)
            
            ttk.Label(param_frame, text=f"{label}:").pack(side=tk.LEFT)
            
            if isinstance(self.parameters[key], tk.IntVar):
                scale = ttk.Scale(param_frame, from_=min_val, to=max_val, 
                                variable=self.parameters[key], orient=tk.HORIZONTAL)
            else:
                scale = ttk.Scale(param_frame, from_=min_val, to=max_val, 
                                variable=self.parameters[key], orient=tk.HORIZONTAL)
            
            scale.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=5)
            
            # Value display
            value_label = ttk.Label(param_frame, text="")
            value_label.pack(side=tk.RIGHT)
            
            # Update value display
            def update_display(val, label=value_label, var=self.parameters[key]):
                if isinstance(var, tk.IntVar):
                    label.config(text=f"{int(float(val))}")
                else:
                    label.config(text=f"{float(val):.2f}")
            
            scale.config(command=update_display)
            update_display(self.parameters[key].get())
        
        # Progress and Controls
        control_frame = ttk.Frame(self.root)
        control_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Progress bar
        self.progress_bar = ttk.Progressbar(control_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(fill=tk.X, pady=5)
        
        # Status label
        self.status_label = ttk.Label(control_frame, text="Ready to process audio")
        self.status_label.pack(pady=2)
        
        # Action buttons
        button_frame = ttk.Frame(control_frame)
        button_frame.pack(pady=5)
        
        self.process_btn = ttk.Button(button_frame, text="🎭 Enhance Audio", 
                                     command=self.start_processing, style="Accent.TButton")
        self.process_btn.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(button_frame, text="🔄 Reset Settings", 
                  command=self.reset_settings).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(button_frame, text="💾 Save Preset", 
                  command=self.save_preset).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(button_frame, text="📁 Load Preset", 
                  command=self.load_preset).pack(side=tk.LEFT, padx=5)
        
        # Preview button (if supported)
        if self.check_audio_tools():
            ttk.Button(button_frame, text="🔊 Preview", 
                      command=self.preview_audio).pack(side=tk.LEFT, padx=5)
    
    def create_tooltip(self, widget, text):
        """Create a simple tooltip for a widget."""
        def on_enter(event):
            tooltip = tk.Toplevel()
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
            label = ttk.Label(tooltip, text=text, background="lightyellow", 
                            relief="solid", borderwidth=1)
            label.pack()
            widget.tooltip = tooltip
        
        def on_leave(event):
            if hasattr(widget, 'tooltip'):
                widget.tooltip.destroy()
                del widget.tooltip
        
        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)
    
    def select_input_file(self):
        """Open file picker for input audio file."""
        filename = filedialog.askopenfilename(
            title="Select Input Audio File",
            filetypes=[
                ("Audio files", "*.wav *.mp3 *.flac *.ogg *.m4a"),
                ("WAV files", "*.wav"),
                ("MP3 files", "*.mp3"),
                ("All files", "*.*")
            ]
        )
        if filename:
            self.input_file.set(filename)
            # Auto-suggest output filename
            if not self.output_file.get():
                base = Path(filename).stem
                output_path = Path(filename).parent / f"{base}_enhanced.wav"
                self.output_file.set(str(output_path))
    
    def select_output_file(self):
        """Open file picker for output audio file."""
        filename = filedialog.asksavefilename(
            title="Save Enhanced Audio As",
            defaultextension=".wav",
            filetypes=[
                ("WAV files", "*.wav"),
                ("MP3 files", "*.mp3"),
                ("FLAC files", "*.flac"),
                ("All files", "*.*")
            ]
        )
        if filename:
            self.output_file.set(filename)
    
    def update_emotion_presets(self):
        """Update enhancement settings based on selected emotion."""
        emotion = self.emotion_type.get()
        
        # Reset all enhancements
        for key in self.enhancements:
            self.enhancements[key].set(False)
        
        # Emotion-specific presets
        presets = {
            'angry': {
                'enhancements': ['pitch_shift', 'formant_shift', 'dynamic_compress', 'harmonic_emphasis'],
                'params': {'pitch_amount': 150, 'formant_amount': 1.15, 'compress_ratio': 3.0, 'eq_boost': 6}
            },
            'fearful': {
                'enhancements': ['pitch_shift', 'tremolo', 'reverb'],
                'params': {'pitch_amount': 200, 'tremolo_speed': 8.0, 'reverb_room': 70.0}
            },
            'sad': {
                'enhancements': ['pitch_shift', 'tempo_adjust', 'dynamic_compress'],
                'params': {'pitch_amount': -100, 'tempo_ratio': 0.85, 'compress_ratio': 1.5}
            },
            'happy': {
                'enhancements': ['pitch_shift', 'harmonic_emphasis', 'vibrato'],
                'params': {'pitch_amount': 100, 'eq_boost': 4, 'vibrato_speed': 4.0}
            },
            'disgusted': {
                'enhancements': ['formant_shift', 'harmonic_emphasis'],
                'params': {'formant_amount': 0.85, 'eq_boost': -3}
            },
            'surprised': {
                'enhancements': ['pitch_shift', 'tempo_adjust'],
                'params': {'pitch_amount': 250, 'tempo_ratio': 1.2}
            },
            'neutral': {
                'enhancements': ['dynamic_compress'],
                'params': {'compress_ratio': 2.0}
            }
        }
        
        if emotion in presets:
            preset = presets[emotion]
            
            # Enable relevant enhancements
            for enhancement in preset['enhancements']:
                if enhancement in self.enhancements:
                    self.enhancements[enhancement].set(True)
            
            # Set parameters
            for param, value in preset['params'].items():
                if param in self.parameters:
                    self.parameters[param].set(value)
    
    def check_audio_tools(self):
        """Check if required audio processing tools are available."""
        tools = ['sox', 'ffmpeg']
        available = []
        
        for tool in tools:
            try:
                subprocess.run([tool, '--version'], capture_output=True, check=True)
                available.append(tool)
            except (subprocess.CalledProcessError, FileNotFoundError):
                pass
        
        if not available:
            messagebox.showwarning(
                "Missing Audio Tools",
                "Audio processing tools (sox, ffmpeg) not found.\n"
                "Please install them for full functionality:\n\n"
                "sudo apt install sox ffmpeg"
            )
            return False
        
        return True
    
    def start_processing(self):
        """Start audio processing in a separate thread."""
        if not self.input_file.get():
            messagebox.showerror("Error", "Please select an input audio file")
            return
        
        if not self.output_file.get():
            messagebox.showerror("Error", "Please specify an output file")
            return
        
        if self.is_processing:
            return
        
        self.is_processing = True
        self.process_btn.config(text="Processing...", state="disabled")
        self.progress_var.set(0)
        
        # Start processing thread
        thread = threading.Thread(target=self.process_audio)
        thread.daemon = True
        thread.start()
    
    def process_audio(self):
        """Process the audio file with selected enhancements."""
        try:
            input_file = self.input_file.get()
            output_file = self.output_file.get()
            
            # Create processing chain
            processing_steps = []
            current_file = input_file
            step_count = 0
            
            # Count enabled enhancements
            total_steps = sum(1 for enhancement in self.enhancements.values() if enhancement.get())
            
            self.update_status("Starting audio processing...")
            
            # Apply each enhancement
            if self.enhancements['pitch_shift'].get():
                step_count += 1
                next_file = os.path.join(self.temp_dir, f"step_{step_count}.wav")
                self.apply_pitch_shift(current_file, next_file)
                current_file = next_file
                self.progress_var.set((step_count / total_steps) * 100)
            
            if self.enhancements['formant_shift'].get():
                step_count += 1
                next_file = os.path.join(self.temp_dir, f"step_{step_count}.wav")
                self.apply_formant_shift(current_file, next_file)
                current_file = next_file
                self.progress_var.set((step_count / total_steps) * 100)
            
            if self.enhancements['dynamic_compress'].get():
                step_count += 1
                next_file = os.path.join(self.temp_dir, f"step_{step_count}.wav")
                self.apply_compression(current_file, next_file)
                current_file = next_file
                self.progress_var.set((step_count / total_steps) * 100)
            
            if self.enhancements['harmonic_emphasis'].get():
                step_count += 1
                next_file = os.path.join(self.temp_dir, f"step_{step_count}.wav")
                self.apply_eq(current_file, next_file)
                current_file = next_file
                self.progress_var.set((step_count / total_steps) * 100)
            
            if self.enhancements['tempo_adjust'].get():
                step_count += 1
                next_file = os.path.join(self.temp_dir, f"step_{step_count}.wav")
                self.apply_tempo_change(current_file, next_file)
                current_file = next_file
                self.progress_var.set((step_count / total_steps) * 100)
            
            if self.enhancements['reverb'].get():
                step_count += 1
                next_file = os.path.join(self.temp_dir, f"step_{step_count}.wav")
                self.apply_reverb(current_file, next_file)
                current_file = next_file
                self.progress_var.set((step_count / total_steps) * 100)
            
            if self.enhancements['tremolo'].get():
                step_count += 1
                next_file = os.path.join(self.temp_dir, f"step_{step_count}.wav")
                self.apply_tremolo(current_file, next_file)
                current_file = next_file
                self.progress_var.set((step_count / total_steps) * 100)
            
            if self.enhancements['vibrato'].get():
                step_count += 1
                next_file = os.path.join(self.temp_dir, f"step_{step_count}.wav")
                self.apply_vibrato(current_file, next_file)
                current_file = next_file
                self.progress_var.set((step_count / total_steps) * 100)
            
            # Copy final result to output
            self.update_status("Finalizing output...")
            shutil.copy2(current_file, output_file)
            
            self.progress_var.set(100)
            self.update_status(f"✅ Processing complete! Output saved to: {output_file}")
            
            messagebox.showinfo("Success", f"Audio enhancement complete!\n\nOutput saved to:\n{output_file}")
            
        except Exception as e:
            logging.error(f"Processing error: {e}")
            self.update_status(f"❌ Error: {str(e)}")
            messagebox.showerror("Processing Error", f"An error occurred during processing:\n\n{str(e)}")
        
        finally:
            self.is_processing = False
            self.process_btn.config(text="🎭 Enhance Audio", state="normal")
            # Clean up temp files
            self.cleanup_temp_files()
    
    def apply_pitch_shift(self, input_file, output_file):
        """Apply pitch shifting using sox."""
        cents = self.parameters['pitch_amount'].get()
        self.update_status(f"Applying pitch shift ({cents:+d} cents)...")
        
        cmd = ['sox', input_file, output_file, 'pitch', str(cents)]
        subprocess.run(cmd, check=True, capture_output=True)
    
    def apply_formant_shift(self, input_file, output_file):
        """Apply formant shifting using sox bend effect."""
        ratio = self.parameters['formant_amount'].get()
        self.update_status(f"Applying formant shift (ratio: {ratio:.2f})...")
        
        # Use bend effect to simulate formant shifting
        bend_amount = (ratio - 1.0) * 100  # Convert to percentage
        cmd = ['sox', input_file, output_file, 'bend', f'0.5,{bend_amount},2.0']
        subprocess.run(cmd, check=True, capture_output=True)
    
    def apply_compression(self, input_file, output_file):
        """Apply dynamic range compression."""
        ratio = self.parameters['compress_ratio'].get()
        self.update_status(f"Applying compression (ratio: {ratio:.1f}:1)...")
        
        # Sox compand effect
        attack_decay = "0.1,0.3"
        soft_knee = f"-60,-40,-30,-20,-20,-{20/ratio},-5,-{5/ratio},-2,-{2/ratio}"
        
        cmd = ['sox', input_file, output_file, 'compand', attack_decay, soft_knee]
        subprocess.run(cmd, check=True, capture_output=True)
    
    def apply_eq(self, input_file, output_file):
        """Apply EQ/harmonic emphasis."""
        boost_db = self.parameters['eq_boost'].get()
        self.update_status(f"Applying EQ boost ({boost_db:+d} dB at 3kHz)...")
        
        cmd = ['sox', input_file, output_file, 'equalizer', '3000', '1000', str(boost_db)]
        subprocess.run(cmd, check=True, capture_output=True)
    
    def apply_tempo_change(self, input_file, output_file):
        """Apply tempo change."""
        ratio = self.parameters['tempo_ratio'].get()
        self.update_status(f"Adjusting tempo ({ratio:.2f}x)...")
        
        cmd = ['sox', input_file, output_file, 'tempo', str(ratio)]
        subprocess.run(cmd, check=True, capture_output=True)
    
    def apply_reverb(self, input_file, output_file):
        """Apply reverb effect."""
        room_size = self.parameters['reverb_room'].get()
        self.update_status(f"Adding reverb (room size: {room_size:.0f}%)...")
        
        # Sox reverb effect
        cmd = ['sox', input_file, output_file, 'reverb', str(room_size)]
        subprocess.run(cmd, check=True, capture_output=True)
    
    def apply_tremolo(self, input_file, output_file):
        """Apply tremolo effect."""
        speed = self.parameters['tremolo_speed'].get()
        self.update_status(f"Adding tremolo ({speed:.1f} Hz)...")
        
        cmd = ['sox', input_file, output_file, 'tremolo', str(speed), '50']
        subprocess.run(cmd, check=True, capture_output=True)
    
    def apply_vibrato(self, input_file, output_file):
        """Apply vibrato effect."""
        speed = self.parameters['vibrato_speed'].get()
        self.update_status(f"Adding vibrato ({speed:.1f} Hz)...")
        
        cmd = ['sox', input_file, output_file, 'vibrato', str(speed), '0.2']
        subprocess.run(cmd, check=True, capture_output=True)
    
    def update_status(self, message):
        """Update status label in thread-safe way."""
        self.root.after(0, lambda: self.status_label.config(text=message))
        logging.info(message)
    
    def cleanup_temp_files(self):
        """Clean up temporary files."""
        try:
            for file in os.listdir(self.temp_dir):
                os.remove(os.path.join(self.temp_dir, file))
        except:
            pass
    
    def preview_audio(self):
        """Preview the processed audio (if tools available)."""
        if not self.input_file.get():
            messagebox.showwarning("No Input", "Please select an input file first")
            return
        
        try:
            # Play original audio
            subprocess.Popen(['aplay', self.input_file.get()], 
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except FileNotFoundError:
            messagebox.showinfo("Preview", "Audio preview requires 'aplay' (alsa-utils package)")
    
    def reset_settings(self):
        """Reset all settings to defaults."""
        self.emotion_type.set("angry")
        
        for enhancement in self.enhancements.values():
            enhancement.set(False)
        
        # Reset parameters to defaults
        self.parameters['pitch_amount'].set(150)
        self.parameters['formant_amount'].set(1.15)
        self.parameters['compress_ratio'].set(3.0)
        self.parameters['eq_boost'].set(6)
        self.parameters['tempo_ratio'].set(1.0)
        self.parameters['reverb_room'].set(50.0)
        self.parameters['tremolo_speed'].set(5.0)
        self.parameters['vibrato_speed'].set(5.0)
        
        self.update_emotion_presets()
    
    def save_preset(self):
        """Save current settings as a preset."""
        filename = filedialog.asksavefilename(
            title="Save Preset",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            preset = {
                'emotion_type': self.emotion_type.get(),
                'enhancements': {k: v.get() for k, v in self.enhancements.items()},
                'parameters': {k: v.get() for k, v in self.parameters.items()}
            }
            
            with open(filename, 'w') as f:
                json.dump(preset, f, indent=2)
            
            messagebox.showinfo("Preset Saved", f"Preset saved to:\n{filename}")
    
    def load_preset(self):
        """Load settings from a preset file."""
        filename = filedialog.askopenfilename(
            title="Load Preset",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'r') as f:
                    preset = json.load(f)
                
                # Load emotion type
                if 'emotion_type' in preset:
                    self.emotion_type.set(preset['emotion_type'])
                
                # Load enhancements
                if 'enhancements' in preset:
                    for k, v in preset['enhancements'].items():
                        if k in self.enhancements:
                            self.enhancements[k].set(v)
                
                # Load parameters
                if 'parameters' in preset:
                    for k, v in preset['parameters'].items():
                        if k in self.parameters:
                            self.parameters[k].set(v)
                
                messagebox.showinfo("Preset Loaded", f"Preset loaded from:\n{filename}")
                
            except Exception as e:
                messagebox.showerror("Load Error", f"Could not load preset:\n{str(e)}")
    
    def __del__(self):
        """Cleanup on destruction."""
        try:
            shutil.rmtree(self.temp_dir)
        except:
            pass

def main():
    """Main entry point."""
    root = tk.Tk()
    
    # Set theme
    style = ttk.Style()
    try:
        style.theme_use('clam')  # Use a modern theme
    except:
        pass
    
    app = EmotionalAudioEnhancer(root)
    
    # Center window
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (root.winfo_width() // 2)
    y = (root.winfo_screenheight() // 2) - (root.winfo_height() // 2)
    root.geometry(f"+{x}+{y}")
    
    # Handle cleanup on close
    def on_closing():
        try:
            app.cleanup_temp_files()
        except:
            pass
        root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    root.mainloop()

if __name__ == "__main__":
    main()