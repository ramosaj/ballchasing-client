import datetime as dt
from jsonpath_ng import parse
import json
import pandas as pd

class ReplayAggregator:

    def __init__(self,records = None,filename=None):
        if records:
            self.records = records
        elif filename: 
            self.records = json.load(open(filename))
        else:
            self.records = []
        
    

    def extract_players(self,record):
        return record['blue']['players'] + record['orange']['players']

    def pull_player_score(self):
        scores = []
        for record in self.records:
            players = self.extract_players(record)
            for player in players: 
                scores.append({'score':player['score'],"date": record["date"],"name":player['name']})
        
        return scores


    def pull_core_stats(self):
        goals = []
        for record in self.records:
            players = self.extract_players(record)
            for player in players:
                platform = player['id']['platform']
                id = player['id']['id']
                goals.append({'date':record['date'], **player['stats']['core'],'player_id':f"{platform}:{id}","name":player['name'],"playlist":record['playlist_name']})
        
        return goals
            

    def aggregate_player_score(self):
        scores = self.pull_player_score()
        a = pd.DataFrame(scores)
        return a['score'].describe()
    
    def aggregate_core_stats(self):
        stats = self.pull_core_stats()
        a = pd.DataFrame(stats)
        return a.groupby("player_id").mean()
        
        
    








    
        