import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

class GeminiAnalyzer:
    def __init__(self):
        genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
        self.model = genai.GenerativeModel('gemini-2.0-flash')
        
    def analyze_tweets(self, tweets):
        prompt = """
        以下のツイートから、「M3-2025春」における新譜の情報であるものを抽出してください。
        新譜情報の特徴：
        - 新作アルバムやシングルの発売告知
        - 新譜の試聴動画（XFD）の公開
        - 新譜の特設サイトの開設
        - 新譜のお品書きの公開
        - M3-2024秋など過去の作品は除外してください。
        
        出力形式：
        - 各ツイートを箇条書きでリスト化
        - ツイート内のURLはMarkdownリンク形式に変換
        - 重要な情報は太字（**）で強調
        
        ツイート:
        """
        
        try:
            response = self.model.generate_content(prompt + "\n".join(tweets))
            return response.text
            
        except Exception as e:
            print(f"Error analyzing tweets with Gemini: {e}")
            return "" 