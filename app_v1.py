# yt_downloader.py
import os
from yt_dlp import YoutubeDL

def download_video(url: str, outdir: str = "downloads"):
    os.makedirs(outdir, exist_ok=True)
    ydl_opts = {
        "format": "bestvideo[height<=360]+bestaudio",
        "outtmpl": os.path.join(outdir, "%(title)s.%(ext)s"),
        "quiet": False,
        "merge_output_format": "mp4",
        "postprocessors": [
            {
                # Re-encode final file to MP4 with H.264 video + AAC audio
                "key": "FFmpegVideoConvertor",
                "preferedformat": "mp4"
            }
        ],
        # Force ffmpeg to use H.264 + AAC
        "postprocessor_args": [
            "-c:v", "libx264",
            "-c:a", "aac",
            "-b:a", "192k"
        ]
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def download_audio(url: str, outdir: str = "downloads"):
    os.makedirs(outdir, exist_ok=True)
    ydl_opts = {
        "format": "bestaudio",
        "outtmpl": os.path.join(outdir, "%(title)s.%(ext)s"),
        "quiet": False,
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "0",  # best quality
        }],
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

if __name__ == "__main__":
    url = input("Enter YouTube URL: ").strip()
    choice = input("Download as MP4 (video) or MP3 (audio)? ").strip().lower()

    if choice == "mp4":
        print("Downloading video at 360p with audio (H.264 + AAC)...")
        download_video(url)
    elif choice == "mp3":
        print("Downloading audio as MP3 (best quality)...")
        download_audio(url)
    else:
        print("Invalid choice. Please enter 'mp4' or 'mp3'.")
