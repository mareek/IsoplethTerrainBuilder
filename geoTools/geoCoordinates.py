import math


class location:
    def __init__(self, latitude, longitude, elevation=None):
        self.latitude = latitude
        self.longitude = longitude
        self.elevation = elevation

    def distanceFromEquatorInMeter(self):
        return self.latitude * 10000000 / 90

    def distanceFromGreenwichMeridianInMeter(self):
        latitudeFactor = math.cos(math.radians(abs(self.latitude)))
        return latitudeFactor * self.longitude * 10000000 / 90

    def moveNorth(self, distanceInMeter):
        newLatitude = location.computeLatitude(self.distanceFromEquatorInMeter() + distanceInMeter)
        return location(newLatitude, self.longitude)

    def moveEast(self, distanceInMeter):
        newDistanceFromGreenwich = self.distanceFromGreenwichMeridianInMeter() + distanceInMeter
        newLongitude = location.ComputeLongitude(newDistanceFromGreenwich, self.distanceFromEquatorInMeter())
        return location(self.latitude, newLongitude)

    @staticmethod
    def computeLatitude(distanceFromeEquatorInMeter):
        return 90 * distanceFromeEquatorInMeter / 10000000

    @staticmethod
    def ComputeLongitude(distanceFromGreenwichMeridianInMeter, distanceFromeEquatorInMeter):
        latitude = location.computeLatitude(distanceFromeEquatorInMeter)
        latitudeFactor = 1 / math.cos(math.radians(abs(latitude)))
        return 90 * latitudeFactor * distanceFromGreenwichMeridianInMeter/10000000

    @staticmethod
    def getAligneLocationsInZone(firstCorner, secondCorner, offsetInMeter=100):
        southWestCorner = location(min([firstCorner.latitude, secondCorner.latitude]),
                                   min([firstCorner.longitude, secondCorner.longitude]))
        northEastCorner = location(max([firstCorner.latitude, secondCorner.latitude]),
                                   max([firstCorner.longitude, secondCorner.longitude]))

        distFromEquator = southWestCorner.distanceFromEquatorInMeter()
        startNorth = offsetInMeter * (distFromEquator // offsetInMeter)
        if distFromEquator > 0:
            startNorth += offsetInMeter

        distFromGreenwich = southWestCorner.distanceFromGreenwichMeridianInMeter()
        startEast = offsetInMeter * (distFromGreenwich // offsetInMeter)
        if distFromGreenwich > 0:
            startEast += offsetInMeter

        referenceLatitude = location(0, 0)

        result = []
        offsetNorth = 0
        while referenceLatitude.moveNorth(startNorth + offsetNorth).latitude <= northEastCorner.latitude:
            offsetEast = 0
            referenceLongitude = referenceLatitude.moveNorth(startNorth + offsetNorth)
            while referenceLongitude.moveEast(startEast + offsetEast).longitude <= northEastCorner.longitude:
                result.append(referenceLongitude.moveEast(startEast + offsetEast))
                offsetEast += offsetInMeter
            offsetNorth += offsetInMeter
        return result

    @classmethod
    def from_json(cls, data):
        return cls(**data)
