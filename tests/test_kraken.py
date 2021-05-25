import unittest 
from unittest.mock import MagicMock
from src.services.kraken import KrakenHelper, getAssets

class TestAsset(unittest.TestCase):
    def test_Asset_getPriceForAsset(self):
        cryptos = ['xbt', 'doge', 'randomkey']
        getMinBuysReturn = { "XXBTZEUR": { "ordermin": 0.0001 }, "DOGEEUR": { "ordermin": 50 }}
        getCurrentPricesReturn = { "XXBTZEUR": { "c": [ 34000 ] }, "DOGEEUR": { "c": [ 0.3123 ] }}
        _krakenHelperMock = KrakenHelper()
        _krakenHelperMock.getMinBuys = MagicMock(return_value = getMinBuysReturn)
        _krakenHelperMock.getCurrentPrices = MagicMock(return_value = getCurrentPricesReturn)
        assets = getAssets(cryptos, _krakenHelperMock)
        self.assertEqual(assets.__len__(), 2)
        xbtz = assets[0]
        self.assertEqual(xbtz.key, "XXBTZEUR")
        self.assertEqual(xbtz.orderMin, getMinBuysReturn["XXBTZEUR"]["ordermin"])
        self.assertEqual(xbtz.currentPrice, getCurrentPricesReturn["XXBTZEUR"]["c"][0])
        xbtz = assets[1]
        self.assertEqual(xbtz.key, "DOGEEUR")
        self.assertEqual(xbtz.orderMin, getMinBuysReturn["DOGEEUR"]["ordermin"])
        self.assertEqual(xbtz.currentPrice, getCurrentPricesReturn["DOGEEUR"]["c"][0])


if __name__ == '__main__':
    unittest.main()