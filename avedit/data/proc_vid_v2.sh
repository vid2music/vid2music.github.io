#!/usr/bin/env bash

# This script uses `find` to locate every .mp4 file (case-insensitive) under a given directory
# (default: current directory). It then processes each file with ffmpeg's `-movflags faststart`
# and overwrites the original file.

# Usage:
#   ./bulk_ffmpeg_faststart.sh [DIRECTORY]
#
# If DIRECTORY is not provided, it defaults to the current directory (.)

set -euo pipefail

# Use the first script argument as the directory to search, or default to current directory.
SEARCH_DIR="${1:-.}"

# Use 'find' in combination with '-print0' to handle filenames with spaces or special characters.
# The read loop will process each file safely.
find "$SEARCH_DIR" -type f -iname "*.mp4" -print0 | while IFS= read -r -d '' file; do
  echo "Processing: $file"

  # Create a temporary output name with an .mp4 extension so ffmpeg recognizes the format.
  temp_file="${file}.temp.mp4"

  # Run ffmpeg to place the moov atom at the front (faststart) and copy streams without re-encoding.
  ffmpeg -y -i "$file" -movflags faststart -c copy "$temp_file"

  # Check ffmpeg result
  if [[ $? -eq 0 ]]; then
    # If successful, remove the original and rename the temp file to the original name.
    rm "$file"
    mv "$temp_file" "$file"
    echo "  -> Successfully replaced with faststart version."
  else
    # If there's an error, remove the temp file to avoid clutter.
    echo "  !! Error processing $file"
    rm -f "$temp_file"
  fi

  echo
done
