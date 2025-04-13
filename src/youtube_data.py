from googleapiclient.discovery import build
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

class YouTubeDataCollector:
    def __init__(self):
        self.youtube = build('youtube', 'v3', developerKey=os.getenv('YOUTUBE_API_KEY'))
        
    def search_videos(self, since_date=None):
        if since_date is None:
            since_date = datetime(2025, 4, 12, 0, 0, 0)
            
        try:
            request = self.youtube.search().list(
                part="snippet",
                q="M3-2025春",
                type="video",
                publishedAfter=since_date.isoformat() + "Z",
                maxResults=50
            )
            
            response = request.execute()
            
            videos = []
            for item in response.get('items', []):
                video_info = {
                    'video_id': item['id']['videoId'],
                    'title': item['snippet']['title'],
                    'description': item['snippet']['description'],
                    'published_at': item['snippet']['publishedAt']
                }
                videos.append(video_info)
                
            return videos
            
        except Exception as e:
            print(f"Error searching YouTube videos: {e}")
            return [] 