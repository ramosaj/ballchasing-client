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
            freq = 'M',
            detailed = False
        ):

        if start and after_delta :
            self.start = start 
            self.end = start + after_delta
        
        elif end and before_delta:
            self.end = end 
            self.start = end - before_delta
        elif start and end:
            self.start = start 
            self.end = end
        else:
            raise Exception("Acceptable combinations of start/end: (start,end), (end,before_delta), (start,after_delta)")
        
        self.player_id = player_id
        self.date_range = pd.date_range(start=self.start,end=self.end,freq=freq,unit='s',inclusive='left').values
        self.detailed = detailed
    

    def extract_date_range(self):
        result = []
        for i in range(1,len(self.date_range)):
            after = self.date_range[i-1]
            before = self.date_range[i]
            client = Replays(self.player_id,after=after,before=before)
            result = []
            replays = client.request_records()
            if self.detailed:
                detailed_replays = self.fetch_detailed_many(replays)
                result += detailed_replays 
            else: 
                result+= replays
                    
        
        return result
        
    
    def fetch_detailed_many(self,replays):
        detailed_replays = []
        for replay in replays:
            detailed_replay = self.fetch_detailed_one(replay['id'])
            detailed_replays.append(detailed_replay)
        return detailed_replays
            
    def fetch_detailed_one(self,replay_id):
        obj = DetailedReplays(replay_id)
        detailed_replay = obj.request_records()
        return detailed_replay







        
        

        
        

