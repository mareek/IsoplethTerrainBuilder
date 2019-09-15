from geoCoordinates import location
import openElevation

locations = [location(0, 0), location(45, 0), location(45.2, 3.89)]
resultLocations = openElevation.downloadLocations(locations)

print(location.headerLine('\t'))
for location in resultLocations:
    print(location.toLine('\t'))
