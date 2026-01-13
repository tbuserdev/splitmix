# SplitMix - Agent Conversation History

## Project Overview
**SplitMix** - A tool that downloads YouTube audio (DJ sets, mixes) and splits them into individual MP3 tracks with metadata and cover art.

---

## What We Accomplished

### 1. **Initial Assessment**
- User had a CLI tool (`main.py`) that required:
  - Manually dropping `input.wav` into project folder
  - Manually adding `cover.jpg`
  - Editing `timestamps.txt` file
  - Running command-line script with arguments

### 2. **Implementation Plan (PLAN.md)**
Created comprehensive plan to:
- Build Streamlit web interface
- Add YouTube download via yt-dlp
- Add Docker support for network deployment
- Auto-fill metadata from video titles
- Add ZIP download and cleanup features

### 3. **Files Created**
- **`app.py`** (221 lines) - Streamlit web interface
- **`downloader.py`** (120 lines) - YouTube download wrapper using yt-dlp
- **`Dockerfile`** - Docker container configuration
- **`docker-compose.yml`** - Easy deployment setup
- **`.dockerignore`** - Docker build optimization

### 4. **Files Modified**
- **`main.py`** - Added progress callback, multi-format support, returns file list
- **`pyproject.toml`** - Added dependencies (streamlit, yt-dlp, pydub, mutagen)
- **`README.md`** - Complete documentation for web and Docker usage
- **`.gitignore`** - Excluded data/, metadata.json, custom_cover.jpg

### 5. **Bug Fixes & Enhancements**

#### Issue #1: Duplicate Notifications
- **Problem**: Status messages appeared twice (in button handler + persistent display)
- **Fixed**: Removed duplicate messages from button handlers, kept only persistent status

#### Issue #2: Lost State on Page Reload
- **Problem**: Streamlit session state lost when reloading page
- **Solution**: Implemented file-based persistence
  - Created `save_metadata()` and `load_metadata()` functions
  - Saves to `data/metadata.json` (artist, album, title)
  - `restore_session_from_files()` checks for existing files on startup
  - Detects existing audio, cover, and output MP3 files
  - Auto-restores session state

#### Issue #3: YouTube Thumbnail Not Downloading
- **Problem**: Cover image from YouTube wasn't being saved
- **Solution**: Enhanced `downloader.py`
  - Added multiple file pattern matching (*.jpg, *.webp, *.png)
  - Added fallback: direct download from thumbnail URL using urllib
  - Better error handling and debug messages

#### Issue #4: No Cover Preview/Upload
- **Problem**: User couldn't see or replace the cover image
- **Solution**: Added cover art section with:
  - Side-by-side layout (downloaded vs custom)
  - Image preview at 300px width
  - File uploader for custom covers (JPG, PNG, WEBP)
  - Automatic replacement when custom cover uploaded

---

## Current Project Structure

```
splitmix/
├── app.py                 # Streamlit web UI (main application)
├── downloader.py          # YouTube download logic
├── main.py                # Core splitting logic (CLI still works)
├── pyproject.toml         # Dependencies
├── PLAN.md                # Implementation plan
├── README.md              # Documentation
├── AGENTS.md              # This file - conversation history
├── Dockerfile             # Container image
├── docker-compose.yml     # Deployment config
├── .dockerignore          # Docker exclusions
├── .gitignore             # Git exclusions
├── data/                  # Runtime working directory
│   ├── input.wav          # Downloaded audio
│   ├── cover.jpg          # YouTube thumbnail
│   ├── custom_cover.jpg   # User-uploaded cover (optional)
│   ├── metadata.json      # Persistent session data
│   └── output_tracks/     # Generated MP3 files
└── .venv/                 # Python virtual environment
```

---

## How The App Works Now

### User Workflow:
1. **Paste YouTube URL** → Click "Download Audio & Thumbnail"
2. **View Cover Art** → Preview downloaded thumbnail or upload custom
3. **Edit Metadata** → Artist and Album (auto-filled from video title)
4. **Paste Timestamps** → Format: `00:00 - Track Name`
5. **Click "Split Tracks"** → Watch progress bar
6. **Download ZIP** → Get all MP3s in one file
7. **Delete All Files** → Clean up for next project

