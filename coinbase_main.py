from coinbase.rest import RESTClient
from json import dumps, loads, load
from crypto_utils.pricebooks import Root
from crypto_utils.product import Root
# import crypto_utils.account
import psycopg2
import os

# api_key = "organizations/53577ac0-e3af-4993-82ed-49265c834df1/apiKeys/dcaeb2d6-8225-42f2-a07c-b86e33891a30"
# api_secret = "-----BEGIN EC PRIVATE KEY-----\nMHcCAQEEIDchuo7p5/nzKt39ENCX5aku6pwqZj8yC6CzG9PwET+GoAoGCCqGSM49\nAwEHoUQDQgAEipzvPF2dcPflxFjHN/bMv7yBAolp5f5jLI46v/Gdbnu8/P/mPnPe\nJF2guGVuDfftFOpjmsmBpdIAGL358NSVAg==\n-----END EC PRIVATE KEY-----\n"
api_key = os.environ.get('COINBASE_API_KEY')
api_secret = os.environ.get('COINBASE_API_SECRET')
print(f"api_key: {api_key}")
print(f"api_secret: {api_secret}")

def store_price(name, price):
    # print(f"Storing current price for {name} as {price}")
    execute_sql(f"INSERT INTO price_book(name, price, created_at) VALUES('{name}','{price}', now())");


def vacuum_old_prices():
    print("vacuum records older than 1 hour")
    execute_sql("DELETE FROM price_book WHERE created_at < now()- interval '1 hour'")


def select_last_price(crypto_name):
    price = execute_sql_single_column_value(
        f"SELECT price FROM price_book WHERE name = '{crypto_name}' ORDER BY created_at DESC LIMIT 1")
    # print(f"select last price for {crypto_name}: {price}")
    return float(price)


def execute_sql(sql_query):
    try:
        conn = psycopg2.connect(database="crypto_prices",
                                user="postgres",
                                host='localhost',
                                password="example",
                                port=5432)
        cur = conn.cursor()
        cur.execute(sql_query)
        conn.commit()
        cur.close()
        conn.close()
    except psycopg2.Error as e:
        print(f"Database error: {e}")


def execute_sql_single_column_value(sql_query):
    # Database credentials
    db_params = {
        'dbname': 'crypto_prices',
        'user': 'postgres',
        'password': 'example',
        'host': 'localhost',
        'port': '5432'
    }
    try:
        # Connect to the database
        conn = psycopg2.connect(**db_params)
        cur = conn.cursor()

        # Execute the query
        cur.execute(sql_query)

        # Fetch the row
        row = cur.fetchone()

        if row:
            # Access column by index
            column_value = row[0]

            # Print the results
            # print(f"column_value: {column_value}")

        else:
            print("column_value not found")
            column_value = "0.01"

        # Close the cursor and connection
        cur.close()
        conn.close()

        return column_value

    except psycopg2.Error as e:
        print(f"Database error: {e}")


def percent_change(value1, value2):
    diff = (value2 - value1) / value1
    percent_change = diff * 100
    return percent_change


def ingest_data():
    client = RESTClient(api_key=api_key, api_secret=api_secret)
    accounts = client.get_accounts()
    dict_from_df = accounts.to_dict()
    for key, value in dict_from_df.items():
        if key == "accounts":
            for item in value:
                # balance = item["available_balance"]["value"]
                if item["name"] != "Cash (USD)" and item["currency"] not in ["ANT", "GALA", "BIT", "GNT", "DDX", "ETH2",
                                                                             "USDC"]:
                    product_info = client.get_product(item["currency"] + "-USD")
                    root = Root.from_dict(product_info.to_dict())
                    product_id = root.product_id
                    price = float(root.price)
                    percent_changed = float(root.price_percentage_change_24h)
                    last_price = select_last_price(product_id)
                    my_percent_changed = percent_change(last_price, price)
                    print(
                        f"product: {product_id} | price: [current: ({price:.6f}) <= previous: ({last_price:.6f})] | percent_change: {my_percent_changed:.2f} | percent_change (24h): {percent_changed:.2f}")
                    store_price(product_id, price)


ingest_data()
vacuum_old_prices()
#print(os.environ)
