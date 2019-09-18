from geoCoordinates import location
import openElevation
import json

locations = [location(0, 0), location(45, 0), location(45.2, 3.89)]
resultLocations = openElevation.downloadLocations(locations)

print(json.dumps(resultLocations, default=lambda o: o.__dict__))
