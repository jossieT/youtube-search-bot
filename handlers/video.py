from aiogram import types
from services.youtube_api import get_video_details
import re

def extract_video_id(url):
    # Simple regex for YouTube video ID
    match = re.search(r'(?:v=|youtu.be/)([\w-]{11})', url)
    return match.group(1) if match else None

async def handle_video(message: types.Message):
    url = message.get_args()
    video_id = extract_video_id(url)
    if not video_id:
        await message.reply('Invalid YouTube URL.')
        return
    details = get_video_details(video_id)
    items = details.get('items', [])
    if not items:
        await message.reply('Video not found.')
        return
    info = items[0]
    snippet = info['snippet']
    stats = info['statistics']
    title = snippet['title']
    channel = snippet['channelTitle']
    published = snippet['publishedAt'][:10]
    views = stats.get('viewCount', 'N/A')
    likes = stats.get('likeCount', 'N/A')
    desc = snippet.get('description', '')
    if len(desc) > 300:
        desc = desc[:300] + '...'
    reply = f"🎥 <b>{title}</b>\n📺 Channel: {channel}\n👀 Views: {views} | 👍 Likes: {likes}\n📅 Published: {published}\n📝 Description: {desc}"
    await message.reply(reply, parse_mode='HTML')
