"""
service module for coinbase crypto
"""
import logging
import psycopg2

from coinbase.rest import RESTClient
from crypto_utils.product import Root

DESIRED_PERCENT = 5.0


class CoinbaseService:
    """
    class to encapsulate the CoinbaseService api
    """

    def __init__(self, api_key, api_secret):
        """
        initialize the CoinbaseService
        :param api_key: string with api key
        :param api_secret: string with secret
        """
        self.api_key = api_key
        self.api_secret = api_secret
        self.client = RESTClient(self.api_key, self.api_secret)

    def store_price(self, name, price):
        """
        persist the price to the db
        :param name:
        :param price:
        :return:
        """
        self.execute_sql(f"INSERT INTO price_book(name, price, created_at) "
                         f"VALUES('{name}','{price}', now())")

    def vacuum_old_prices(self):
        """
        delete records older than 1 hour
        :return:
        """
        logging.info("vacuum records older than 1 hour")
        self.execute_sql("DELETE FROM price_book WHERE created_at < now()- interval '1 hour'")

    def select_last_price(self, crypto_name):
        """
        return the last price of the crypto_name
        :param crypto_name:
        :return:
        """
        price = self.execute_sql(
            f"SELECT price FROM price_book WHERE name = '{crypto_name}' "
            f"ORDER BY created_at DESC LIMIT 1")
        if price is None:
            price = 0.1
        return float(price)

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

    @staticmethod
    def execute_sql(sql_query):
        """
        execute the given sql statement
        :param sql_query:
        :return:
        """
        # TODO: move these creds
        db_params = {
            'dbname': 'crypto_prices',
            'user': 'postgres',
            'password': 'example',
            'host': 'localhost',
            'port': '5432'
        }
        return_value = None
        try:
            conn = psycopg2.connect(**db_params)
            cur = conn.cursor()
            cur.execute(sql_query)

            if cur.description:
                row = cur.fetchone()
                if row:
                    return_value = row[0]

            conn.commit()
            cur.close()
            conn.close()
            return return_value

        except psycopg2.Error as e:
            logging.error("Database error: %s", e)

    def init_item_lot(self, item):
        """
        initialize a crypto lot purchase
        :param item:
        :return:
        """
        # print(f"initial buy lot for {item}")
        product_info = self.client.get_product(item)
        root = Root.from_dict(product_info.to_dict())
        product_id = root.product_id
        price = float(root.price)
        self.store_price(product_id, price)

    def ingest_data_single(self, item):
        """
        ingest a single crypto item
        :param item:
        :return:
        """
        product_info = self.client.get_product(item)
        root = Root.from_dict(product_info.to_dict())
        product_id = root.product_id
        price = float(root.price)
        percent_changed = float(root.price_percentage_change_24h)
        last_price = self.select_last_price(product_id)
        my_percent_changed = self.percent_change(last_price, price)
        logging.info("product: %s | price: "
                     "[current: (%f) <= previous: (%f)] "
                     "| percent_change: %f"
                     "| percent_change (24h): %f",
                     product_id, price, last_price,
                     my_percent_changed, percent_changed)
        if my_percent_changed >= DESIRED_PERCENT:
            print(
                f"*** FOUND increase {my_percent_changed} > {DESIRED_PERCENT} =>  "
                f"product: {product_id} | price: "
                f"[current: ({price:.6f}) <= previous: ({last_price:.6f})] ***")
            logging.info("FOUND increase: %f > %f => product: %s |"
                         " price: [current: (%f) <= previous: (%f)]",
                         my_percent_changed, DESIRED_PERCENT, product_id, price, last_price)
            print(f"SELL {item} now at percent changed: {my_percent_changed}!")
        # else:
        #    logging.info(f"currently no change found above {desired_percent} percent")
        # self.store_price(product_id, price)

    def init_all(self):
        """
        initialize all crypto pairs in the account
        :return:
        """
        self.vacuum_old_prices()
        logging.info("establishing initial lots")
        self.ingest_data_multi(True)

    def ingest_data_multi(self, init_only=False):
        """
        ingest all account crypto pairs
        :param init_only: only init or run ingest
        :return:
        """
        accounts = self.client.get_accounts()
        # print("accounts", accounts.to_dict())
        dict_from_df = accounts.to_dict()
        for key, value in dict_from_df.items():
            if key == "accounts":
                for item in value:
                    if item["name"] != "Cash (USD)" and item["currency"] \
                            not in \
                            ["ANT", "GALA", "BIT", "GNT", "DDX", "ETH2", "DAR", "USDC"]:
                        if init_only:
                            self.init_item_lot(item["currency"] + "-USD")
                        else:
                            self.ingest_data_single(item["currency"] + "-USD")
