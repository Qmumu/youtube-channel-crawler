from youtubesearchpython import *
import json
proxy = {
    "http": "http://your_proxy_ip:port",
    "https": "http://your_proxy_ip:port"
}

# videosSearch = VideosSearch('NoCopyrightSounds', limit = 2)

# print(Channel.get("UC_aEa8K-EOJ3D6gOs7HcyNg"))
# playlistVideos = Playlist.get('https://www.youtube.com/playlist?list=UU47XN5bhLTBH5TRFyKaUpKg')
# print(json.dumps(playlistVideos,ensure_ascii=True))
# videoInfo = Video.getInfo('https://www.youtube.com/watch?v=-SoqQK8WAQw&t=2s', mode = ResultMode.json)
# print(videoInfo)

# from youtubesearchpython import ChannelsSearch

channelsSearch = ChannelsSearch('nicosphotographyshow', limit = 20, region = 'US')

print(json.dumps(channelsSearch.result(),ensure_ascii=True))
# channelsSearch.next()
# print(json.dumps(channelsSearch.result(),ensure_ascii=True))
