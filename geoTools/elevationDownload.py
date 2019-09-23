from geoCoordinates import location
import openElevation
import json
import locationStorage


class elevationManager:
    def __init__(self, locationDb, downloadFunc):
        self.locationDb = locationDb
        self.downloadFunc = downloadFunc

    def getLocationsFromZone(self, firstCorner, secondCorner):
        locationsFromZone = location.getAligneLocationsInZone(firstCorner, secondCorner)
        locationsToDownload = []
        for locationFromZone in locationsFromZone:
            locationFromDb = self.locationDb.getLocation(locationFromZone.latitude, locationFromZone.longitude)
            if locationFromDb == None:
                locationsToDownload.append(locationFromZone)
            else:
                locationFromZone.elevation = locationFromDb.elevation
        self.downloadMissginLocations(locationsToDownload)

        return locationsFromZone

    def downloadMissginLocations(self, locationsToDownload):
        i = 0
        while i < len(locationsToDownload):
            locationsToUpdate = locationsToDownload[i:10]
            self.updateLocations(locationsToUpdate, self.downloadFunc(locationsToUpdate))
            for location in locationsToUpdate:
                self.locationDb.addLocation(location)
            i += 10

    def updateLocations(self, locationsToUpdate, downloadedLocations):
        for downloadedLocation in downloadedLocations:
            location = next(filter(lambda l: l.latitude == downloadedLocation.latitude and
                                   l.longitude == downloadedLocation.longitude, locationsToUpdate))
            location.elevation = downloadedLocation.elevation


#resultLocations = openElevation.downloadLocations(locations)
manager = elevationManager(locationStorage.locationDatabase(), openElevation.fakeDownloadLocations)
locations = manager.getLocationsFromZone(location(45.844428, 6.202622), location(45.843075, 6.205402))
resultLocations = manager.getLocationsFromZone(location(45.844428, 6.202622), location(45.843075, 6.205402))

print(json.dumps(resultLocations, default=lambda o: o.__dict__))
