import sqlite3
from geoTools.geoCoordinates import location


class locationDatabase:
    def __init__(self, databaseFilePath=":memory:"):
        self.connection = sqlite3.connect(databaseFilePath)
        self._initDatabase()

    # create table if it does not exists
    def _initDatabase(self):
        cur = self.connection.cursor()
        cur.execute("create table if not exists location(latitude real not null, longitude real not null, elevation int not null, primary key(latitude, longitude))")
        cur.execute("create index if not exists idx_location_latitude on location(latitude)")
        cur.execute("create index if not exists idx_location_longitude on location(longitude)")
        cur.close()

    # Get location from the database
    def getLocation(self, latitude, longitude):
        cur = self.connection.cursor()
        cur.execute("select elevation from location where latitude = ? and longitude = ?", (latitude, longitude))
        elevationTuple = cur.fetchone()
        cur.close()
        if elevationTuple == None:
            return None
        else:
            return location(latitude, longitude, elevationTuple[0])

    def addLocations(self, locations):
        for location in locations:
            row = (location.latitude, location.longitude, location.elevation)
            self.connection.execute("insert into location (latitude, longitude, elevation) values (?,?,?)", row)
        self.connection.commit()

    def getAllElevations(self):
        cur = self.connection.cursor()
        cur.execute("select distinct elevation from location order by 1")
        result = cur.fetchall()
        cur.close()
        truc = list(map(lambda r: r[0], result))
        return truc

    def normalizeAllCoordinates(self):
        for elevation in self.getAllElevations():
            cur = self.connection.cursor()
            cur.execute("select latitude, longitude, elevation from location where elevation = ?", [elevation])
            results = cur.fetchall()
            cur.close()
            locationsAtElevation = list(map(lambda result: location(result[0], result[1], result[2]), results))
            self.normalizeCoordinates(locationsAtElevation)

    def normalizeCoordinates(self, locations):
        for location in locations:
            normalizedLocation = location.normalize()
            if location.latitude != normalizedLocation.latitude or location.longitude != normalizedLocation.longitude:
                sqlUpdateQuery = ("update location set latitude = ?, longitude = ?, elevation = ? "
                                  "where latitude = ? and longitude = ?")
                sqlUpdateParams = (normalizedLocation.latitude, normalizedLocation.longitude,
                                   normalizedLocation.elevation, location.latitude, location.longitude)
                self.connection.execute(sqlUpdateQuery, sqlUpdateParams)
        self.connection.commit()
