from ballchasing_client.extract import Extractor
from ballchasing_client.api import Replays,DetailedReplays
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd


class MockReplays:

    def request_records(self):
            return [{"id":"1234"},{"id":"12345"}]


class MockDetailedReplays:
     def request_records(self):
            return {"id":"12345"}
     


### Replay.fetch_records() to return list

def test_init():
    start = datetime(year=2023,month=2,day=1)
    after_delta = relativedelta(months = 1)
    extract = Extractor(start=start,after_delta=after_delta,player_id="Retals")

    assert(extract.start == start)
    assert(extract.end == (start + after_delta))
    assert(datetime(year=2023,day=28,month=2).isoformat() in extract.date_range.astype(str))


def test_fetch_detailed_one(monkeypatch):
    def mock_request_records(*args,**kwargs):
        return {"id":"1234"}
    monkeypatch.setattr(DetailedReplays,"request_records",mock_request_records)
    start = datetime(year=2023,month=2,day=1)
    after_delta = relativedelta(month = 1)
    extract = Extractor(start=start,after_delta=after_delta,player_id="Retals")
    assert(extract.fetch_detailed_one("12345") == {"id":"1234"})


def test_fetch_detailed_many(monkeypatch):
    def mock_request_records(*args,**kwargs):
        return [{"id":"1234"},{"id":"12345"}]

    replays = [{"id":"1234"},{"id":"12345"}]
    monkeypatch.setattr(Replays,"request_records",mock_request_records)
    start = datetime(year=2023,month=2,day=1)
    after_delta = relativedelta(month = 1)
    extract = Extractor(start=start,after_delta=after_delta,player_id="Retals")
    print(extract.fetch_detailed_many(replays))
    assert( {"id":"12345"} == extract.fetch_detailed_many(replays)[0])
    assert( {"id":"1234"} == extract.fetch_detailed_many(replays)[1])

    

def test_extract_date_range(monkeypatch):
    def mock_fetch_detailed(*args,**kwargs):
        return {"id":"1234"}
    monkeypatch.setattr(Extractor,"fetch_detailed_one",mock_fetch_detailed)
    start = datetime(year=2023,month=2,day=1)
    after_delta = relativedelta(month = 1)
    extract = Extractor(start=start,after_delta=after_delta,player_id="Retals")





