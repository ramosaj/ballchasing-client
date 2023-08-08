from ballchasing_client.extract import Extractor
from ballchasing_client.api import Replays,DetailedReplays
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd


def setup_arguments_start():
    start = datetime(year=2023,month=2,day=1)
    after_delta = relativedelta(months = 2)
    return start, after_delta

def setup_arguments_end():
    end = datetime(year=2023,month=2,day=1)
    before_delta = relativedelta(months = 2)
    return end, before_delta

   
def test_init_start():
    start,after_delta = setup_arguments_start()
    extract = Extractor(start=start,after_delta=after_delta,player_id="Retals")

    assert(extract.start == start)
    assert(extract.end == (start + after_delta))
    assert(datetime(year=2023,day=28,month=2).isoformat() in extract.date_range.astype(str))

def test_init_end():
    end,before_delta = setup_arguments_start()
    extract = Extractor(end=end,before_delta=before_delta,player_id="Retals")

    assert(extract.end == end)
    assert(extract.start == (end - before_delta))
    assert(datetime(year=2023,day=31,month=1).isoformat() in extract.date_range.astype(str))


def test_fetch_detailed_one(monkeypatch):
    def mock_request_records(*args,**kwargs):
        return {"id":"1234"}
    monkeypatch.setattr(DetailedReplays,"request_records",mock_request_records)
    start,after_delta = setup_arguments_start()
    extract = Extractor(start=start,after_delta=after_delta,player_id="Retals")
    assert(extract.fetch_detailed_one("12345") == {"id":"1234"})


def test_fetch_detailed_many(monkeypatch):
    def mock_request_records(*args,**kwargs):
        return {"id":"12345"}

    replays = [{"id":"12345"}]
    monkeypatch.setattr(DetailedReplays,"request_records",mock_request_records)
    start,after_delta = setup_arguments_start()
    extract = Extractor(start=start,after_delta=after_delta,player_id="Retals")
    assert(extract.fetch_detailed_many(replays)[0]['id'] == '12345')

    
def test_extract_date_range(monkeypatch):
    def mock_request_records(*args,**kwargs):
        return [{"id":"1234"},{"id":"12345"}]

    monkeypatch.setattr(Replays,"request_records",mock_request_records)
    start,after_delta = setup_arguments_start()
    extract = Extractor(start=start,after_delta=after_delta,player_id="Retals")
    print(extract.date_range)
    assert(extract.extract_date_range()[0]['id'] == "1234")


def test_detailed_extract_date_range(monkeypatch):
    def mock_fetch_detailed(*args,**kwargs):
        return {"id":"1234"}
    
    def mock_request_records(*args,**kwargs):
        return [{"id":"1234"},{"id":"12345"}]

    monkeypatch.setattr(Replays,"request_records",mock_request_records)
    monkeypatch.setattr(Extractor,"fetch_detailed_one",mock_fetch_detailed)

    start,after_delta = setup_arguments_start()
    extract = Extractor(start=start,after_delta=after_delta,player_id="Retals",detailed=True)
    assert(extract.extract_date_range())





