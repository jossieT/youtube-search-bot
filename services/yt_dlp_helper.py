
import yt_dlp
import os
import re
from urllib.parse import urlparse

def is_valid_youtube_url(url):
    # Basic check for YouTube URL
    parsed = urlparse(url)
    return 'youtube.com' in parsed.netloc or 'youtu.be' in parsed.netloc

def download_youtube(url, user_id, timestamp, audio_only=False, progress_hook=None):
    if not is_valid_youtube_url(url):
        raise ValueError('Invalid YouTube URL')
    ext = 'mp3' if audio_only else 'mp4'
    out_dir = 'downloads'
    os.makedirs(out_dir, exist_ok=True)
    filename = f"{user_id}_{timestamp}.{ext}"
    filepath = os.path.join(out_dir, filename)
    ydl_opts = {
        'outtmpl': filepath,
        'format': 'bestaudio/best' if audio_only else 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4',
        'merge_output_format': ext,
        'quiet': True,
        'noplaylist': True,
    }
    if audio_only:
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]
    if progress_hook:
        ydl_opts['progress_hooks'] = [progress_hook]
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
    return {'filepath': filepath, 'webpath': filepath}
