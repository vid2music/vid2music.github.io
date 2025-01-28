#!/usr/bin/env bash

# This script looks for files matching the pattern '*@*.mp4'
# and replaces underscores in the part after "@" but before ".mp4".

for file in ./*/*@*.mp4; do
  # Skip if not a regular file (in case the pattern matches something unusual)
  [ -f "$file" ] || continue

  # Separate the parts of the filename.
  prefix="${file%@*}"       # everything before '@'
  suffix="${file#*@}"       # everything after '@'
  basename="${suffix%.mp4}" # remove the ".mp4" extension from suffix

  # Replace underscores with spaces in the basename part only.
  new_basename="${basename//_/ }"

  # Construct the new filename: prefix@new_basename.mp4
  new_name="${prefix}@${new_basename}.mp4"

  # Rename only if there's an actual change.
  if [[ "$new_name" != "$file" ]]; then
    mv -- "$file" "$new_name"
    echo "Renamed '$file' -> '$new_name'"
  fi
done
