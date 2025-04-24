import unittest


class TestCoinbase(unittest.TestCase):

    def setUp(self) -> None:
        self.assertEqual(True, True)

    def tearDown(self) -> None:
        self.assertEqual(True, True)

    def test_something(self):
        self.assertEqual(100, 100)  # add assertion here


if __name__ == '__main__':
    unittest.main()
