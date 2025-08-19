
# 🎬 YouTube Search Telegram Bot

> **A modern Telegram bot to search YouTube videos, channels, and get detailed information — all inside Telegram!**

---

## 🚀 Features

- **/search <keyword>** — Instantly search YouTube for videos, channels, or playlists. Returns the top results with clickable titles, views, duration, and thumbnails.
- **/video <YouTube URL>** — Fetch detailed information about any YouTube video: title, channel, publish date, views, likes, and a summarized description.
- **/channel <Channel Name or URL>** — Get channel details: title, subscriber count, total videos, creation date, and latest uploads.
- **(Optional, Advanced)**
  - Download audio/video using yt-dlp
  - Fetch and summarize video transcripts with AI
  - Store user search history (SQLite/Supabase)

---

## 📦 Tech Stack

- **Python 3.8+**
- **[aiogram](https://docs.aiogram.dev/)** — Fast Telegram bot framework
- **[YouTube Data API v3](https://developers.google.com/youtube/v3)** — Official YouTube API
- **yt-dlp** — For optional downloads
- **SQLite/Supabase** — (Optional) For storing user history

---

## 🛠️ Setup & Installation

1. **Clone the repository:**
	```sh
	git clone https://github.com/jossieT/youtube-search-bot.git
	cd youtube-search-bot
	```
2. **Install dependencies:**
	```sh
	pip install -r requirements.txt
	```
3. **Configure API keys:**
	- Copy `config.example.py` to `config.py` and fill in your credentials:
	  - `TELEGRAM_TOKEN` — Your Telegram Bot token
	  - `YOUTUBE_API_KEY` — Your YouTube Data API v3 key
4. **Run the bot:**
	```sh
	python bot.py
	```

---

## 💡 Usage Examples

**Search YouTube:**
```
/search stand up comedy
```
_Bot replies with top 3–5 results, each with a clickable title, views, and duration._

**Get video info:**
```
/video https://youtu.be/xxxx
```
_Bot replies with title, channel, publish date, views, likes, and a short description._

**Get channel info:**
```
/channel Comedy Central
```
_Bot replies with channel title, subscribers, total videos, creation date, and latest uploads._

---

## 📁 Project Structure

```
youtube-search-bot/
│── bot.py                # Main entry point
│── config.py             # API keys, tokens (not committed)
│── requirements.txt      # Dependencies
│── README.md             # Documentation
│── services/
│    ├── youtube_api.py   # YouTube API wrapper functions
│    ├── yt_dlp_helper.py # Optional video/audio extraction
│── handlers/
│    ├── search.py        # Handles /search command
│    ├── video.py         # Handles /video command
│    ├── channel.py       # Handles /channel command
```

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

---

## 📝 License

MIT License. See [LICENSE](LICENSE) for details.
