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

    @classmethod
    def from_json(cls, data):
        return cls(**data)
