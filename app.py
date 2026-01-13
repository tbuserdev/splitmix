import streamlit as st
import os
import shutil
from io import BytesIO
import zipfile
from pathlib import Path
import json

from downloader import download_youtube
from main import split_wav_file
from pydub import AudioSegment


# Page configuration
st.set_page_config(page_title="SplitMix", page_icon="🎵", layout="centered")


def save_metadata(artist, album, title):
    """Save metadata to a JSON file for persistence."""
    metadata_path = os.path.join("data", "metadata.json")
    os.makedirs("data", exist_ok=True)

    metadata = {"artist": artist, "album": album, "title": title}

    with open(metadata_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)


def load_metadata():
    """Load metadata from JSON file."""
    metadata_path = os.path.join("data", "metadata.json")

    if os.path.exists(metadata_path):
        try:
            with open(metadata_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading metadata: {e}")

    return None


def restore_session_from_files():
    """Restore session state from existing files in data/ directory."""
    data_dir = "data"
    audio_path = os.path.join(data_dir, "input.wav")
    cover_path = os.path.join(data_dir, "cover.jpg")

    # Load metadata
    metadata = load_metadata()

    # Check if audio file exists
    if os.path.exists(audio_path):
        try:
            # Get audio duration
            audio = AudioSegment.from_file(audio_path)
            duration_seconds = len(audio) // 1000
            hours = duration_seconds // 3600
            minutes = (duration_seconds % 3600) // 60
            seconds = duration_seconds % 60

            if hours > 0:
                duration = f"{hours}:{minutes:02d}:{seconds:02d}"
            else:
                duration = f"{minutes}:{seconds:02d}"

            # Restore metadata if available
            if metadata:
                st.session_state.artist = metadata.get("artist", "")
                st.session_state.album = metadata.get("album", "")
                title = metadata.get("title", "Downloaded Audio")
            else:
                title = "Downloaded Audio"

            # Restore video info
            st.session_state.video_info = {
                "title": title,
                "audio_path": audio_path,
                "cover_path": cover_path if os.path.exists(cover_path) else None,
                "duration": duration,
            }
            st.session_state.downloaded = True

        except Exception as e:
            print(f"Error restoring audio: {e}")

    # Check for output tracks
    output_dirs = [
        os.path.join(data_dir, "output_tracks"),
        # Check for any other directories in data/
    ]

    for output_dir in output_dirs:
        if os.path.exists(output_dir):
            mp3_files = sorted(list(Path(output_dir).glob("*.mp3")))
            if mp3_files:
                st.session_state.output_files = [str(f) for f in mp3_files]
                st.session_state.processing_complete = True
                break


# Initialize session state
if "downloaded" not in st.session_state:
    st.session_state.downloaded = False
if "video_info" not in st.session_state:
    st.session_state.video_info = None
if "processing_complete" not in st.session_state:
    st.session_state.processing_complete = False
if "output_files" not in st.session_state:
    st.session_state.output_files = []
if "artist" not in st.session_state:
    st.session_state.artist = ""
if "album" not in st.session_state:
    st.session_state.album = ""
if "session_restored" not in st.session_state:
    st.session_state.session_restored = False

# Restore session from existing files (only once per session)
if not st.session_state.session_restored:
    restore_session_from_files()
    st.session_state.session_restored = True


# Title and description
st.title("🎵 SplitMix")
st.markdown("Download and split YouTube audio into tagged tracks")

st.divider()

# YouTube URL input
st.subheader("1. Download Audio")
youtube_url = st.text_input(
    "YouTube URL",
    placeholder="https://youtube.com/watch?v=...",
    help="Paste the URL of the YouTube video you want to download",
)

if st.button("Download Audio & Thumbnail", type="primary", disabled=not youtube_url):
    with st.spinner("Downloading from YouTube..."):
        try:
            # Download the video
            info = download_youtube(youtube_url, output_dir="data")
            st.session_state.video_info = info
            st.session_state.downloaded = True
            st.session_state.processing_complete = False

            # Auto-fill artist and album from video title
            st.session_state.artist = info["title"]
            st.session_state.album = info["title"]

            # Save metadata for persistence
            save_metadata(info["title"], info["title"], info["title"])

        except Exception as e:
            st.error(f"Error downloading video: {str(e)}")
            st.session_state.downloaded = False

# Show download status if already downloaded
if st.session_state.downloaded and st.session_state.video_info:
    st.success(f'✓ Downloaded: "{st.session_state.video_info["title"]}"')
    st.info(
        f"✓ Audio: {os.path.basename(st.session_state.video_info['audio_path'])} ({st.session_state.video_info['duration']})"
    )
    if st.session_state.video_info["cover_path"]:
        st.info(
            f"✓ Cover: {os.path.basename(st.session_state.video_info['cover_path'])}"
        )

    # Cover image preview and upload section
    st.markdown("### Cover Art")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("**Downloaded Cover**")
        if st.session_state.video_info.get("cover_path") and os.path.exists(
            st.session_state.video_info["cover_path"]
        ):
            st.image(
                st.session_state.video_info["cover_path"],
                width=300,
                caption="YouTube Thumbnail",
            )
        else:
            st.info("No cover downloaded")

    with col2:
        st.markdown("**Upload Custom Cover**")
        uploaded_cover = st.file_uploader(
            "Upload your own cover image",
            type=["jpg", "jpeg", "png", "webp"],
            help="Upload a custom cover image to use instead of the YouTube thumbnail",
        )

        if uploaded_cover is not None:
            # Save uploaded cover
            custom_cover_path = os.path.join("data", "custom_cover.jpg")
            with open(custom_cover_path, "wb") as f:
                f.write(uploaded_cover.getbuffer())

            # Update session state to use custom cover
            st.session_state.video_info["cover_path"] = custom_cover_path

            # Show preview
            st.image(custom_cover_path, width=300, caption="Custom Cover")
            st.success("✓ Custom cover uploaded!")

st.divider()

# Metadata input
st.subheader("2. Enter Metadata")

col1, col2 = st.columns(2)
with col1:
    artist = st.text_input(
        "Artist", value=st.session_state.artist, help="Artist name for the metadata"
    )
with col2:
    album = st.text_input(
        "Album", value=st.session_state.album, help="Album name for the metadata"
    )

# Update session state and save metadata
if artist != st.session_state.artist or album != st.session_state.album:
    st.session_state.artist = artist
    st.session_state.album = album
    # Save metadata if we have video info
    if st.session_state.video_info:
        save_metadata(artist, album, st.session_state.video_info.get("title", ""))

st.divider()

# Timestamps input
st.subheader("3. Enter Timestamps")
timestamps = st.text_area(
    "Timestamps",
    height=200,
    placeholder="""00:00 - Track 1
03:24 - Track 2
07:15 - Track 3""",
    help="Enter timestamps in MM:SS or HH:MM:SS format, followed by ' - ' and the track name",
)

# Output folder name
output_folder = st.text_input(
    "Output Folder Name",
    value="output_tracks",
    help="Name of the folder where tracks will be saved",
)

st.divider()

# Split tracks button
st.subheader("4. Split Tracks")

can_split = st.session_state.downloaded and artist and album and timestamps

if st.button("Split Tracks", type="primary", disabled=not can_split):
    if not st.session_state.video_info:
        st.error("Please download audio first")
    else:
        # Create progress bar
        progress_bar = st.progress(0)
        status_text = st.empty()

        def progress_callback(current, total, track_name):
            progress = current / total
            progress_bar.progress(progress)
            status_text.text(f"Exporting {current}/{total}: {track_name}")

        try:
            # Split the audio file
            audio_path = st.session_state.video_info["audio_path"]
            cover_path = st.session_state.video_info.get("cover_path")

            output_dir = os.path.join("data", output_folder)

            created_files = split_wav_file(
                source_file=audio_path,
                tracklist_str=timestamps,
                artist_name=artist,
                album_name=album,
                output_dir=output_dir,
                cover_art_path=cover_path,
                progress_callback=progress_callback,
            )

            st.session_state.output_files = created_files
            st.session_state.processing_complete = True

            progress_bar.progress(1.0)
            status_text.empty()

        except Exception as e:
            st.error(f"Error splitting tracks: {str(e)}")
            st.session_state.processing_complete = False

# Show completion status
if st.session_state.processing_complete and st.session_state.output_files:
    st.success(f"✓ Complete! {len(st.session_state.output_files)} tracks created")

    st.divider()

    # Download and cleanup section
    st.subheader("5. Download & Cleanup")

    col1, col2 = st.columns(2)

    with col1:
        # Create ZIP file for download
        def create_zip():
            zip_buffer = BytesIO()
            with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
                for file_path in st.session_state.output_files:
                    if os.path.exists(file_path):
                        zip_file.write(file_path, os.path.basename(file_path))
            zip_buffer.seek(0)
            return zip_buffer

        if st.session_state.output_files:
            zip_data = create_zip()
            st.download_button(
                label="Download All (ZIP)",
                data=zip_data,
                file_name=f"{album.replace(' ', '_')}_tracks.zip",
                mime="application/zip",
                type="primary",
            )

    with col2:
        # Delete all files button
        if st.button("Delete All Files", type="secondary"):
            try:
                # Delete the data directory
                if os.path.exists("data"):
                    shutil.rmtree("data")

                # Reset session state
                st.session_state.downloaded = False
                st.session_state.video_info = None
                st.session_state.processing_complete = False
                st.session_state.output_files = []

                st.success("✓ All files deleted successfully")
                st.rerun()

            except Exception as e:
                st.error(f"Error deleting files: {str(e)}")

# Footer
st.divider()
st.markdown(
    """
    <div style='text-align: center; color: #666; padding: 20px;'>
    Made with Streamlit • Powered by yt-dlp & pydub
    </div>
    """,
    unsafe_allow_html=True,
)
