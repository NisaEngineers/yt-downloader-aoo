import os
import streamlit as st
from yt_dlp import YoutubeDL

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def download_video(url: str):
    ydl_opts = {
        "format": "bestvideo[height<=360]+bestaudio",
        "outtmpl": os.path.join(DOWNLOAD_DIR, "%(title)s.%(ext)s"),
        "quiet": True,
        "merge_output_format": "mp4",
        "postprocessors": [
            {
                "key": "FFmpegVideoConvertor",
                "preferedformat": "mp4"
            }
        ],
        "postprocessor_args": [
            "-c:v", "libx264",
            "-c:a", "aac",
            "-b:a", "192k"
        ]
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def download_audio(url: str):
    ydl_opts = {
        "format": "bestaudio",
        "outtmpl": os.path.join(DOWNLOAD_DIR, "%(title)s.%(ext)s"),
        "quiet": True,
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "0",
        }],
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

# --- Streamlit UI ---
st.set_page_config(page_title="YouTube Downloader", page_icon="🎵", layout="centered")

st.title("🎬 YouTube Downloader")
st.write("Download YouTube videos as **MP4 (360p)** or audio as **MP3 (best quality)**.")

url = st.text_input("Enter YouTube URL:")

choice = st.radio("Choose format:", ["MP4 (video)", "MP3 (audio)"])

if st.button("Download"):
    if url.strip():
        with st.spinner("Downloading... please wait"):
            try:
                if choice.startswith("MP4"):
                    download_video(url)
                    st.success("✅ Video downloaded successfully!")
                else:
                    download_audio(url)
                    st.success("✅ Audio downloaded successfully!")
            except Exception as e:
                st.error(f"❌ Error: {e}")
    else:
        st.warning("Please enter a valid YouTube URL.")
