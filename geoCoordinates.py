class location:
    def __init__(self, latitude, longitude, elevation=None):
        self.latitude = latitude
        self.longitude = longitude
        self.elevation = elevation

    def toLine(self, separator):
        return separator.join(map(lambda f: str(f), [self.latitude, self.longitude, self.elevation]))

    @staticmethod
    def headerLine(separator):
        return separator.join(['latitude', 'longitude', 'elevation'])

    @classmethod
    def from_json(cls, data):
        return cls(**data)
