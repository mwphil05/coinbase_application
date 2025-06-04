"""
test module for coinbase
"""
import contextlib
import io
import unittest
from unittest import mock
from unittest.mock import MagicMock, patch, ANY

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
        self.account_manager.get_crypto_pairs = MagicMock(return_value=["BTC-USD",
                                                                        "ETH-USD", "SOL-USD"])
        self.instance = CoinbaseService(self.account_manager, self.database_manager)
        self.instance.percent_change = MagicMock(return_value=0.5)
        self.client = MagicMock()
        self.client.get_accounts().__getitem__.side_effect \
            = get_accounts_response().__getitem__

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
        val = "*** FOUND increase 0.5 > 0.01"
        with io.StringIO() as buf, contextlib.redirect_stdout(buf):
            self.instance.ingest_data_single("BTC-USD")
            output = buf.getvalue()
            print(output)
            self.assertTrue(val in output)

    def test_save_lot(self):
        """
        testing save_lot
        :return:
        """
        print("testing: test_save_lot")
        with mock.patch('database_manager.DatabaseManager') as mock_db_manager:
            mock_lot = mock.Mock()
            mock_db_manager.save_lot = mock.MagicMock(return_value="test")
            result = CoinbaseService(MagicMock(), mock_db_manager).init_item_lot(mock_lot)
            mock_db_manager.save_lot.assert_called_once_with(ANY)
        self.assertEqual(None, result)


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


def get_accounts_response():
    """
     test data for product info object
    :return:
    """
    return {
        "account": {
            "name": "XRP Wallet",
            "currency": "XRP",
        }
    }


if __name__ == '__main__':
    unittest.main()