### Persistence Features:
- Page reload restores everything
- Works in Docker containers
- Detects existing downloads/splits
- No data loss

---

## Key Technologies

- **Streamlit** - Web interface
- **yt-dlp** - YouTube downloads
- **pydub** - Audio manipulation
- **mutagen** - MP3 metadata/ID3 tags
- **FFmpeg** - Audio conversion
- **Docker** - Containerization

---

## Running The App

**Local Development:**
```bash
uv run streamlit run app.py
# Access at http://localhost:8501
```

**Docker Deployment:**
```bash
docker-compose up -d
# Access at http://<server-ip>:8501
```

---

## Recent Changes (Last Session)

1. ✅ Fixed duplicate notifications in download and split sections
2. ✅ Implemented file-based persistence (survives page reload)
3. ✅ Fixed YouTube thumbnail download with fallback mechanism
4. ✅ Added cover art preview (downloaded + custom upload side-by-side)

---

## Potential Next Steps (if needed)

- Add timestamp auto-detection from video description
- Add audio waveform visualization
- Add batch processing (multiple videos)
- Add track preview/playback
- Add progress persistence for large files
- Add error recovery (resume failed splits)
- Add preset templates for common DJ set formats
- Add metadata editing after splitting
- Add direct Spotify/Apple Music artwork fetching

---

## Files To Focus On For Modifications

- **`app.py`** - All UI changes, new features, layout modifications
- **`downloader.py`** - YouTube download improvements, format support
- **`main.py`** - Core audio splitting logic, metadata handling

---

## Known Working Features

✅ YouTube download with audio + thumbnail  
✅ Custom cover upload  
✅ Side-by-side cover preview  
✅ Metadata auto-fill and persistence  
✅ Real-time progress tracking  
✅ ZIP download of all tracks  
✅ File cleanup  
✅ Session persistence across reloads  
✅ Docker deployment ready  
✅ Multi-format audio support (WAV, MP3, M4A)

---

## Current State: FULLY FUNCTIONAL

The application is complete and working. All planned features implemented. Ready for deployment and use.

---

## Development Notes for Future AI Agents

### Context for New Sessions
- This project evolved from a CLI tool to a full web application
- State persistence was a critical requirement (Streamlit sessions are ephemeral)
- User workflow optimized for DJ mix splitting (common use case)
- File-based state (`metadata.json`) is the source of truth

### Code Patterns Used
- Streamlit session state for UI reactivity
- File system as persistence layer
- Progress callbacks for long-running operations
- Defensive coding for missing files/directories

### Known Limitations
- Single-user design (no multi-tenancy)
- No authentication/authorization
- File cleanup is manual (user-initiated)
- No automated timestamp detection yet

### Testing Checklist
When making changes, verify:
1. YouTube download with thumbnail
2. Custom cover upload and replacement
3. Page reload restores state correctly
4. Track splitting with progress bar
5. ZIP download contains all tracks with correct metadata
6. File cleanup removes all data files
7. Docker build and deployment works

### Architecture Decisions
- **Why Streamlit?** Rapid prototyping, built-in UI components
- **Why yt-dlp?** Most reliable YouTube downloader, active maintenance
- **Why file-based persistence?** Simple, no database needed, survives container restarts
- **Why pydub?** Pythonic API, easier than raw FFmpeg
- **Why mutagen?** Better ID3 tag support than pydub alone

---

## Agent Handoff Protocol

When a new AI agent takes over this project:

1. **Read this file first** to understand the full context
2. **Check PLAN.md** for original requirements
3. **Review README.md** for user-facing documentation
4. **Test the application** before making changes:
   ```bash
   uv run streamlit run app.py
   ```
5. **Preserve existing functionality** - all features are working
6. **Update this file** with any significant changes or decisions
7. **Maintain the testing checklist** when adding features

---

## Contact & Contribution

This is a personal project by the repository owner. Future AI agents should maintain code quality and user experience standards established in this implementation.

**Last Updated:** 2026-01-13  
**Status:** Production Ready  
**Version:** 1.0
