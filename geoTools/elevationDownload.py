from geoCoordinates import location
import openElevation
import json
import locationStorage

locationDb = locationStorage.locationDatabase()


def geLocationsFromZone(firstCorner, secondCorner):
    locationsFromZone = location.getAligneLocationsInZone(firstCorner, secondCorner)
    locationsToDownload = []
    for locationFromZone in locationsFromZone:
        locationFromDb = locationDb.getLocation(locationFromZone.latitude, locationFromZone.longitude)
        if locationFromDb == None:
            locationsToDownload.append(locationFromZone)
        else:
            locationFromZone.elevation = locationFromDb.elevation
    downloadMissginLocations(locationsToDownload)


def downloadMissginLocations(locationsToDownload):
    i = 0
    while i < len(locationsToDownload):
        truc = locationsToDownload[i:10]
        downloadedLocations = openElevation.downloadLocations(truc)
        for downloadedLocation in downloadedLocations:
            location = next(filter(lambda l: l.latitude == downloadedLocation.latitude &
                                   l.longitude == downloadedLocation.longitude, truc))
            location.elevation = downloadedLocation.elevation
            locationDb.addLocation(location)
        i += 10


locations = [location(0, 0), location(45, 0), location(45.2, 3.89)]
resultLocations = openElevation.downloadLocations(locations)

print(json.dumps(resultLocations, default=lambda o: o.__dict__))
