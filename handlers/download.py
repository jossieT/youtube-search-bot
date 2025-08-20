from aiogram import types
from services.yt_dlp_helper import download_youtube
import os
import time

TELEGRAM_LIMIT = 50 * 1024 * 1024  # 50 MB
DOWNLOADS_DIR = 'downloads'

async def handle_download(message: types.Message):
    args = message.get_args().split()
    if not args:
        await message.reply('❌ Please provide a YouTube URL.')
        return
    url = args[0]
    audio_only = len(args) > 1 and args[1].lower() == 'audio'
    user_id = message.from_user.id
    timestamp = int(time.time())
    await message.reply('⏳ Downloading {}...'.format('audio' if audio_only else 'video'))
    try:
        result = download_youtube(url, user_id, timestamp, audio_only)
    except ValueError:
        await message.reply('❌ Invalid YouTube URL. Please try again.')
        return
    except Exception:
        await message.reply('⚠️ Could not download the video. Try another link.')
        return
    if not result or not os.path.exists(result['filepath']):
        await message.reply('⚠️ Could not download the video. Try another link.')
        return
    file_size = os.path.getsize(result['filepath'])
    if file_size > TELEGRAM_LIMIT:
        await message.reply(f"⚠️ File is too large to send via Telegram. Here is a direct link: {result['webpath']}")
        os.remove(result['filepath'])
        return
    with open(result['filepath'], 'rb') as f:
        if audio_only:
            await message.reply_document(f, caption='✅ Here is your audio 🎵')
        else:
            await message.reply_video(f, caption='✅ Here is your video 🎬')
    os.remove(result['filepath'])
