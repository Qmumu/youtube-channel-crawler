# YouTube Channel Crawler

A Python-based tool for discovering and analyzing similar YouTube channels based on seed channels. This project helps content creators and researchers find channels with similar content types and gather their metadata and video information.

## Features

- **Channel Discovery**: Find similar channels based on:
  - Channel keywords
  - Content type
  - Channel relationships
- **Data Collection**:
  - Channel metadata (subscribers, views, etc.)
  - Video information
  - Channel statistics
- **Batch Processing**:
  - Process multiple seed channels
  - Automatic data expansion
  - Error handling and retry mechanism

## Crawling Methods

This project utilizes two different approaches to fetch YouTube data:

### 1. Official YouTube Data API (`pyyoutube`)
- Uses official YouTube Data API
- Requires API key authentication
- Features:
  - Higher reliability and stability
  - Official API quota limits
  - Each IP can use up to 3 API keys
  - Used for detailed channel information and statistics

### 2. Unofficial API (`youtubesearchpython`)
- No API key required
- Requires proxy pool for reliable access
- Features:
  - No quota limitations
  - Requires proper proxy rotation
  - Used for channel search and discovery
  - Better for bulk data collection

### Implementation Strategy
- Channel Details: Uses official API for accurate statistics
- Channel Discovery: Uses unofficial API with proxy pool
- Hybrid approach maximizes data collection efficiency while maintaining reliability

## Channel Discovery Strategy

### Discovery Methods

1. **Channel Name Search**
- Directly search using seed channel's name
- Advantages:
  - Strong correlation with original channel
  - High relevance in most cases
- Limitations:
  - May deviate due to ambiguous channel names
  - Can return unrelated channels with similar names

2. **Keywords-based Search**
- Use channel's keyword metadata
- Helps validate and filter search results
- More accurate content type matching
- Reduces false positives from name-only search

### Search Logic Flow
Seed Channel
│
├── Channel Name Search
│ └── Get strongly related channels
│
├── Keywords Search
│ └── Get content-type related channels
│
└── Results Processing
├── Remove duplicates
├── Validate relevance
└── Store valid channels


### Benefits of Hybrid Approach
1. **Higher Accuracy**
   - Reduces false positives from name-only matching
   - Ensures content type relevance

2. **Better Coverage**
   - Captures related channels that might not share name patterns
   - Finds channels in the same content niche

3. **Quality Control**
   - Keywords act as a validation layer
   - Helps maintain dataset coherence

## Installation

1. Clone the repository
```bash
git clone [repository-url]
cd youtube-channel-crawler
```

2. Create and activate virtual environment
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

## Configuration

### 1. YouTube API Setup
```env
# .env file
YOUTUBE_API_KEY_1=your_first_api_key
YOUTUBE_API_KEY_2=your_second_api_key
YOUTUBE_API_KEY_3=your_third_api_key
```

### 2. Proxy Configuration
```python
# Configure proxy pool
proxy = {
    "http": "http://your_proxy_ip:port",
    "https": "http://your_proxy_ip:port"
}
```

### 3. Prepare seed channels in `youtube_seeds.csv`:
```csv
channel_id,channel_url
@example,https://youtube.com/@example
```

## Usage

1. Collect channel information:
```python
python youtube_main.py --mode channel_detail
```

2. Find related channels:
```python
python youtube_main.py --mode related_channel
```

## Data Structure

### Channel Information
```json
{
    "title": "Channel Name",
    "channel_id": "@channel",
    "publishedAt": "2024-01-20T00:00:00Z",
    "statistics": {
        "viewCount": "1000000",
        "subscriberCount": "10000",
        "videoCount": "100"
    },
    "keywords": "keyword1 keyword2 keyword3",
    "channel_url": "https://youtube.com/@channel"
}
```

## Project Structure
youtube-channel-crawler/
├── youtube/
│ ├── api.py # YouTube API interactions
│ ├── handler.py # Data processing logic
│ └── youtube_main.py # Main execution file
├── utils/
│ └── utils.py # Utility functions
├── data/
│ ├── youtube_seeds.csv # Seed channel data
│ └── youtube_channel_data.csv # Processed channel data
├── requirements.txt
└── README.md


## Rate Limiting and Quotas

### Official API (pyyoutube)
- Daily quota limits apply
- Automatic key rotation among 3 API keys
- Built-in retry mechanism with exponential backoff

### Unofficial API (youtubesearchpython)
- No quota limits
- Requires proper proxy rotation
- Rate limiting handled through proxy pool
- Error handling for failed requests

## Dependencies

- pyyoutube
- pandas
- loguru
- python-dotenv
- requests
- youtubesearchpython

