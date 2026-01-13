# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2026-01-13

### Changed

- **Docker Build Optimization**: Migrated from `pip` to `uv` for 10-50x faster dependency installation.
- **Docker Layer Caching**: Implemented BuildKit cache mounts for `apt` and `uv` to speed up subsequent builds.
- **Production Readiness**: Added BuildKit syntax support and improved healthcheck using Python standard library.

## [1.0.0] - 2026-01-13

### Added

- **Streamlit Web Interface** (`app.py`)
  - Paste YouTube URL to download audio and thumbnail
  - Side-by-side cover art preview (downloaded vs custom upload)
  - Editable metadata fields (Artist, Album) with auto-fill from video title
  - Timestamp input with format validation
  - Real-time progress bar during track splitting
  - ZIP download for all generated MP3 files
  - One-click file cleanup

- **YouTube Downloader** (`downloader.py`)
  - Audio download via yt-dlp in WAV format
  - Automatic thumbnail extraction with fallback mechanism
  - Metadata extraction (title, uploader, thumbnail URL)

- **Docker Support**
  - Production-ready Dockerfile with FFmpeg
  - docker-compose.yml for easy deployment
  - GitHub Actions workflow for automated Docker image builds

- **Session Persistence**
  - File-based state persistence (survives page reloads)
  - Automatic session restoration from existing files
  - Metadata saved to `data/metadata.json`

- **Enhanced Core Splitting** (`main.py`)
  - Progress callback support for UI integration
  - Multi-format audio input support (WAV, MP3, M4A)
  - Returns list of generated files

### Changed

- Improved README with comprehensive documentation
- Added new dependencies: streamlit, yt-dlp, pydub, mutagen

## [0.1.0] - 2025-01-13

### Added

- Initial CLI tool for splitting audio files
- Timestamp-based track splitting
- ID3 metadata tagging (artist, album, title, track number)
- Cover art embedding in MP3 files
- Basic usage documentation

[1.1.0]: https://github.com/tbuserdev/splitmix/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/tbuserdev/splitmix/compare/v0.1.0...v1.0.0
[0.1.0]: https://github.com/tbuserdev/splitmix/releases/tag/v0.1.0
