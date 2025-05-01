import pandas as pd
import json
import ast
from loguru import logger

def csv_to_json_by_title(csv_file: str = "youtube_channel_data.csv", json_file: str = "youtube_data.json"):
    # Read CSV and fill NaN with empty string
    df = pd.read_csv(csv_file)
    df = df.fillna("")
    
    # Process each row
    data_list = []
    for _, row in df.iterrows():
        try:
            # Convert JSON strings to objects using ast.literal_eval
            row['statistics'] = ast.literal_eval(row['statistics']) if row['statistics'] else {}
            row['videos'] = ast.literal_eval(row['videos']) if row['videos'] else []
            
            data_list.append(row.to_dict())
            
        except Exception as e:
            print(f"Error parsing row: {row['title']}")
            print(f"Error details: {str(e)}")
            row['videos'] = []
            data_list.append(row.to_dict())
    
    # Save to JSON file
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(data_list, f, ensure_ascii=False, indent=2)
    
    logger.success("Converted {} channels to JSON", len(data_list))

if __name__ == "__main__":
    csv_to_json_by_title()