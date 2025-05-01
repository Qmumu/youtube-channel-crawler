
import feapder
import youtube.api as YoutubeApi
import youtube.utils as utils

import time
import json
import traceback
import requests

api =  YoutubeApi.Api()

def get_channel_info(channel_url):
    channel_id = utils.get_channel_id(channel_url)
    playlist_id,author_info = api.get_channel_info(channel_id)
    author_info["channel_url"]=channel_url
    
    videos = api.get_videos_API(playlist_id)
    #Due to ip limit cancel this Function 
    # videos = api.get_videos_playlist(playlist_id)
    # processed_videos = []
    # for video in videos:
    #     video_url = video["link"]
    #     video_info = api.get_video_info(video_url)
    #     new_video = {
    #         **video,  
    #         "keywords": video_info.get("keywords", []) 
    #     }
    #     processed_videos.append(new_video)
    author_info["videos"]=videos[:min(3, len(videos))]
    return author_info


def get_channels_by_keywords(channel_url,channel_id,keywords,pages=1):
    keywords = str(keywords)
    
    if len(keywords)==0:
        search_query=channel_id+" ""photography"

        channels_infos_channelId = api.search_channals(search_query,limit_per_page=20,pages=pages)
        channels_infos_keyWords = []
    else:
        keywords_query = utils.build_search_query(keywords)
        search_query = channel_id+" "+keywords_query
        channels_infos_channelId = api.search_channals(search_query,limit_per_page=20,pages=pages)
        channels_infos_keyWords = api.search_channals(keywords_query,limit_per_page=20,pages=pages)
    related_channels = []
    for channel in channels_infos_channelId+channels_infos_keyWords:
        try:
            channel_data = {
                "channel_id":channel["subscribers"].replace("@",""),
                "channel_url":channel["link"]
            }
            related_channels.append(channel_data)
        except:
            continue
    return related_channels



if __name__ == '__main__':
    # print(json.dumps(get_user_info("phlearn","https://www.youtube.com/@phlearn"),ensure_ascii=False))
    print(json.dumps(get_channels_by_keywords("https://www.youtube.com/@CameraTalkVideos","CameraTalkVideos","photography cameras film \"digital photography\" \"film photography\" composition art entertainment \"camera talk\" \"classic cameras\" \"folding cameras\""),ensure_ascii=False))
    pass