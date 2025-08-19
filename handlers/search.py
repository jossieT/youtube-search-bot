from aiogram import types
from services.youtube_api import search_youtube

async def handle_search(message: types.Message):
    query = message.get_args()
    if not query:
        await message.reply('Please provide a search keyword.')
        return
    results = search_youtube(query)
    items = results.get('items', [])
    if not items:
        await message.reply('No results found.')
        return
    reply = '🔍 Found results:\n\n'
    for item in items:
        kind = item['id']['kind']
        title = item['snippet']['title']
        url = ''
        if kind == 'youtube#video':
            url = f"https://youtu.be/{item['id']['videoId']}"
        elif kind == 'youtube#channel':
            url = f"https://youtube.com/channel/{item['id']['channelId']}"
        elif kind == 'youtube#playlist':
            url = f"https://youtube.com/playlist?list={item['id']['playlistId']}"
        reply += f"🎬 <a href='{url}'>{title}</a>\n"
    await message.reply(reply, parse_mode='HTML')
