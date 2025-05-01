import pandas as pd
import json
from loguru import logger

def csv_to_json_by_title(csv_file: str = "youtube_channel_data.csv", json_file: str = "youtube_data.json"):
    try:
        df = pd.read_csv(csv_file)
        df = df.fillna("")
        data = df.to_dict('records')
        
        # Save to JSON
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            
        logger.success("Converted {} unique channels to JSON", len(data))
        
    except Exception as e:
        logger.error("Failed to convert CSV to JSON: {}", str(e))

if __name__ == "__main__":
    csv_to_json_by_title()