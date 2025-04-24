import os

from coinbase_service import CoinbaseService

api_key = os.environ.get('COINBASE_API_KEY')
api_secret = os.environ.get('COINBASE_API_SECRET')

coinbase_svc = CoinbaseService(api_key, api_secret)
coinbase_svc.ingest_data()
coinbase_svc.vacuum_old_prices()
