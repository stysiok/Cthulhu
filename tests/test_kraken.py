import unittest 
from unittest.mock import MagicMock
from src.services.kraken import KrakenHelper, getAssets

class TestAsset(unittest.TestCase):
    def test_Asset_getPriceForAsset(self):
        cryptos = ['xbt', 'doge', 'randomkey']
        _krakenHelperMock = KrakenHelper()
        _krakenHelperMock.getMinBuys = MagicMock(return_value = { "XXBTZEUR": { "ordermin": 0.0001 }, "DOGEEUR": { "ordermin": 50 }})
        _krakenHelperMock.getCurrentPrices = MagicMock(return_value = { "XXBTZEUR": { "c": [ 34000 ] }, "DOGEEUR": { "c": [ 0.3123 ] }})
        assets = getAssets(cryptos, _krakenHelperMock)
        self.assertEqual(assets.len(), 2)


if __name__ == '__main__':
    unittest.main()