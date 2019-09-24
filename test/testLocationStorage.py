import unittest
import geoTools
import geoTools.locationStorage
from geoTools.geoCoordinates import location

class TestLocationDatabase(unittest.TestCase):
    def setUp(self):
        self.db = geoTools.locationStorage.locationDatabase()

    def test_getLocationOnEmptyDbRetirnsNone(self):
        self.assertEqual(self.db.getLocation(0, 0), None)

    def test_addAndGetLocation(self):
        self.db.addLocation(location(45, 5, 150))
        self.assertEqual(self.db.getLocation(0, 0), None)
        storedLocation = self.db.getLocation(45, 5)
        self.assertEqual(storedLocation.latitude, 45)
        self.assertEqual(storedLocation.longitude, 5)
        self.assertEqual(storedLocation.elevation, 150)
