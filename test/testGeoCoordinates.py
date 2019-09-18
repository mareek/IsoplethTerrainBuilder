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

    def test_ComputeLatitudeOnEquator(self):
        self.assertEqual(location.computeLatitude(0), 0)

    def test_ComputeLatitudeOnNorthPole(self):
        self.assertEqual(location.computeLatitude(10000000), 90)

    def test_ComputeLatitudeAtBordeaux(self):
        self.assertEqual(location.computeLatitude(5000000), 45)

    def test_ComputeLongitudeAtEquatorLevel(self):
        self.assertEqual(location.ComputeLongitude(10000000, 0), 90)

    def test_ComputeLongitudeOfValence(self):
        longitude = location.ComputeLongitude(400000, 5000000)
        self.assertGreater(longitude, 4.9)
        self.assertLess(longitude, 5.1)

    def test_MoveNorthFromEquatorToNorthPole(self):
        start = location(0, 38.2)
        finish = start.moveNorth(10000000)
        self.assertEqual(finish.longitude, start.longitude)
        self.assertEqual(finish.latitude, 90)

    def test_MoveEastFromBordeauxToValence(self):
        start = location(45, 0)
        finish = start.moveEast(400000)
        self.assertEqual(finish.latitude, start.latitude)
        self.assertGreater(finish.longitude, 4.9)
        self.assertLess(finish.longitude, 5.1)


if __name__ == '__main__':
    unittest.main()
