import requests
from googleapiclient.discovery import build
from config import YOUTUBE_API_KEY

youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

def search_youtube(query, max_results=3):
    # Search for videos, channels, playlists
    req = youtube.search().list(q=query, part='snippet', maxResults=max_results, type='video,channel,playlist')
    return req.execute()

def get_video_details(video_id):
    req = youtube.videos().list(part='snippet,statistics,contentDetails', id=video_id)
    return req.execute()

def get_channel_details(channel_id):
    req = youtube.channels().list(part='snippet,statistics,contentDetails', id=channel_id)
    return req.execute()

def get_channel_uploads(channel_id, max_results=3):
    # Get uploads playlist ID
    channel = get_channel_details(channel_id)
    uploads_playlist = channel['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    req = youtube.playlistItems().list(playlistId=uploads_playlist, part='snippet', maxResults=max_results)
    return req.execute()
