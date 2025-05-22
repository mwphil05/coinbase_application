import os
import datetime
import schedule
import time
import ignore

from coinbase_service import CoinbaseService

api_key = os.environ.get('COINBASE_API_KEY')
api_secret = os.environ.get('COINBASE_API_SECRET')
coinbase_svc = CoinbaseService(api_key, api_secret)


def process_coinbase():
    coinbase_svc.init_all()
    schedule.every(2).minutes.do(check_coinbase)
    # schedule.every(15).seconds.do(check_coinbase)

    while True:
        schedule.run_pending()
        time.sleep(1)


def check_coinbase():
    # Your code to be executed every 30 minutes goes here
    print(f"Executing check_coinbase at {datetime.datetime.now()}")
    coinbase_svc.ingest_data_multi()
    # coinbase_svc.vacuum_old_prices()


process_coinbase()

# debugging code
# coinbase_svc.ingest_data_multi()
# coinbase_svc.vacuum_old_prices()


