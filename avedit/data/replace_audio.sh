#!/bin/bash

# Define directories
SOURCE_AUDIO_DIR="RAVE"
TARGET_DIRS=("TokenFlow_no_sound" "ControlVideo_no_sound")

# Create a backup directory for safety
mkdir -p backup

# Loop through each target directory
for TARGET_DIR in "${TARGET_DIRS[@]}"; do
    if [ -d "$TARGET_DIR" ]; then
        for video_file in "$TARGET_DIR"/*; do
            if [[ -f "$video_file" ]]; then
                filename=$(basename -- "$video_file")
                audio_file="$SOURCE_AUDIO_DIR/$filename"

                # Ensure the corresponding audio file exists
                if [ -f "$audio_file" ]; then
                    echo "Processing: $filename"

                    # Backup the original file
                    cp "$video_file" "backup/$filename"

                    # Replace video with new one containing the original audio
                    ffmpeg -i "$video_file" -i "$audio_file" -c:v copy -c:a aac -strict experimental "temp_$filename"
                    
                    # Replace the original file with the new one
                    mv "temp_$filename" "$video_file"
                else
                    echo "Skipping $filename: No matching audio file found in $SOURCE_AUDIO_DIR"
                fi
            fi
        done
    else
        echo "Skipping $TARGET_DIR: Directory not found"
    fi
done

echo "Processing complete."
