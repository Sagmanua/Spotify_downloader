#!/usr/bin/env bash

# Path to the file containing song names
INPUT_FILE="songs_list.txt"

# Check if the list file exists
if [[ ! -f "$INPUT_FILE" ]]; then
    echo "Error: $INPUT_FILE not found in the current directory."
    exit 1
fi

# Read the list line by line and download each song
while IFS= read -r song || [[ -n "$song" ]]; do
    # Skip empty lines
    [[ -z "$song" ]] && continue

    echo "=================================================="
    echo "Downloading: $song"
    echo "=================================================="

    yt-dlp \
        --js-runtimes node \
        --extract-audio \
        --audio-format mp3 \
        --audio-quality 0 \
        --extractor-args "youtube:player_client=android" \
        --default-search "ytsearch1" \
        "$song"

done < "$INPUT_FILE"

echo "All downloads completed!"
