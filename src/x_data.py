import tweepy
import os
from datetime import datetime
from dotenv import load_dotenv
import time

load_dotenv()

class XDataCollector:
    def __init__(self):
        # OAuth 2.0認証を使用
        self.client = tweepy.Client(
            bearer_token=os.getenv('X_BEARER_TOKEN'),
            consumer_key=os.getenv('X_CLIENT_ID'),
            consumer_secret=os.getenv('X_CLIENT_SECRET'),
            access_token=os.getenv('X_ACCESS_TOKEN'),
            access_token_secret=os.getenv('X_ACCESS_TOKEN_SECRET')
        )
        
    def search_tweets(self, since_date=None):
        if since_date is None:
            since_date = datetime(2025, 4, 12, 0, 0, 0)
            
        # 検索クエリを修正（リツイートを除外）
        query = '(#M3春2025 OR (M3 新譜) OR (M3 新作) OR (M3 特設) OR (M3 XFD) OR (M3 告知) OR (M3 お品書き)) -is:retweet'
        
        try:
            # V2のsearch_recent_tweetsメソッドを使用
            tweets = self.client.search_recent_tweets(
                query=query,
                start_time=since_date,
                tweet_fields=['created_at', 'text', 'author_id'],
                max_results=100,
                sort_order='recency'
            )
            
            if tweets and tweets.data:
                return [tweet.text for tweet in tweets.data]
            return []
            
        except tweepy.TooManyRequests as e:
            print(f"レート制限に達しました。 {e}")
            return []
            
        except tweepy.TweepyException as e:
            print(f"X APIエラー: {e}")
            return []
            
        except Exception as e:
            print(f"予期せぬエラー: {e}")
            return [] 