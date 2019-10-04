import json
import geoTools
from geoTools import openElevation
from geoTools.locationStorage import locationDatabase
from geoTools.geoCoordinates import location
from geoTools.elevationDownload import elevationManager

manager = elevationManager(locationDatabase("./bin/locations.db"), openElevation.openElevationClient())
locations = manager.getLocationsFromZone(location(45.855830, 6.196099), location(45.761282, 6.343284))
#resultLocations = manager.getLocationsFromZone(location(45.844428, 6.202622), location(45.843075, 6.205402))

print(json.dumps(locations, default=lambda o: o.__dict__))
