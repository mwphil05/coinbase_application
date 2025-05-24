"""
 class to manage Coinbase accounts
"""
import os
import logging

from coinbase.rest import RESTClient
from crypto_utils.product import Root

api_key = os.environ.get('COINBASE_API_KEY')
api_secret = os.environ.get('COINBASE_API_SECRET')
EXCLUDED_PAIRS = ["ANT", "GALA", "BIT", "GNT", "DDX", "ETH2", "DAR", "USDC"]


class AccountsManager:
    """
     class to manage Coinbase accounts
    """

    def __init__(self):
        """
        initialize the AccountsManager
        """
        self.client = RESTClient(api_key, api_secret)
        self.logger = logging.getLogger('simpleLogger')
        self.var = None

    def get_crypto_pairs(self):
        """
         return a list of crypto product info pairs
        :return:
        """
        pairs = []
        accounts = self.client.get_accounts()
        # print("accounts", accounts.to_dict())
        dict_from_df = accounts.to_dict()
        for key, value in dict_from_df.items():
            if key == "accounts":
                for item in value:
                    if item["name"] != "Cash (USD)" and item["currency"] not in EXCLUDED_PAIRS:
                        pairs.append(item["currency"] + "-USD")
        return pairs

    def get_product_info(self, item):
        """
        return the crupto product info based on
            crypto currency pair: i.e. "BTC-USD"
        :return:
        """
        product_info = self.client.get_product(item)
        return Root.from_dict(product_info.to_dict())

