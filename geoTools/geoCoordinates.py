import math

metersInOneDegree = 10000000 / 90
degreesInOneMeter = 90 / 10000000


class location:
    def __init__(self, latitude, longitude, elevation=None):
        self.latitude = latitude
        self.longitude = longitude
        self.elevation = elevation

    def distanceFromEquatorInMeter(self):
        return self.latitude * metersInOneDegree

    def distanceFromGreenwichMeridianInMeter(self):
        latitudeFactor = math.cos(math.radians(abs(self.latitude)))
        return latitudeFactor * self.longitude * metersInOneDegree

    def moveNorth(self, distanceInMeter):
        newLatitude = location.computeLatitude(self.distanceFromEquatorInMeter() + distanceInMeter)
        return location(newLatitude, self.longitude).normalize()

    def moveEast(self, distanceInMeter):
        newDistanceFromGreenwich = self.distanceFromGreenwichMeridianInMeter() + distanceInMeter
        newLongitude = location.ComputeLongitude(newDistanceFromGreenwich, self.distanceFromEquatorInMeter())
        return location(self.latitude, newLongitude).normalize()

    def normalize(self, decimalDigits=5):
        return location(round(self.latitude, decimalDigits), round(self.longitude, decimalDigits), self.elevation)

    def getNearestAlignedLocations(self, offsetInMeter=100):
        if self.distanceFromEquatorInMeter() % offsetInMeter == 0:
            nearestLatitudes = [self.distanceFromEquatorInMeter()]
        else:
            nearestLatitude = (self.distanceFromEquatorInMeter() // offsetInMeter) * offsetInMeter
            nearestLatitudes = [nearestLatitude, nearestLatitude + offsetInMeter]
        if self.distanceFromGreenwichMeridianInMeter() % offsetInMeter == 0:
            nearestLongitudes = [self.distanceFromGreenwichMeridianInMeter()]
        else:
            nearestLongitude = (self.distanceFromGreenwichMeridianInMeter() // offsetInMeter) * offsetInMeter
            nearestLongitudes = [nearestLongitude, nearestLongitude + offsetInMeter]

        result = []
        referenceLatitude = location(0, 0)
        for latitude in nearestLatitudes:
            referenceLongitude = referenceLatitude.moveNorth(latitude)
            for longitude in nearestLongitudes:
                result.append(referenceLongitude.moveEast(longitude))

        return result

    @staticmethod
    def computeLatitude(distanceFromeEquatorInMeter):
        return degreesInOneMeter * distanceFromeEquatorInMeter

    @staticmethod
    def ComputeLongitude(distanceFromGreenwichMeridianInMeter, distanceFromeEquatorInMeter):
        latitude = location.computeLatitude(distanceFromeEquatorInMeter)
        latitudeFactor = 1 / math.cos(math.radians(abs(latitude)))
        return latitudeFactor * degreesInOneMeter * distanceFromGreenwichMeridianInMeter

    @staticmethod
    def getAlignedLocationsInZone(firstCorner, secondCorner, offsetInMeter=100):
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
