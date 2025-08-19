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

async def handle_channel(message: types.Message):
    arg = message.get_args()
    channel_id = extract_channel_id(arg)
    if not channel_id:
        await message.reply('Channel not found.')
        return
    details = get_channel_details(channel_id)
    items = details.get('items', [])
    if not items:
        await message.reply('Channel not found.')
        return
    info = items[0]
    snippet = info['snippet']
    stats = info['statistics']
    title = snippet['title']
    subs = stats.get('subscriberCount', 'N/A')
    videos = stats.get('videoCount', 'N/A')
    created = snippet['publishedAt'][:4]
    reply = f"📺 <b>{title}</b>\n👥 Subscribers: {subs}\n🎞 Total Videos: {videos}\n📅 Created: {created}\n"
    # Latest uploads
    uploads = get_channel_uploads(channel_id)
    upload_items = uploads.get('items', [])
    if upload_items:
        reply += '🔔 Latest Uploads:\n'
        for item in upload_items:
            reply += f"{item['snippet']['title']}\n"
    await message.reply(reply, parse_mode='HTML')
