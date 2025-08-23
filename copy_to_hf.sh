#!/bin/bash

# Copy updated Gradio files to HuggingFace deployment folder
SOURCE_DIR="/home/danno/MyApps/chatterbox (copy)/gradio_tabs"
DEST_DIR="/home/danno/MyApps/chatterbox (copy)/ChatterboxTTS-DNXS-Spokenwordv1/gradio_tabs"

echo "Copying HuggingFace-compatible Gradio files..."

# Copy each file
cp "$SOURCE_DIR/tab1_convert_book.py" "$DEST_DIR/"
cp "$SOURCE_DIR/tab2_configuration.py" "$DEST_DIR/"  
cp "$SOURCE_DIR/tab4_combine_audio.py" "$DEST_DIR/"
cp "$SOURCE_DIR/tab5_prepare_text.py" "$DEST_DIR/"
cp "$SOURCE_DIR/tab7_chunk_tools.py" "$DEST_DIR/"
cp "$SOURCE_DIR/tab8_json_generate.py" "$DEST_DIR/"

echo "Files copied successfully!"
ls -la "$DEST_DIR"