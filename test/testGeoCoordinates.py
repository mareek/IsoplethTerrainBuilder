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

    def test_getStableLocatiosnInZone(self):
        swCorner = location(0, 0)
        neCorner = swCorner.moveNorth(200).moveEast(200)
        manyLocations = location.getAlignedLocationsInZone(swCorner, neCorner)
        self.assertEqual(9, len(manyLocations))

        singleLocation = location.getAlignedLocationsInZone(swCorner.moveNorth(1).moveEast(1),
                                                            neCorner.moveNorth(-1).moveEast(-1))
        self.assertEqual(1, len(singleLocation))

        self.assertEqual(singleLocation[0].latitude, manyLocations[4].latitude)
        self.assertEqual(singleLocation[0].longitude, manyLocations[4].longitude)

    def test_getNearestLocationOfZeroZero(self):
        zeroZero = location(0, 0)
        nearestAlignedLocations = zeroZero.getNearestAlignedLocations()
        self.assertEqual(len(nearestAlignedLocations), 1)
        self.assertEqual(nearestAlignedLocations[0].latitude, 0)
        self.assertEqual(nearestAlignedLocations[0].longitude, 0)

    def test_getNearestLocationOfDuingt(self):
        duingt = location(45.835343, 6.205914)
        nearestAlignedLocations = duingt.getNearestAlignedLocations()

        self.assertEqual(len(nearestAlignedLocations), 4)

        self.assertEqual(2, len(list(filter(lambda l: l.latitude < duingt.latitude, nearestAlignedLocations))))
        self.assertEqual(2, len(list(filter(lambda l: l.latitude > duingt.latitude, nearestAlignedLocations))))

        self.assertEqual(2, len(list(filter(lambda l: l.longitude < duingt.longitude, nearestAlignedLocations))))
        self.assertEqual(2, len(list(filter(lambda l: l.longitude > duingt.longitude, nearestAlignedLocations))))

        for nearestLocation in nearestAlignedLocations:
            self.assertAlmostEquals(nearestLocation.latitude, duingt.latitude, 2)
            self.assertAlmostEquals(nearestLocation.longitude, duingt.longitude, 2)

    def test_getNearestLocationOfRio(self):
        rio = location(-22.955044, -43.215391)
        nearestAlignedLocations = rio.getNearestAlignedLocations()

        self.assertEqual(len(nearestAlignedLocations), 4)

        self.assertEqual(2, len(list(filter(lambda l: l.latitude < rio.latitude, nearestAlignedLocations))))
        self.assertEqual(2, len(list(filter(lambda l: l.latitude > rio.latitude, nearestAlignedLocations))))

        self.assertEqual(2, len(list(filter(lambda l: l.longitude < rio.longitude, nearestAlignedLocations))))
        self.assertEqual(2, len(list(filter(lambda l: l.longitude > rio.longitude, nearestAlignedLocations))))

        for nearestLocation in nearestAlignedLocations:
            self.assertAlmostEquals(nearestLocation.latitude, rio.latitude, 2)
            self.assertAlmostEquals(nearestLocation.longitude, rio.longitude, 2)

