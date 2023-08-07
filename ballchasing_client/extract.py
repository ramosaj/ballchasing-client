from ballchasing_client.aggregate import ReplayAggregator
from ballchasing_client.api import Replays, DetailedReplays
import pandas as pd


class Extractor:
    def __init__(
            self,
            player_id,
            start=None,
            end=None,
            before_delta = None,
            after_delta=None,
            freq = 'm',
            detailed = False
        ):

        if start and after_delta :
            self.start = start 
            self.end = start + after_delta 
        
        elif end and before_delta:
            self.end = end 
            self.start = end - before_delta
        
        self.player_id = player_id
        self.date_range = pd.date_range(start=start,end=end,freq=freq).values
        self.detailed = detailed
    

    def extract_date_range(self):
        for i,x in enumerate(self.date_range,start=1):
            after = self.date_range[i-1]
            before = self.date_range[i]
            client = Replays(self.player_id,after=after,before=before)
            result = []
            try:
                replays = client.request_records()
                if self.detailed:
                    detailed_replays = self.fetch_detailed_many(self, replays)
                    result += detailed_replays 
                else: 
                    result+= replays
                    
            except Exception as e:
                print("Rate limited by ballchasing")
    
    def fetch_detailed_many(self,replay_id=None,replays=None):
        detailed_replays = []
        if replays: 
            for replay in replays:
                detailed_replay = self.fetch_detailed_one(replay['id'])
                detailed_replays.append(detailed_replay)

            return detailed_replays
        elif replay_id:
            detailed_replay = self.fetch_detailed_one(replay['id'])
            return detailed_replay
            
    def fetch_detailed_one(self,replay_id):
        obj = DetailedReplays(replay_id)
        detailed_replay = obj.request_records()
        return detailed_replay







        
        

        
        

