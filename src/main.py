from x_data import XDataCollector
from youtube_data import YouTubeDataCollector
from gemini_analyzer import GeminiAnalyzer
from last_run import LastRunManager
import json
from datetime import datetime
import os

def ensure_results_dir():
    """resultsディレクトリが存在しない場合は作成する"""
    if not os.path.exists('results'):
        os.makedirs('results')

def save_to_file(data, filename_prefix):
    # resultsディレクトリの存在を確認
    ensure_results_dir()
    
    # 日時を含むファイル名を生成
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"results/{filename_prefix}_{timestamp}.json"
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return filename

def save_markdown(content, filename_prefix):
    """Markdownファイルを保存する"""
    ensure_results_dir()
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"results/{filename_prefix}_{timestamp}.md"
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    return filename

def generate_youtube_markdown(videos):
    """YouTubeの動画情報をMarkdown形式に変換"""
    markdown = "# YouTube検索結果\n\n"
    
    for video in videos:
        video_id = video.get('video_id', '')
        title = video.get('title', '')
        description = video.get('description', '')
        published_at = video.get('published_at', '')
        
        markdown += f"## [{title}](https://www.youtube.com/watch?v={video_id})\n\n"
        markdown += f"- 公開日: {published_at}\n"
        markdown += f"- 説明: {description}\n\n"
    
    return markdown

def load_from_file(filename):
    """指定されたファイルからデータを読み込む"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"ファイルの読み込み中にエラーが発生しました: {e}")
        return None

def main():
    # 前回実行時の日時を取得
    last_run_manager = LastRunManager()
    
    # Xのデータ取得
    try:
        x_since_date = last_run_manager.get_last_run_time('x')
        x_collector = XDataCollector()
        tweets = x_collector.search_tweets(x_since_date)
        if not tweets:  # 空配列の場合
            print("Xのデータ取得に失敗しました。処理をスキップします。")
        else:
            x_filename = save_to_file(tweets, 'x_results')
            print(f"Xの検索結果を保存しました: {x_filename}")
            
            # Geminiによる分析（Xの取得成功時のみ実行）
            try:
                analyzer = GeminiAnalyzer()
                analysis_results = analyzer.analyze_tweets(tweets)
                if not analysis_results:  # 空文字列の場合
                    print("Geminiによる分析に失敗しました。処理をスキップします。")
                else:
                    # 分析結果の保存（Markdown形式）
                    analysis_md = f"# M3新譜情報分析結果\n\n"
                    analysis_md += "## 分析結果\n\n"
                    analysis_md += f"{analysis_results}\n\n"
                    analysis_md += "## 参照元の投稿\n\n"
                    for tweet in tweets:
                        username = tweet.get('username', '不明')
                        tweet_url = f"https://x.com/{username}/status/{tweet.get('id', '')}"
                        analysis_md += f"- [{username}]({tweet_url})\n"
                    analysis_filename = save_markdown(analysis_md, 'analysis_results')
                    print(f"分析結果を保存しました: {analysis_filename}")
                    # Geminiの分析が成功した場合のみXの最終実行時刻を更新
                    last_run_manager.update_last_run_time('x')
            except Exception as e:
                print(f"Geminiによる分析中にエラーが発生しました: {e}")
    except Exception as e:
        print(f"Xのデータ取得中にエラーが発生しました: {e}")
    
    # YouTubeのデータ取得
    try:
        youtube_since_date = last_run_manager.get_last_run_time('youtube')
        youtube_collector = YouTubeDataCollector()
        videos = youtube_collector.search_videos(youtube_since_date)
        if not videos:  # 空配列の場合
            print("YouTubeのデータ取得に失敗しました。処理をスキップします。")
        else:
            youtube_json_filename = save_to_file(videos, 'youtube_results')
            print(f"YouTubeの検索結果（JSON）を保存しました: {youtube_json_filename}")
            
            # YouTubeのMarkdown生成
            youtube_markdown = generate_youtube_markdown(videos)
            youtube_md_filename = save_markdown(youtube_markdown, 'youtube_results')
            print(f"YouTubeの検索結果（Markdown）を保存しました: {youtube_md_filename}")
            last_run_manager.update_last_run_time('youtube')
    except Exception as e:
        print(f"YouTubeのデータ取得中にエラーが発生しました: {e}")

if __name__ == "__main__":
    main() 