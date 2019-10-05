import json
import geoTools
from geoTools import openElevation
from geoTools.locationStorage import locationDatabase
from geoTools.geoCoordinates import location
from geoTools.elevationDownload import elevationManager

db = locationDatabase("./bin/locations.db")
#db.normalizeAllCoordinates()
manager = elevationManager(db, openElevation.openElevationClient())
locations = manager.getLocationsFromZone(location(45.855830, 6.196099), location(45.761282, 6.343284))

print(json.dumps(locations, default=lambda o: o.__dict__))
