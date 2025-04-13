import json
from datetime import datetime
import os

class LastRunManager:
    def __init__(self, file_path='last_run.json'):
        self.file_path = file_path
        
    def get_last_run_time(self, service):
        if not os.path.exists(self.file_path):
            # 初回実行時は2025/4/12を返す
            return datetime(2025, 4, 12, 0, 0, 0)
            
        try:
            with open(self.file_path, 'r') as f:
                data = json.load(f)
                if service in data:
                    return datetime.fromisoformat(data[service])
                return datetime(2025, 4, 12, 0, 0, 0)
        except Exception as e:
            print(f"Error reading last run time: {e}")
            return datetime(2025, 4, 12, 0, 0, 0)
            
    def update_last_run_time(self, service):
        try:
            data = {}
            if os.path.exists(self.file_path):
                with open(self.file_path, 'r') as f:
                    data = json.load(f)
            
            data[service] = datetime.now().isoformat()
            
            with open(self.file_path, 'w') as f:
                json.dump(data, f)
        except Exception as e:
            print(f"Error updating last run time: {e}") 