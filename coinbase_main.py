"""
main module for coinbase application
"""
import os
import time
import logging
import datetime
import schedule
import ignore

from coinbase_service import CoinbaseService

api_key = os.environ.get('COINBASE_API_KEY')
api_secret = os.environ.get('COINBASE_API_SECRET')
coinbase_svc = CoinbaseService(api_key, api_secret)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def process_coinbase():
    """
    main processing entry point
    :return:
    """
    coinbase_svc.init_all()
    # schedule.every(2).minutes.do(check_coinbase)
    schedule.every(15).seconds.do(check_coinbase)

    while True:
        schedule.run_pending()
        time.sleep(1)


def check_coinbase():
    """
    this is the callback function for processing
    :return:
    """
    # Your code to be executed every 30 minutes goes here
    logging.info("Executing check_coinbase at %s", datetime.datetime.now())
    coinbase_svc.ingest_data_multi()
    # coinbase_svc.vacuum_old_prices()


process_coinbase()

# debugging code
# coinbase_svc.ingest_data_multi()
# coinbase_svc.vacuum_old_prices()
