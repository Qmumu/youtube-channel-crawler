import time,datetime
import requests,re
import requests
import pandas as pd
from typing import List, Dict
import json,csv
import functools
from typing import Callable, Any
from loguru import logger

def get_channel_seeds_csv(file='./youtube_seeds.csv') -> List[Dict]:
    """
    Returns:
        List[Dict[]]: 
        examples：
        [
            {
                'id': 8,
                'user_id': 'Shutterbug101',
                user_url': 'https://www.youtube.com/@Shutterbug101'
            },
            ...
        ]
    """
    df = pd.read_csv(file)
    data_array = df.to_dict('records')
    return data_array

def get_channel_detail_csv(file='./youtube_channel_data.csv') -> List[Dict]:
    df = pd.read_csv(file)
    data_array = df.to_dict('records')
    return data_array

def get_channel_id(url):
    html_text = requests.get(url).text
    channel_url = re.findall('href="https://www.youtube.com/channel/.*?"',html_text)[0]
    channel_url = channel_url.split('"')[-2]
    channel_id = channel_url.split("/")[-1]
    return channel_id

def build_search_query(keywords: str, limit: int = 2) -> str:
    """
    Extract N keywords from a keywords string to build a search query
    
    Args:
        keywords: String containing keywords
        limit: Number of keywords needed, default is 3
    
    Returns:
        Formatted search query string
    """
    
    # Handle cases with quotes
    if '"' in keywords:
        # Use regex to match phrases with quotes
        import re
        phrases = re.findall(r'\"([^\"]+)\"|(\S+)', keywords)
        # Extract matched phrases or words (remove empty values)
        terms = ['"' + match[0] + '"' if match[0] else match[1] 
                for match in phrases]
    else:
        # Simple space splitting
        terms = keywords.split()
    
    # Take first N keywords
    selected_terms = terms[:limit]
    
    # Combine into query string
    return ' '.join(selected_terms)
    

def save_to_json(data,filename="./youtube_data.json"):
    json_data = {
        "result":data
    }
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
    return True
def save_to_csv_seeds(data: Dict, filename: str = "youtube_seeds.csv"):
    """
    将YouTube频道数据保存到CSV文件
    
    Args:
        data: 包含频道信息和视频列表的字典
        filename: CSV文件名
    """
    try:
        # 准备CSV表头
        headers = [
           "channel_id","channel_url"
        ]
        
        with open(filename, 'a', newline='', encoding='utf-8') as f:                
            writer = csv.DictWriter(f, fieldnames=headers)
            if f.tell() == 0:
                writer.writeheader()
            writer.writerow(data)

        return True
    except Exception as e:
        print(f"保存CSV文件时出错: {str(e)}")
        return False
def save_to_csv(data: Dict, filename: str = "youtube_channel_data.csv"):
    """
    将YouTube频道数据保存到CSV文件
    
    Args:
        data: 包含频道信息和视频列表的字典
        filename: CSV文件名
    """
    try:
        # 准备CSV表头
        headers = [
            'title','channel_url','channel_id', 'publishedAt',
            'statistics',
            'head_pic', 'keywords',
            'videos'
        ]
        
        with open(filename, 'a', newline='', encoding='utf-8') as f:                
            writer = csv.DictWriter(f, fieldnames=headers)
            if f.tell() == 0:
                writer.writeheader()
            writer.writerow(data)
            
            
                
        return True
    except Exception as e:
        print(f"保存CSV文件时出错: {str(e)}")
        return False

def retry_with_backoff(
    max_retries: int = 3,      
    initial_delay: float = 3,   
    max_delay: float = 30,      
    backoff_factor: float = 2  
) -> Callable:
    """
    Retry decorator with exponential backoff
    
    Args:
        max_retries: Maximum number of retries
        initial_delay: Initial delay in seconds
        max_delay: Maximum delay in seconds
        backoff_factor: Multiply factor for delay increase
    
    Returns:
        Decorated function
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            delay = initial_delay
            last_exception = None
            
            for retry in range(max_retries + 1):  # +1 for initial attempt
                try:
                    return func(*args, **kwargs)
                
                except Exception as e:
                    last_exception = e
                    if retry == max_retries:  # If this was our last attempt
                        logger.error(
                            "Failed after {} retries | function: {} | error: {}", 
                            max_retries, func.__name__, str(e)
                        )
                        raise last_exception
                    
                    # Calculate next delay
                    delay = min(delay * backoff_factor, max_delay)
                    
                    logger.warning(
                        "Retry {}/{} after {} seconds | function: {} | error: {}", 
                        retry + 1, max_retries, delay, func.__name__, str(e)
                    )
                    
                    time.sleep(delay)
            
            raise last_exception  # Should never reach here
        
        return wrapper
    return decorator

if __name__ == '__main__':
    # a = get_channel_id("https://www.youtube.com/@phlearn")
    # # a = get_user_tasks()
    # print(a)
    # Test case 1: Simple space-separated keywords
    keywords1 = "Phlearn Photoshop Photography AaronNace Adobe Tutorials Lightroom"
    query1 = build_search_query(keywords1)
    print("Test 1:", query1)
    # Output: Phlearn Photoshop Photography

    # Test case 2: Keywords with quotes
    keywords2 = "photography \"photography tutorials\" \"travel photography\" \"travel photography tutorials\" \"adventure photography\" \"travel videography\" \"videography tutorials\""
    query2 = build_search_query(keywords2)
    print("Test 2:", query2)