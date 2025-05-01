# import feapder
import pyyoutube
from youtubesearchpython import *
import re,json,time
from  loguru import logger
from utils import  retry_with_backoff
class Api():
    API_KEYs = [
        'AIzaSyAKfY0kf6VkLg_XbmZaeCcPPwR9lpzKQeM',
        'AIzaSyDwQtpdrdsmuRsawPAAWYa6zZ21KaH39pY',
        "AIzaSyAmo0z7UkhU0BmKEDmK7LD4w1Mrsbu_miY"
    ]
    TOKENS_NUM = 0
    def get_client(self):
        key = self.API_KEYs[self.TOKENS_NUM]
        api = pyyoutube.Api(api_key=key)
        self.TOKENS_NUM += 1
        if (self.TOKENS_NUM == len(self.API_KEYs)):
            self.TOKENS_NUM = 0
        return api
    
    def get_channel_info(self,channel_id):
        """
    Fetch and process YouTube channel information
    
    Args:
        channel_id (str): The YouTube channel ID to fetch information for
        
    Returns:
        tuple: A tuple containing:
            - playlist_id (str): ID of the channel's uploads playlist
            - author_info (dict): Dictionary containing channel details:
                - title (str): Channel title
                - channel_id (str): Channel custom URL
                - publishedAt (str): Channel creation date
                - statistics (dict): Channel statistics including:
                    - viewCount (str): Total view count
                    - subscriberCount (str): Number of subscribers
                    - videoCount (str): Total number of videos
                - head_pic (str): URL of channel's profile picture
                - keywords (str): Channel keywords or empty string if none
    """
        channel_info = self.get_client().get_channel_info(channel_id=channel_id,return_json=True)
        channel_info = channel_info["items"][0]
        playlist_id = channel_info["contentDetails"]["relatedPlaylists"]["uploads"]
        snippet = channel_info["snippet"]
        title = snippet["title"]
        channel_id = snippet["customUrl"]
        publishedAt = snippet["publishedAt"]
        statistics = channel_info["statistics"]
        statistics.pop("hiddenSubscriberCount", None)
        head_pic = snippet["thumbnails"]["medium"]["url"]
        keywords = channel_info.get("brandingSettings", {}).get("channel", {}).get("keywords", "")
        author_info = {
            "title":title,
            "channel_id":channel_id,
            "publishedAt":publishedAt,
            "statistics":statistics,
            "head_pic":head_pic,
            "keywords":keywords
            
        }
        return playlist_id,author_info
    @retry_with_backoff()
    def search_channals(self,seach_query,limit_per_page=10, region = 'US',language='en',pages=2):
        '''Searches for channels in YouTube.

        Args:
            query (str): Sets the search query.
            limit (int, optional): Sets limit to the number of results. Defaults to 20.
            language (str, optional): Sets the result language. Defaults to 'en'.
            region (str, optional): Sets the result region. Defaults to 'US'.

        Examples:
            Calling `result` method gives the search result.

            >>> search = ChannelsSearch('Harry Styles', limit = 1)
            >>> print(search.result())
            {
                "result": [
                    {
                        "type": "channel",
                        "id": "UCZFWPqqPkFlNwIxcpsLOwew",
                        "title": "Harry Styles",
                        "thumbnails": [
                            {
                                "url": "https://yt3.ggpht.com/ytc/AAUvwnhR81ocC_KalYEk5ItnJcfMBqaiIpuM1B0lJyg4Rw=s88-c-k-c0x00ffffff-no-rj-mo",
                                "width": 88,
                                "height": 88
                            },
                            {
                                "url": "https://yt3.ggpht.com/ytc/AAUvwnhR81ocC_KalYEk5ItnJcfMBqaiIpuM1B0lJyg4Rw=s176-c-k-c0x00ffffff-no-rj-mo",
                                "width": 176,
                                "height": 176
                            }
                        ],
                        "videoCount": "7",
                        "descriptionSnippet": null,
                        "subscribers": "9.25M subscribers",
                        "link": "https://www.youtube.com/channel/UCZFWPqqPkFlNwIxcpsLOwew"
                    }
                ]
            }
        '''
        channels_info = ChannelsSearch(seach_query, limit = limit_per_page, region = region,language= language,timeout=10)
        channels_infos = channels_info.result()["result"]
        for _ in range(pages-1):
            channels_info.next()
            channels_infos += channels_info.result()["result"]
        return channels_infos
    @retry_with_backoff()
    def get_videos_playlist(self,playlist_id,limit=5):
        '''Fetches only videos in the given playlist from link.
        Returns None if playlist is unavailable.

        Args:
            playlistLink (str): link of the playlist on YouTube.
            

        Examples:
        [
            {
                "title":video["title"],
                "link":video["link"]
            }
        ]

            
        '''
        playlistVideos = Playlist.getVideos('https://www.youtube.com/playlist?list='+playlist_id,timeout=10)
        videos = []
        for video in playlistVideos["videos"]:
            video_info = {
                "title":video["title"],
                "link":video["link"]
            }
            videos.append(video_info)
        return videos[:min(limit, len(videos))]
    def get_videos_API(self,playlist_id):
        uploads_playlist_items = self.get_client().get_playlist_items(
        playlist_id=playlist_id, count=3, limit=3,return_json=True,page_token="")
        videos = []
        for item in uploads_playlist_items["items"]:
            title = item["snippet"]["title"]
            video_id = item["contentDetails"]["videoId"]
            video_dict = {
                "title":title,
                "link":"https://www.youtube.com/watch?v="+video_id
            }
            videos.append(video_dict)
            
        return videos
    def get_video_info(self,video_url):
        '''Fetches only information for the given video link or ID.
        Returns None if video is unavailable.

        Args:
            videoLink (str): link or ID of the video on YouTube.
            mode (int, optional): Sets the type of result. Defaults to ResultMode.dict.

        Examples:

            >>> video = Video.getInfo("E07s5ZYygMg")
            >>> print(video)
            {
                "id": "E07s5ZYygMg",
                "title": "Harry Styles - Watermelon Sugar (Official Video)",
                "viewCount": {
                    "text": "170389228"
                },
                "thumbnails": [
                    {
                        "url": "https://i.ytimg.com/vi/E07s5ZYygMg/hqdefault.jpg?sqp=-oaymwEiCKgBEF5IWvKriqkDFQgBFQAAAAAYASUAAMhCPQCAokN4AQ==&rs=AOn4CLCT6nkbmYf-zbqAFgzF0D9PUhtsOQ",
                        "width": 168,
                        "height": 94
                    },
                    {
                        "url": "https://i.ytimg.com/vi/E07s5ZYygMg/hqdefault.jpg?sqp=-oaymwEiCMQBEG5IWvKriqkDFQgBFQAAAAAYASUAAMhCPQCAokN4AQ==&rs=AOn4CLA-JdoctyNp4aaj9dVtR0c6l5RDVw",
                        "width": 196,
                        "height": 110
                    },
                    {
                        "url": "https://i.ytimg.com/vi/E07s5ZYygMg/hqdefault.jpg?sqp=-oaymwEjCPYBEIoBSFryq4qpAxUIARUAAAAAGAElAADIQj0AgKJDeAE=&rs=AOn4CLBquHs9OWY5Dy1nE_syglwKP6-pMw",
                        "width": 246,
                        "height": 138
                    },
                    {
                        "url": "https://i.ytimg.com/vi/E07s5ZYygMg/hqdefault.jpg?sqp=-oaymwEjCNACELwBSFryq4qpAxUIARUAAAAAGAElAADIQj0AgKJDeAE=&rs=AOn4CLDSjHwdHxt9aU8NTojucGLp4PurTA",
                        "width": 336,
                        "height": 188
                    },
                    {
                        "url": "https://i.ytimg.com/vi/E07s5ZYygMg/maxresdefault.jpg?v=5ebedc0c",
                        "width": 1920,
                        "height": 1080
                    }
                ],
                "description": "This video is dedicated to touching. Listen to Harry Styles\u2019 new album \u2018Fine Line\u2019 now: https://HStyles.lnk.to/FineLineAY   Follow Harry Styles: Facebook: https://HarryStyles.lnk.to/followFI Instagram: https://HarryStyles.lnk.to/followII Twitter: https://HarryStyles.lnk.to/followTI Website: https://HarryStyles.lnk.to/followWI Spotify: https://HarryStyles.lnk.to/followSI YouTube: https://HarryStyles.lnk.to/subscribeYD  Lyrics:   Tastes like strawberries On a summer evening And it sounds just like a song I want more berries And that summer feeling It\u2019s so wonderful and warm Breathe me in Breathe me out I don\u2019t know if I could ever go without I\u2019m just thinking out loud I don\u2019t know if I could ever go without   Watermelon sugar high Watermelon sugar high Watermelon sugar high Watermelon sugar high Watermelon sugar   Strawberries On a summer evening Baby, you\u2019re the end of June I want your belly And that summer feeling Getting washed away in you Breathe me in Breathe me out I don\u2019t know if I could ever go without   Watermelon sugar high   I just wanna taste it I just wanna taste it Watermelon sugar high   Tastes like strawberries On a summer evening And it sounds just like a song I want your belly And that summer feeling I don\u2019t know if I could ever go without   Watermelon sugar high   I just wanna taste it I just wanna taste it Watermelon sugar high I just wanna taste it I just wanna taste it Watermelon sugar high   Watermelon Sugar  #HarryStyles #WatermelonSugar #FineLine",
                "channel": {
                    "name": "HarryStylesVEVO",
                    "id": "UCbOCbp5gXL8jigIBZLqMPrw",
                    "link": "https://www.youtube.com/channel/UCbOCbp5gXL8jigIBZLqMPrw"
                },
                "averageRating": 4.9043722,
                "keywords": [
                    "Fine Line",
                    "Harry Styles Fine Line",

                ],
                "publishDate": "2020-05-18",
                "uploadDate": "2020-05-18",
                "link": "https://www.youtube.com/watch?v=E07s5ZYygMg",
            }
        '''
        videoInfo = Video.getInfo(video_url, mode = ResultMode.json)
        return videoInfo
    

if __name__ == '__main__':
    # a = Api().get_channel_info("UC47XN5bhLTBH5TRFyKaUpKg")
    b = Api().get_videos_API("UU47XN5bhLTBH5TRFyKaUpKg")
    print(json.dumps(b,ensure_ascii=True))
