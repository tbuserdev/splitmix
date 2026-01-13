import os
import yt_dlp
from pathlib import Path


def download_youtube(url: str, output_dir: str = "data") -> dict:
    """
    Downloads audio and thumbnail from YouTube URL.

    Args:
        url: YouTube video URL
        output_dir: Directory to save downloaded files

    Returns:
        {
            "title": "Video Title",
            "audio_path": "/path/to/input.wav",
            "cover_path": "/path/to/cover.jpg",
            "duration": "1:23:45"
        }
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    audio_path = os.path.join(output_dir, "input.wav")
    cover_path = os.path.join(output_dir, "cover.jpg")

    # Configure yt-dlp options
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": os.path.join(output_dir, "temp_audio.%(ext)s"),
        "writethumbnail": True,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "wav",
            },
            {
                "key": "FFmpegThumbnailsConvertor",
                "format": "jpg",
            },
        ],
        "quiet": False,
        "no_warnings": False,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Extract video info
            info = ydl.extract_info(url, download=True)

            # Get video metadata
            title = info.get("title", "Unknown Title")
            duration_seconds = info.get("duration", 0)

            # Format duration as HH:MM:SS
            hours = duration_seconds // 3600
            minutes = (duration_seconds % 3600) // 60
            seconds = duration_seconds % 60

            if hours > 0:
                duration = f"{hours}:{minutes:02d}:{seconds:02d}"
            else:
                duration = f"{minutes}:{seconds:02d}"

            # Rename downloaded files to standard names
            # Find the downloaded audio file
            temp_audio_candidates = list(Path(output_dir).glob("temp_audio.wav"))
            if temp_audio_candidates:
                # Remove existing input.wav if it exists
                if os.path.exists(audio_path):
                    os.remove(audio_path)
                temp_audio_candidates[0].rename(audio_path)
            else:
                raise FileNotFoundError("Downloaded audio file not found")

            # Find and rename thumbnail - try multiple patterns
            # yt-dlp might create: temp_audio.jpg, temp_audio.webp.jpg, etc.
            thumbnail_patterns = [
                "temp_audio*.jpg",
                "temp_audio*.webp",
                "temp_audio*.png",
            ]

            thumbnail_found = False
            for pattern in thumbnail_patterns:
                temp_thumbnail_candidates = list(Path(output_dir).glob(pattern))
                if temp_thumbnail_candidates:
                    # Remove existing cover.jpg if it exists
                    if os.path.exists(cover_path):
                        os.remove(cover_path)
                    temp_thumbnail_candidates[0].rename(cover_path)
                    thumbnail_found = True
                    break

            if not thumbnail_found:
                # Try to extract thumbnail URL and download it manually
                print(
                    "Warning: Thumbnail not found in downloaded files, attempting manual download..."
                )
                thumbnail_url = info.get("thumbnail")
                if thumbnail_url:
                    import urllib.request

                    try:
                        urllib.request.urlretrieve(thumbnail_url, cover_path)
                        thumbnail_found = True
                        print(
                            f"Successfully downloaded thumbnail from: {thumbnail_url}"
                        )
                    except Exception as e:
                        print(f"Failed to download thumbnail: {e}")
                        cover_path = None
                else:
                    cover_path = None

            return {
                "title": title,
                "audio_path": audio_path,
                "cover_path": cover_path if thumbnail_found else None,
                "duration": duration,
            }

    except Exception as e:
        raise Exception(f"Failed to download video: {str(e)}")
