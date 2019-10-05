import unittest
import geoTools
from geoTools.locationStorage import locationDatabase
from geoTools.geoCoordinates import location

class TestLocationDatabase(unittest.TestCase):
    def setUp(self):
        self.db = locationDatabase()

    def test_getLocationOnEmptyDbRetirnsNone(self):
        self.assertEqual(self.db.getLocation(0, 0), None)

    def test_addAndGetLocation(self):
        self.db.addLocations([location(45, 5, 150)])
        self.assertEqual(self.db.getLocation(0, 0), None)
        storedLocation = self.db.getLocation(45, 5)
        self.assertEqual(storedLocation.latitude, 45)
        self.assertEqual(storedLocation.longitude, 5)
        self.assertEqual(storedLocation.elevation, 150)

    def test_normalizeLocation(self):
        duingt = location(45.831381, 6.205998, 450)
        normalizedDuingt = duingt.normalize()
        rio = location(-22.951564, -43.210753, 493)
        normalizedRio = rio.normalize()
        self.db.addLocations([rio, duingt])
        
        self.db.normalizeCoordinates([rio])
        
        self.assertEqual(self.db.getLocation(rio.latitude, rio.longitude), None)
        self.assertNotEqual(self.db.getLocation(normalizedRio.latitude, normalizedRio.longitude), None)
        self.assertNotEqual(self.db.getLocation(duingt.latitude, duingt.longitude), None)
        
        self.db.normalizeAllCoordinates()
        self.assertEqual(self.db.getLocation(duingt.latitude, duingt.longitude), None)
        self.assertNotEqual(self.db.getLocation(normalizedDuingt.latitude, normalizedDuingt.longitude), None)
