"""
a db manager
"""
import logging

import psycopg2


class DatabaseManager:
    """
    class to manage db interaction
    """
    def __init__(self):
        """
        initialize the CoinbaseService
        """
        self.logger = logging.getLogger('simpleLogger')

    def execute_sql(self, sql_query):
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
            self.logger.error("Database error: %s", e)

    def store_price(self, name, price):
        """
        persist the price to the db
        :param name:
        :param price:
        :return:
        """
        self.execute_sql(f"INSERT INTO price_book(name, price, created_at) "
                         f"VALUES('{name}','{price}', now())")

    def save_lot(self, lot):
        """
        INSERT INTO "lots" ("id", "name", "quantity", "price_paid",
        "created_at", "executed", "value") VALUES
        (1,	'BTC_USD',	1,	5.00,	'2025-05-26 15:52:31.502472',
        '0',	5.00);

        persist the price to the db
        :param lot:
        :return:
        """
        self.execute_sql(f"INSERT INTO lots(name, quantity, price_paid, executed, "
                         f"value, created_at) "
                         f"VALUES('{lot.name}','{lot.quantity}', '{lot.price_paid}',"
                         f"'{lot.executed}', '{lot.value}', now())")

    def vacuum_old_prices(self):
        """
        delete records older than 1 hour
        :return:
        """
        self.logger.info("vacuum records older than 1 hour")
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
