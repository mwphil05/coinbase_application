"""
test module for coinbase
"""
import unittest
from unittest.mock import MagicMock, patch

from coinbase_service import CoinbaseService


class TestCoinbase(unittest.TestCase):
    """
    testcases for coinbase app
    """

    def setUp(self) -> None:
        self.database_manager = MagicMock()
        self.account_manager = MagicMock()
        self.account_manager.get_product_info = MagicMock()
        self.account_manager.get_product_info.__getitem__.side_effect = \
            get_product_test_response().__getitem__
        self.account_manager.get_crypto_pairs = MagicMock(return_value=["BTC-USD"])
        self.instance = CoinbaseService(self.account_manager, self.database_manager)
        self.instance.percent_change = MagicMock(return_value=0.5)

    def tearDown(self) -> None:
        self.assertEqual(True, True)

    def test_ingest_data_multi(self):
        """
        test the ingest_data_multi
        :return:
        """
        print("testing: test_ingest_data_multi")
        self.instance.ingest_data_multi()
        self.assertEqual(100, 100)  # add assertion here

    @patch("coinbase_service.DESIRED_PERCENT", 0.01)
    def test_ingest_data_single(self):
        """
        test the ingest_data_multi
        :return:
        """
        print("testing: test_ingest_data_single")
        self.instance.ingest_data_single("BTC-USD")
        self.assertEqual(100, 100)  # add assertion here


def get_product_test_response():
    """
     test data for product info object
    :return:
    """
    return {
        "product_id": "BTC-USD",
        "price": "140.21",
        "price_percentage_change_24h": "9.43%"
    }


if __name__ == '__main__':
    unittest.main()
