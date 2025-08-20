from aiogram import types
from services.yt_dlp_helper import download_youtube
import os
import time

TELEGRAM_LIMIT = 50 * 1024 * 1024  # 50 MB
DOWNLOADS_DIR = 'downloads'

async def handle_download(message: types.Message):
    import asyncio
    args = message.get_args().split()
    if not args:
        await message.reply('❌ Please provide a YouTube URL.')
        return
    url = args[0]
    audio_only = len(args) > 1 and args[1].lower() == 'audio'
    user_id = message.from_user.id
    timestamp = int(time.time())
    status_msg = await message.reply('⏳ Downloading {}...'.format('audio' if audio_only else 'video'))
    progress = {'last_percent': 0}


    async def progress_hook_coro(percent=None, finished=False):
        try:
            if finished:
                await status_msg.edit_text("✅ Download finished. Preparing file...")
            elif percent is not None:
                await status_msg.edit_text(f"⏳ Downloading... {percent}%")
        except Exception:
            pass

    def sync_progress_hook(d):
        if d['status'] == 'downloading':
            percent = int(float(d.get('downloaded_bytes', 0)) / float(d.get('total_bytes', 1)) * 100) if d.get('total_bytes') else 0
            if percent - progress['last_percent'] >= 5:
                progress['last_percent'] = percent
                import asyncio
                asyncio.create_task(progress_hook_coro(percent=percent))
        elif d['status'] == 'finished':
            import asyncio
            asyncio.create_task(progress_hook_coro(finished=True))

    try:
        result = download_youtube(url, user_id, timestamp, audio_only, progress_hook=sync_progress_hook)
    except ValueError:
        await status_msg.edit_text('❌ Invalid YouTube URL. Please try again.')
        return
    except Exception:
        await status_msg.edit_text('⚠️ Could not download the video. Try another link.')
        return
    if not result or not os.path.exists(result['filepath']):
        await status_msg.edit_text('⚠️ Could not download the video. Try another link.')
        return
    file_size = os.path.getsize(result['filepath'])
    if file_size > TELEGRAM_LIMIT:
        await status_msg.edit_text(f"⚠️ File is too large to send via Telegram. Here is a direct link: {result['webpath']}")
        os.remove(result['filepath'])
        return
    with open(result['filepath'], 'rb') as f:
        if audio_only:
            await status_msg.edit_text('✅ Here is your audio 🎵')
            await message.reply_document(f, caption='✅ Here is your audio 🎵')
        else:
            await status_msg.edit_text('✅ Here is your video 🎬')
            await message.reply_video(f, caption='✅ Here is your video 🎬')
    os.remove(result['filepath'])
