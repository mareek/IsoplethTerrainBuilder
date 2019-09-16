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

    @staticmethod
    def computeLatitude(distanceFromeEquatorInMeter):
        return 90 * distanceFromeEquatorInMeter / 10000000
    
    @staticmethod
    def ComputeLongitude(distanceFromGreenwichMeridianInMeter, distanceFromeEquatorInMeter):
        latitude = location.computeLatitude(distanceFromeEquatorInMeter)
        latitudeFactor = 1 / math.cos(math.radians(abs(latitude)))
        return 90 * latitudeFactor * distanceFromGreenwichMeridianInMeter/10000000


    def toLine(self, separator):
        return separator.join(map(lambda f: str(f), [self.latitude, self.longitude, self.elevation]))

    @staticmethod
    def headerLine(separator):
        return separator.join(['latitude', 'longitude', 'elevation'])

    @classmethod
    def from_json(cls, data):
        return cls(**data)
