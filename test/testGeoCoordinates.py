import unittest
import geoTools
from geoTools.geoCoordinates import location


class TestLocation(unittest.TestCase):
    def test_pointOnEquatorIsZeroMeterFromEquator(self):
        self.assertEqual(location(0, 0).distanceFromEquatorInMeter(), 0)

    def test_pointOnNorthPoleIsTenThousandKilometerFromEquator(self):
        self.assertEqual(location(90, 0).distanceFromEquatorInMeter(), 10000000)

    def test_pointOnFortyFiveDegreeNorthIsFiveThousandKilometerFromEquator(self):
        self.assertEqual(location(45, 0).distanceFromEquatorInMeter(), 5000000)

    def test_pointOnFortyFiveDegreeSouthIsMinusFiveThousandKilometerFromEquator(self):
        self.assertEqual(location(-45, 0).distanceFromEquatorInMeter(), -5000000)


if __name__ == '__main__':
    unittest.main()
