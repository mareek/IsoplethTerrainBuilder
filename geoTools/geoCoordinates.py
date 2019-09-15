import math

class location:
    def __init__(self, latitude, longitude, elevation=None):
        self.latitude = latitude
        self.longitude = longitude
        self.elevation = elevation

    def toLine(self, separator):
        return separator.join(map(lambda f: str(f), [self.latitude, self.longitude, self.elevation]))

    def distanceFromEquatorInMeter(self):
        return self.latitude * 10000000 / 90

    def distanceFromGreenwichMeridianInMeter(self):
        latitudeFactor = math.cos(math.radians(abs(self.latitude)))
        return latitudeFactor * self.longitude * 10000000 / 90

    @staticmethod
    def headerLine(separator):
        return separator.join(['latitude', 'longitude', 'elevation'])

    @classmethod
    def from_json(cls, data):
        return cls(**data)
