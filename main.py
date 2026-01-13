import os
from pydub import AudioSegment
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, APIC
import argparse
import re

def parse_time_to_ms(time_str):
    """Converts a MM:SS or HH:MM:SS string to milliseconds."""
    parts = list(map(int, time_str.split(':')))
    ms = 0
    if len(parts) == 3:  # HH:MM:SS
        ms = (parts[0] * 3600 + parts[1] * 60 + parts[2]) * 1000
    elif len(parts) == 2:  # MM:SS
        ms = (parts[0] * 60 + parts[1]) * 1000
    return ms

def parse_tracklist(tracklist_str):
    """Parses the multiline string of timestamps and titles."""
    tracks = []
    # Regex to find timestamps (HH:MM:SS or MM:SS) and titles
    pattern = re.compile(r'(\d{1,2}:\d{2}(?::\d{2})?)\s*-\s*(.+)')
    for line in tracklist_str.strip().split('\n'):
        match = pattern.match(line.strip())
        if match:
            start_time_str, title = match.groups()
            start_ms = parse_time_to_ms(start_time_str)
            tracks.append({'start_ms': start_ms, 'title': title.strip()})
    
    # Sort tracks by start time just in case they are not in order
    tracks.sort(key=lambda x: x['start_ms'])
    return tracks

def split_wav_file(source_file, tracklist_str, artist_name, album_name, output_dir='output_tracks', cover_art_path=None):
    """
    Splits a WAV file into multiple MP3 tracks based on a tracklist,
    and applies metadata and album art.
    """
    try:
        # Load the audio file
        print(f"Loading audio file: {source_file}...")
        audio = AudioSegment.from_wav(source_file)
        print("Audio file loaded successfully.")
    except FileNotFoundError:
        print(f"Error: The file '{source_file}' was not found.")
        return
    except Exception as e:
        print(f"Error loading audio file: {e}")
        print("Please ensure ffmpeg is installed and accessible in your system's PATH.")
        return

    # Parse the tracklist
    tracks = parse_tracklist(tracklist_str)
    if not tracks:
        print("Could not parse any tracks from the timestamp list. Please check the format.")
        return

    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created output directory: {output_dir}")

    # Determine end times and export each track
    for i, track in enumerate(tracks):
        start_ms = track['start_ms']
        # End time is the start of the next track, or the end of the audio for the last track
        end_ms = tracks[i + 1]['start_ms'] if i + 1 < len(tracks) else len(audio)
        title = track['title']
        
        track_num = i + 1
        
        # Sanitize title for the filename
        safe_filename = re.sub(r'[\\/*?:"<>|]', "", f"{track_num:02d} - {title}.mp3")
        output_path = os.path.join(output_dir, safe_filename)

        print(f"[{track_num}/{len(tracks)}] Exporting: '{title}'...")

        # Slice the audio
        track_audio = audio[start_ms:end_ms]

        # Export as MP3 with metadata
        track_audio.export(
            output_path,
            format="mp3",
            bitrate="320k",
            tags={
                'artist': artist_name,
                'album': album_name,
                'title': title,
                'track': str(track_num)
            }
        )
        
        # Add album art using mutagen for better compatibility
        if cover_art_path:
            try:
                audio_file = EasyID3(output_path)
                audio_file.save() # Save EasyID3 tags first
                
                audio_file = ID3(output_path)
                with open(cover_art_path, 'rb') as art:
                    audio_file.add(APIC(
                        encoding=3, # 3 is for utf-8
                        mime='image/jpeg', # image/jpeg or image/png
                        type=3, # 3 is for the cover (front) image
                        desc=u'Cover',
                        data=art.read()
                    ))
                audio_file.save()
                print(f"   -> Added cover art to '{safe_filename}'")
            except Exception as e:
                print(f"   -> Warning: Could not add cover art. Error: {e}")

        print(f"   -> Successfully saved to '{output_path}'")

    print("\nProcessing complete!")

def main():
    parser = argparse.ArgumentParser(description="Split a WAV file into multiple MP3 tracks with metadata based on a timestamp list.")
    parser.add_argument("source_file", help="Path to the source WAV file.")
    parser.add_argument("--artist", required=True, help="Artist name for the metadata.")
    parser.add_argument("--album", required=True, help="Album name for the metadata.")
    parser.add_argument("--tracklist", required=True, help="Path to a .txt file containing the timestamps and titles.")
    parser.add_argument("--output_dir", default="output_tracks", help="Directory to save the output tracks (default: 'output_tracks').")
    parser.add_argument("--cover", help="Path to an image file (e.g., cover.jpg) to embed as album art.")
    
    args = parser.parse_args()

    try:
        with open(args.tracklist, 'r', encoding='utf-8') as f:
            tracklist_content = f.read()
    except FileNotFoundError:
        print(f"Error: The tracklist file '{args.tracklist}' was not found.")
        return
    except Exception as e:
        print(f"Error reading tracklist file: {e}")
        return

    split_wav_file(args.source_file, tracklist_content, args.artist, args.album, args.output_dir, args.cover)

if __name__ == "__main__":
    # To run this script, use the command line. Example:
    # python wav_splitter.py "path/to/your/audio.wav" --artist "Artist Name" --album "Album Name" --tracklist "path/to/timestamps.txt" --cover "path/to/cover.jpg"
    main()
