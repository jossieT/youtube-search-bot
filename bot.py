from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from config import TELEGRAM_TOKEN
from handlers import search, video, channel, download

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(bot)

# Register handlers
dp.register_message_handler(search.handle_search, commands=['search'])
dp.register_message_handler(video.handle_video, commands=['video'])
dp.register_message_handler(channel.handle_channel, commands=['channel'])
dp.register_message_handler(download.handle_download, commands=['download'])

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
