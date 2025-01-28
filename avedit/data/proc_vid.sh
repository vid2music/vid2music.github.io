#!/usr/bin/env bash
# Converts each file.mp4 under */XXX/ into the corresponding folder */XXX_new/ 
# with the same filename, using web-friendly H.264/AAC settings.

for f in ./*/*.mp4; do
  # "f" might look like "SomeFolder/XXX/video.mp4"
  # Parse out directory and filename
  dir="$(dirname "$f")"          # e.g. "SomeFolder/XXX"
  file="$(basename "$f")"        # e.g. "video.mp4"
  
  # Build the new output directory by appending "_new"
  outdir="${dir}_new"            # e.g. "SomeFolder/XXX_new"
  
  # Create the output directory if it doesn't exist
  mkdir -p "$outdir"
  
  # Construct the output path, preserving the same filename
  outpath="$outdir/$file"
  
  echo "Converting: $f"
  echo "    Output: $outpath"
  
  # FFmpeg command:
  ffmpeg -i "$f" \
    -c:v libx264 -crf 23 -preset medium -pix_fmt yuv420p \
    -c:a aac -b:a 128k -movflags +faststart \
    "$outpath"
done

echo "All conversions complete!"
