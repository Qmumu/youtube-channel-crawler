import pandas as pd
from loguru import logger

def deduplicate_csv(input_file: str = "youtube_seeds.csv", output_file: str = "youtube_seeds_unique.csv"):
    """
    Remove duplicate rows from CSV file
    
    Args:
        input_file: Input CSV file path
        output_file: Output CSV file path for unique records
    """
    try:
        # Read CSV file
        df = pd.read_csv(input_file)
        
        # Record original count
        original_count = len(df)
        
        # Remove duplicates
        df_unique = df.drop_duplicates()
        
        # Record unique count
        unique_count = len(df_unique)
        
        # Save to new CSV file
        df_unique.to_csv(output_file, index=False)
        
        # Log results
        logger.success(
            "Deduplication completed | Original records: {} | Unique records: {} | Duplicates removed: {}", 
            original_count, 
            unique_count, 
            original_count - unique_count
        )
        
        return True
    except Exception as e:
        logger.error("Failed to deduplicate CSV | Error: {}", str(e))
        return False

if __name__ == "__main__":
    deduplicate_csv()

