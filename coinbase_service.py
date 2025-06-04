"""
service module for coinbase crypto
"""
import logging
import datetime

from crypto_utils.lots import Lot

DESIRED_PERCENT = 5.0
DESIRED_QTY = 1


class CoinbaseService:
    """
    class to encapsulate the CoinbaseService api
    """
    def __init__(self, account_manager, database_manager):
        """
        initialize the CoinbaseService
        """
        self.account_manager = account_manager
        self.database_manager = database_manager
        self.logger = logging.getLogger('simpleLogger')

    @staticmethod
    def percent_change(value1, value2):
        """
        return the percent change of value1 and value2
        :param value1:
        :param value2:
        :return:
        """
        diff = (value2 - value1) / value1
        return diff * 100

    def init_item_lot(self, item):
        """
        initialize a crypto lot purchase
        :param item: a string representation
            of a crypto currency pair: i.e. "BTC-USD"
        :return:
        """
        root = self.account_manager.get_product_info(item)
        product_id = root.product_id
        price = float(root.price)
        self.database_manager.store_price(product_id, price)
        # TODO: make save_lot the default behavior
        lot = Lot(root.product_id, str(DESIRED_QTY), str(price), False,
                  str(DESIRED_QTY*price), str(datetime.datetime.now()))
        self.database_manager.save_lot(lot)

    def ingest_data_single(self, item):
        """
        check a single crypto item and
        sell if meets desired percent change
        :param item: a string representation
            of a crypto currency pair: i.e. "BTC-USD"
        :return:
        """
        root = self.account_manager.get_product_info(item)
        product_id = root.product_id
        price = float(root.price)
        last_price = self.database_manager.select_last_price(product_id)
        my_percent_changed = self.percent_change(last_price, price)
        self.logger.info("product: %s | price: "
                         "[current: (%f) <= previous: (%f)] "
                         "| percent_change (since initial run): %f",
                         product_id, price, last_price,
                         my_percent_changed)
        if my_percent_changed >= DESIRED_PERCENT:
            print(
                f"*** FOUND increase {my_percent_changed} > {DESIRED_PERCENT} =>  "
                f"product: {product_id} | price: "
                f"[current: ({price}) <= previous: ({last_price})] ***")

            self.logger.info("FOUND increase: %f > %f => product: %s |"
                             " price: [current: (%f) <= previous: (%f)]",
                             my_percent_changed, DESIRED_PERCENT, product_id, price, last_price)
            print(f"SELL {item} now at percent changed: {my_percent_changed}!")
            # TODO: add some kind of "sell_lot" call here
            # else:
            #    logging.info(f"currently no change found above {desired_percent} percent")
            # self.database_manager.store_price(product_id, price)

    def init_all(self):
        """
        initialize all crypto pairs in the account
        :return:
        """
        self.database_manager.vacuum_old_prices()
        self.logger.info("establishing initial lots")
        self.ingest_data_multi(True)

    def ingest_data_multi(self, init_only=False):
        """
        ingest all account crypto pairs
        :param init_only: only init or run ingest
        :return:
        """
        for item in self.account_manager.get_crypto_pairs():
            if init_only:
                self.init_item_lot(item)
            else:
                self.ingest_data_single(item)
