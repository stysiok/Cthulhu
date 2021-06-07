import unittest 
from unittest.mock import MagicMock

import krakenex
from src.services.kraken import KrakenHelper, getAssets, Asset

class TestAsset(unittest.TestCase):
    def test_Asset_getAssets(self):
        cryptos = ['xbt', 'randomkey', 'doge']
        getMinBuysReturn = { "XXBTZEUR": { "ordermin": 0.0001 }, "DOGEEUR": { "ordermin": 50 }}
        getCurrentPricesReturn = { "XXBTZEUR": { "c": [ 34000 ] }, "DOGEEUR": { "c": [ 0.3123 ] }}
        krakenHelperMock = KrakenHelper()
        krakenHelperMock.getMinBuys = MagicMock(return_value = getMinBuysReturn)
        krakenHelperMock.getCurrentPrices = MagicMock(return_value = getCurrentPricesReturn)
        assets = getAssets(cryptos, krakenHelperMock)
        self.assertEqual(assets.__len__(), 2)
        xbtz = assets[0]
        self.assertEqual(xbtz.key, "XXBTZEUR")
        self.assertEqual(xbtz.orderMin, getMinBuysReturn["XXBTZEUR"]["ordermin"])
        self.assertEqual(xbtz.currentPrice, getCurrentPricesReturn["XXBTZEUR"]["c"][0])
        xbtz = assets[1]
        self.assertEqual(xbtz.key, "DOGEEUR")
        self.assertEqual(xbtz.orderMin, getMinBuysReturn["DOGEEUR"]["ordermin"])
        self.assertEqual(xbtz.currentPrice, getCurrentPricesReturn["DOGEEUR"]["c"][0])
    
    def test_Asset_getPrice(self):
        asset = Asset("coin")
        asset.orderMin = 20
        asset.currentPrice = 10
        price = asset.getPrice()
        self.assertEqual(price, 20 * 10)
        asset = Asset("coin")
        asset.orderMin = 0.001
        asset.currentPrice = 3400
        price = asset.getPrice()
        self.assertEqual(price, 0.001 * 3400)


class TestKrakenHelper(unittest.TestCase):
    def test_KrakenHelper_hasEnough(self):
        kraken = KrakenHelper()
        assets = [ Asset("coin"), Asset("magic") ]
        assets[0].orderMin = 10
        assets[0].currentPrice = 0.3212
        assets[1].orderMin = 0.001
        assets[1].currentPrice = 3400
        canBuy = kraken.hasEnough(300, assets)
        self.assertTrue(canBuy)
        cantBuy = kraken.hasEnough(0.02, assets)
        self.assertFalse(cantBuy)
    
    def test_KrakenHelper_getAffordable(self):
        kraken = KrakenHelper()
        assets = [ Asset("coin"), Asset("magic") ]
        assets[0].orderMin = 10
        assets[0].currentPrice = 0.3212
        assets[1].orderMin = 0.001
        assets[1].currentPrice = 6500
        canAffordBoth = kraken.getAffordable(300, assets)
        self.assertListEqual(canAffordBoth, assets)
        cantAffordAny = kraken.getAffordable(3.03, assets)
        self.assertListEqual(cantAffordAny, [])
        canAffordOnlyOne = kraken.getAffordable(5.53, assets)
        self.assertListEqual(canAffordOnlyOne, [ assets[0] ])


if __name__ == '__main__':
    unittest.main()