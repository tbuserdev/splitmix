# SplitMix 🎵

Download and split YouTube audio into tagged MP3 tracks with metadata and cover art.

## Features

- Download audio from YouTube videos (DJ sets, mixes, live sets, etc.)
- Automatically extract video thumbnail as cover art
- Web-based interface with Streamlit
- Split audio into individual tracks based on timestamps
- Add ID3 metadata (artist, album, title, track number)
- Embed cover art into each track
- Export as high-quality 320kbps MP3 files
- Download all tracks as a ZIP file
- Docker support for easy deployment

## Prerequisites

### Local Development

1. **Python 3.11+** installed on your system

2. **FFmpeg** - Required for audio processing
   - **macOS**: `brew install ffmpeg`
   - **Linux**: `sudo apt update && sudo apt install ffmpeg`
   - **Windows**: Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add to PATH

3. **uv** (recommended) or pip for dependency management
   - Install uv: `curl -LsSf https://astral.sh/uv/install.sh | sh`

### Docker

- Docker and Docker Compose installed

## Installation

### Local Development

```bash
# Clone the repository
git clone <your-repo-url>
cd splitmix

# Install dependencies using uv
uv sync

# Or using pip
pip install pydub mutagen streamlit yt-dlp
```

### Docker

```bash
# Build and run with Docker Compose
docker-compose up -d

# Access at http://localhost:8501
```

## Usage

### Web Interface (Recommended)

1. **Start the application**
   ```bash
   # Local development
   uv run streamlit run app.py
   
   # Or with Docker
   docker-compose up -d
   ```

2. **Open your browser** to `http://localhost:8501`

3. **Follow the steps in the UI:**
   - Paste a YouTube URL
   - Click "Download Audio & Thumbnail"
   - Edit the Artist and Album names (auto-filled from video title)
   - Paste timestamps in the format:
     ```
     00:00 - Track 1 Name
     03:24 - Track 2 Name
     07:15 - Track 3 Name
     ```
   - Click "Split Tracks"
   - Download the ZIP file with all tracks
   - Optionally delete all files to clean up

### Command Line Interface

The original CLI is still available:

```bash
python main.py "input.wav" \
  --artist "Artist Name" \
  --album "Album Name" \
  --tracklist "timestamps.txt" \
  --cover "cover.jpg"
```

**Arguments:**
- `source_file` - Path to audio file (WAV, MP3, M4A, etc.)
- `--artist` - Artist name for metadata
- `--album` - Album name for metadata
- `--tracklist` - Path to text file with timestamps
- `--cover` - (Optional) Path to cover image (JPG, PNG)
- `--output_dir` - (Optional) Output directory (default: `output_tracks`)

## Timestamp Format

Timestamps should be in one of these formats:

```
MM:SS - Track Name
HH:MM:SS - Track Name
```

**Example:**
```
00:00 - LIGHTNING
03:01 - NERVOUS
06:41 - CURIOUS
09:43 - Unreleased #1
11:12 - Proper Education (Eric Prydz, Floyd)
```

## Docker Deployment

### Using Pre-built Image from GitHub Container Registry (Recommended)

```bash
# Pull and run using docker-compose
docker-compose -f docker-compose.prod.yml up -d

# Or pull and run directly
docker pull ghcr.io/tbuserdev/splitmix:latest
docker run -d -p 8501:8501 --name splitmix ghcr.io/tbuserdev/splitmix:latest
```

**Note**: The image is automatically built and pushed to GitHub Container Registry on every push to the `main` branch.

### Using Docker Compose (Build Locally)

```bash
# Start the service
docker-compose -f docker-compose.local.yml up -d

# View logs
docker-compose logs -f

# Stop the service
docker-compose down
```

### Using Docker directly

```bash
# Build the image
docker build -t splitmix .

# Run the container
docker run -d -p 8501:8501 --name splitmix splitmix

# Stop the container
docker stop splitmix
docker rm splitmix
```

### Environment Variables

You can customize the Streamlit configuration using environment variables:

```yaml
environment:
  - STREAMLIT_SERVER_PORT=8501
  - STREAMLIT_SERVER_ADDRESS=0.0.0.0
  - STREAMLIT_SERVER_HEADLESS=true
```

## Project Structure

```
splitmix/
├── main.py              # Core splitting logic
├── app.py               # Streamlit web interface
├── downloader.py        # YouTube download wrapper
├── pyproject.toml       # Python dependencies
├── Dockerfile           # Docker image definition
├── docker-compose.yml   # Docker Compose configuration
├── .dockerignore        # Docker build exclusions
└── README.md            # This file
```

## How It Works

1. **Download**: Uses `yt-dlp` to download the best audio quality from YouTube and extract the thumbnail
2. **Convert**: Converts audio to WAV format using FFmpeg (if needed)
3. **Parse**: Reads timestamps and track names from your input
4. **Split**: Uses `pydub` to slice the audio at each timestamp
5. **Export**: Exports each track as 320kbps MP3 with metadata
6. **Tag**: Uses `mutagen` to embed ID3 tags and cover art
7. **Package**: Creates a ZIP file with all tracks for download
8. **Cleanup**: Optionally deletes all working files

## Troubleshooting

### "Error loading audio file"
- Ensure FFmpeg is installed and in your PATH
- Try converting your audio file to WAV first

### "Could not parse any tracks"
- Check timestamp format (MM:SS or HH:MM:SS)
- Ensure there's a space-dash-space ` - ` between timestamp and title
- Make sure each timestamp is on a new line

### Docker container won't start
- Check if port 8501 is already in use: `lsof -i :8501`
- View logs: `docker-compose logs -f`
- Ensure FFmpeg is included in the Docker image

### Download fails
- Check your internet connection
- Verify the YouTube URL is correct and the video is accessible
- Some videos may be restricted or age-gated

## Tips

- For best results, use YouTube videos that have the tracklist in the description
- The video title will auto-fill the Artist and Album fields, but you can edit them
- Use descriptive track names - they'll appear in music players
- Cover art is automatically extracted from the video thumbnail
- The output folder will be created inside the `data/` directory when using the web interface

## Development

```bash
# Install dependencies
uv sync

# Run locally
uv run streamlit run app.py

# Run CLI tests
uv run python main.py "test.wav" --artist "Test" --album "Test" --tracklist "timestamps.txt"
```

## License

MIT

## Credits

- Built with [Streamlit](https://streamlit.io/)
- Audio processing by [pydub](https://github.com/jiaaro/pydub)
- Metadata handling by [mutagen](https://mutagen.readthedocs.io/)
- YouTube downloads by [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- Audio conversion by [FFmpeg](https://ffmpeg.org/)
