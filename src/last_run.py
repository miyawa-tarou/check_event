import json
from datetime import datetime
import os

class LastRunManager:
    def __init__(self, file_path='last_run.json'):
        self.file_path = file_path
        
    def get_last_run_time(self):
        if not os.path.exists(self.file_path):
            # 初回実行時は2025/4/12を返す
            return datetime(2025, 4, 12, 0, 0, 0)
            
        try:
            with open(self.file_path, 'r') as f:
                data = json.load(f)
                return datetime.fromisoformat(data['last_run'])
        except Exception as e:
            print(f"Error reading last run time: {e}")
            return datetime(2025, 4, 12, 0, 0, 0)
            
    def update_last_run_time(self):
        try:
            with open(self.file_path, 'w') as f:
                json.dump({
                    'last_run': datetime.now().isoformat()
                }, f)
        except Exception as e:
            print(f"Error updating last run time: {e}") 