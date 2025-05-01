import feapder
import youtube.utils as utils
import youtube.handler  as handler
import traceback
import json
from  loguru import logger

class Youtube():
    channel_ids = []
    def batch_channel_detail(self):
        """
        Batch process YouTube channel information from seed data
        
        This function:
        1. Reads channel seeds from youtube_seeds.csv
        2. Fetches detailed information for each channel
        3. Saves the results to youtube_channel_data.csv
    """
        youtube_seeds = utils.get_channel_seeds_csv()
        for seed in youtube_seeds:
            channel_id = seed["channel_id"]
            channel_url = seed["channel_url"]
            try:
                user_info = handler.get_channel_info(channel_url)
            except:
                continue
            utils.save_to_csv(user_info,filename="youtube_channel_data.csv")
            logger.success("User data fetched successfully | channel_id: {} | channel_url: {}", channel_id, channel_url)

    def batch_related_channel(self):
        """
        Batch process to discover related channels using channel details and keywords
        
        This function:
        1. Reads channel details from youtube_channel_data.csv
        2. For each channel, searches for related channels using:
        - Channel URL
        - Channel ID
        - Channel keywords
        3. Saves discovered channels to youtube_seeds.csv
        """
        channel_details = utils.get_channel_detail_csv()
        for channel_detail in channel_details:
            channel_url = channel_detail["channel_url"]
            channel_id = channel_detail["channel_id"]
            keywords = channel_detail["keywords"]
            
            channel_datas = handler.get_channels_by_keywords(channel_url,channel_id,keywords)
            for channel_data in channel_datas:
                utils.save_to_csv_seeds(channel_data)
            logger.success("User data fetched successfully | channel_id: {} | channel_url: {}", channel_id, channel_url)
            
            
            


           
            

   

if __name__ == "__main__":
    youtube = Youtube()
    youtube.batch_channel_detail()
    youtube.batch_related_channel()
   
    

    