import csv
import os
import subprocess
import sys

INPUT_CSV = "Ejemplo.csv" #Change name of your csv
OUTPUT_TXT = "songs_list.txt"
OUTPUT_FOLDER = "music"

# 1. Parse CSV and save tracks to songs_list.txt
if not os.path.isfile(INPUT_CSV):
    print(f"Error: '{INPUT_CSV}' not found in the current directory.")
    sys.exit(1)

songs = []
with open(INPUT_CSV, mode="r", encoding="utf-8") as infile:
    reader = csv.DictReader(infile)
    for row in reader:
        artist = row.get("Artist Name(s)") or row.get("Artist Name") or row.get("Artist")
        track = row.get("Track Name") or row.get("Title") or row.get("Song")

        if artist and track:
            songs.append(f"{artist.strip()} - {track.strip()}")

if not songs:
    print("No valid tracks found in the CSV file.")
    sys.exit(1)

with open(OUTPUT_TXT, mode="w", encoding="utf-8") as outfile:
    outfile.write("\n".join(songs) + "\n")

print(f"Saved {len(songs)} tracks into '{OUTPUT_TXT}'.")

# 2. Download songs using yt-dlp
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

with open(OUTPUT_TXT, "r", encoding="utf-8") as f:
    for line in f:
        song = line.strip()
        if not song:
            continue

        print("=" * 50)
        print(f"Downloading: {song}")
        print("=" * 50)

        output_template = os.path.join(OUTPUT_FOLDER, "%(title)s [%(id)s].%(ext)s")

        cmd = [
            "yt-dlp",
            "--js-runtimes", "node",
            "--extract-audio",
            "--audio-format", "mp3",
            "--audio-quality", "0",
            "--extractor-args", "youtube:player_client=android",
            "--default-search", "ytsearch1",
            "-o", output_template,
            song,
        ]

        try:
            subprocess.run(cmd, check=True)
        except FileNotFoundError:
            print("Error: 'yt-dlp' is not installed or not added to system PATH.")
            sys.exit(1)
        except subprocess.CalledProcessError as e:
            print(f"Failed to download '{song}': Process exited with code {e.returncode}")

print("\nAll downloads completed!")