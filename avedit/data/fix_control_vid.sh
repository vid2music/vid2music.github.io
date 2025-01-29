#!/bin/bash

# Directory containing the files
TARGET_DIR="ControlVideo_no_sound"

# Ensure the directory exists
if [ -d "$TARGET_DIR" ]; then
    for file in "$TARGET_DIR"/*; do
        if [[ -f "$file" ]]; then
            # Extract filename
            filename=$(basename -- "$file")
            
            # Replace only the first underscore after the six-digit number with '@'
            new_filename=$(echo "$filename" | sed -E 's/([0-9]{6})_/\1@/')

            # Rename the file if the name has changed
            if [[ "$filename" != "$new_filename" ]]; then
                mv "$TARGET_DIR/$filename" "$TARGET_DIR/$new_filename"
                echo "Renamed: $filename -> $new_filename"
            fi
        fi
    done
    echo "Renaming complete."
else
    echo "Directory $TARGET_DIR not found!"
fi
