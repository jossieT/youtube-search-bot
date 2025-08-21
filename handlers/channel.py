from aiogram import types
from services.youtube_api import get_channel_details, search_youtube, get_channel_uploads
import re

def extract_channel_id(url_or_name):
    # Try to extract channel ID from URL
    match = re.search(r'(?:channel/)([\w-]+)', url_or_name)
    if match:
        return match.group(1)
    # Otherwise, search by name
    results = search_youtube(url_or_name, max_results=1)
    items = results.get('items', [])
    for item in items:
        if item['id']['kind'] == 'youtube#channel':
            return item['id']['channelId']
    return None

def format_number(n):
    try:
        return f"{int(n):,}"
    except Exception:
        return n

async def handle_channel(message: types.Message):
    arg = message.get_args()
    if not arg:
        await message.reply("❌ Please provide a channel name or URL.\nExample: <code>/channel Comedy Central</code>", parse_mode='HTML')
        return

    channel_id = extract_channel_id(arg)
    if not channel_id:
        await message.reply('❌ Channel not found. Please try a different name or provide a valid channel URL.')
        return

    details = get_channel_details(channel_id)
    items = details.get('items', [])
    if not items:
        await message.reply('❌ Channel not found. Please try a different name or provide a valid channel URL.')
        return

    info = items[0]
    snippet = info['snippet']
    stats = info['statistics']
    title = snippet['title']
    subs = format_number(stats.get('subscriberCount', 'N/A'))
    videos = format_number(stats.get('videoCount', 'N/A'))
    created = snippet['publishedAt'][:4]
    description = snippet.get('description', '')
    description_short = (description[:150] + '...') if len(description) > 150 else description
    channel_url = f"https://www.youtube.com/channel/{channel_id}"
    thumbnail_url = snippet.get('thumbnails', {}).get('high', {}).get('url')

    reply = (
        f"📺 <b><a href='{channel_url}'>{title}</a></b>\n"
        f"👥 Subscribers: {subs}\n"
        f"🎞 Total Videos: {videos}\n"
        f"📅 Created: {created}\n"
    )
    if description_short:
        reply += f"📝 <i>{description_short}</i>\n"

    # Latest uploads
    uploads = get_channel_uploads(channel_id)
    upload_items = uploads.get('items', [])
    if upload_items:
        reply += '🔔 <b>Latest Uploads:</b>\n'
        for item in upload_items[:3]:
            video_title = item['snippet']['title']
            video_id = item['snippet']['resourceId']['videoId']
            video_url = f"https://youtu.be/{video_id}"
            reply += f"• <a href='{video_url}'>{video_title}</a>\n"

    if thumbnail_url:
        await message.bot.send_photo(
            message.chat.id,
            photo=thumbnail_url,
            caption=reply,
            parse_mode='HTML'
        )
    else:
        await message.reply(reply, parse_mode='HTML', disable_web_page_preview=True)
