from ballchasing_client import api
from ballchasing_client.extract import Extractor
import pandas as pd
from datetime import date
from dateutil.relativedelta import relativedelta


def main():
    ## process_args
    args = None
    replays = Extractor(
        player_id=args,
        detailed=args,
        start=date.today() - relativedelta(day=1),
        end=date.today()
    ).extract_date_range()

if __name__ == '__main__':
    main()