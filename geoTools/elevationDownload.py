from geoTools.geoCoordinates import location


class elevationManager:
    def __init__(self, locationDb, openElevationClient):
        self.locationDb = locationDb
        self.openElevationClient = openElevationClient

    def getLocationsFromZone(self, firstCorner, secondCorner):
        locationsFromZone = location.getAlignedLocationsInZone(firstCorner, secondCorner)
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
        chunckSize = 3
        i = 0
        while i < len(locationsToDownload):
            locationsToUpdate = locationsToDownload[i:i + chunckSize]
            self.updateLocations(locationsToUpdate, self.openElevationClient.downloadLocations(locationsToUpdate))
            self.locationDb.addLocations(locationsToUpdate)
            i += chunckSize

    def updateLocations(self, locationsToUpdate, downloadedLocations):
        for downloadedLocation in downloadedLocations:
            location = next(filter(lambda l: l.latitude == downloadedLocation.latitude and
                                   l.longitude == downloadedLocation.longitude, locationsToUpdate))
            location.elevation = downloadedLocation.elevation
