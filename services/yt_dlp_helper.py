# Optional: yt-dlp helper for downloads
import yt_dlp

def download_video(url, audio_only=False):
    ydl_opts = {'format': 'bestaudio/best'} if audio_only else {'format': 'best'}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        return info
