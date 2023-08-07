import requests 
import os
from jsonpath_ng import parse
import json


class BallchasingApi:
    def __init__(self):
        self.token = "bKE1sr2t7XVr7pi3Ms6l8OjmnBdqf0cTwFomq1dD"
        self.jsonpath = None
        self.params = None
        self.endpoint = None

    def headers(self):
        return { "Authorization": self.token }

    def url_base(self):
        return "https://ballchasing.com/api/"
    
    def request_records(self):

        endpoint = self.endpoint
        url = self.url_base() + endpoint
        resp = requests.get(url,headers= self.headers(), params = self.params).json()
        if self.jsonpath:
            jsonpath_exp = parse(self.jsonpath)
            records = [match.value for match in jsonpath_exp.find(resp)]
        else: 
            return resp

        while "next" in resp:
            url = resp['next']
            resp = requests.get(url,headers=self.headers(),params = self.params)
            if resp.status_code == 429:
                print("Rate limit hit, waiting for 200 seconds")
                os.wait(200)
            else: 
                resp = resp.json()
                
            print(resp['list'][0]['date'])
            records += [match.value for match in jsonpath_exp.find(resp)]
        
        return records


class Replays(BallchasingApi):
    
    
    def __init__(self,player_id,before=None,after=None,limit=None):
        super().__init__()
        self.endpoint = "replays"
        self.jsonpath = "$.list[*]"
        self.params = {
            'player-id': player_id, 
            'replay-date-before':before,
            'replay-date-after': after
        }

    def save_to_file(self,filename):
        records = self.request_records()
        json.dump(records,open(filename,"w"))


class DetailedReplays(BallchasingApi):
    def __init__(self,replay_id):
        super().__init__()
        self.endpoint = f"replays/{replay_id}"

    

        
    




    
    
    





        
        

        

    
