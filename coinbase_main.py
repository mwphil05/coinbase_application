"""
main module for coinbase application
"""
import time
import logging.config
import datetime
import schedule
import ignore
from accounts_manager import AccountsManager

from coinbase_service import CoinbaseService
from database_manager import DatabaseManager

accounts_manager = AccountsManager()
database_manager = DatabaseManager()
coinbase_svc = CoinbaseService(accounts_manager, database_manager)
logging.config.fileConfig('logging.conf')
logger = logging.getLogger('simpleLogger')


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
    logger.info("Executing check_coinbase at %s", datetime.datetime.now())
    coinbase_svc.ingest_data_multi()
    # coinbase_svc.vacuum_old_prices()


process_coinbase()

# debugging code
# coinbase_svc.ingest_data_multi()
# coinbase_svc.vacuum_old_prices()
