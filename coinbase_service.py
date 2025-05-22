import psycopg2

from coinbase.rest import RESTClient
from crypto_utils.product import Root

desired_percent = 5.0


class CoinbaseService:
    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret
        self.client = RESTClient(self.api_key, self.api_secret)

    def store_price(self, name, price):
        self.execute_sql(f"INSERT INTO price_book(name, price, created_at) "
                         f"VALUES('{name}','{price}', now())")

    def vacuum_old_prices(self):
        print("vacuum records older than 1 hour")
        self.execute_sql("DELETE FROM price_book WHERE created_at < now()- interval '1 hour'")

    def select_last_price(self, crypto_name):
        price = self.execute_sql(
            f"SELECT price FROM price_book WHERE name = '{crypto_name}' "
            f"ORDER BY created_at DESC LIMIT 1")
        if price is None:
            price = 0.1
        return float(price)

    @staticmethod
    def percent_change(value1, value2):
        diff = (value2 - value1) / value1
        return diff * 100

    @staticmethod
    def execute_sql(sql_query):
        # TODO: move these creds
        db_params = {
            'dbname': 'crypto_prices',
            'user': 'postgres',
            'password': 'example',
            'host': 'localhost',
            'port': '5432'
        }
        try:
            conn = psycopg2.connect(**db_params)
            cur = conn.cursor()
            cur.execute(sql_query)
            return_value = None

            if cur.description:
                row = cur.fetchone()
                if row:
                    return_value = row[0]

            conn.commit()
            cur.close()
            conn.close()
            return return_value

        except psycopg2.Error as e:
            print(f"Database error: {e}")

    def init_item_lot(self, item):
        # print(f"initial buy lot for {item}")
        product_info = self.client.get_product(item)
        root = Root.from_dict(product_info.to_dict())
        product_id = root.product_id
        price = float(root.price)
        self.store_price(product_id, price)

    def ingest_data_single(self, item):
        product_info = self.client.get_product(item)
        root = Root.from_dict(product_info.to_dict())
        product_id = root.product_id
        price = float(root.price)
        # percent_changed = float(root.price_percentage_change_24h)
        last_price = self.select_last_price(product_id)
        my_percent_changed = self.percent_change(last_price, price)
        # print(
        #     f"INFO: product: {product_id} | price: "
        #     f"[current: ({price:.6f}) <= previous: ({last_price:.6f})] "
        #     f"| percent_change: {my_percent_changed:.2f} "
        #     f"| percent_change (24h): {percent_changed:.2f}")
        if my_percent_changed >= desired_percent:
            print(
                f"*** FOUND increase {my_percent_changed} > {desired_percent} =>  product: {product_id} | price: "
                f"[current: ({price:.6f}) <= previous: ({last_price:.6f})] ***")
            print(f"SELL {item} now at percent changed: {my_percent_changed}!")
        # else:
        #     print(f"currently no change found above {desired_percent} percent")
        # self.store_price(product_id, price)

    def init_all(self):
        self.vacuum_old_prices()
        print("establishing initial lots")
        self.ingest_data_multi(True)

    def ingest_data_multi(self, init_only=False):
        accounts = self.client.get_accounts()
        # print("accounts", accounts.to_dict())
        dict_from_df = accounts.to_dict()
        for key, value in dict_from_df.items():
            if key == "accounts":
                for item in value:
                    if item["name"] != "Cash (USD)" and item["currency"] not in ["ANT", "GALA",
                                                                                 "BIT", "GNT", "DDX",
                                                                                 "ETH2", "DAR", "USDC"]:
                        if init_only:
                            self.init_item_lot(item["currency"] + "-USD")
                        else:
                            self.ingest_data_single(item["currency"] + "-USD")
