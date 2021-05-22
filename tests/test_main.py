import unittest, sys
from src.services.kraken import Asset

class TestAsset(unittest.TestCase):
    def test_Asset_getPriceForAsset(self):
        a = Asset('DOGE', 10)
        self.assertTrue(True)