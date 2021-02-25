"""The pyzipcode package"""


from pyzipcode.settings import db_location
import sqlite3

import time


class ConnectionManager(object):
    """
    Assumes a database that will work with cursor objects
    """

    def __init__(self):
        # test out the connection...
        conn = sqlite3.connect(db_location)
        conn.close()

    def query(self, sql, params=None):
        """
        Query the database using the supplied SQL. The SQL should follow the
        formatting rules defined in :pep:`249` for SQLite, whos `paramstyle` is
        `qmark`. Doing so will protect against SQL injection attacks.

        For example::

           sql = "SELECT * FROM ZipCodes WHERE zip=?"
           params = ('94949',)

        """
        conn = None
        retry_count = 0
        while not conn and retry_count <= 10:
            # If there is trouble reading the file, retry for 10 attempts
            # then just give up...
            try:
                conn = sqlite3.connect(db_location)
            except sqlite3.OperationalError:
                retry_count += 1
                time.sleep(0.001)

        if not conn and retry_count > 10:
            raise sqlite3.OperationalError(
                "Can't connect to sqlite database: '%s'." % db_location
            )

        cursor = conn.cursor()
        if params is not None:
            cursor.execute(sql, params)
        else:
            cursor.execute(sql)
        res = cursor.fetchall()
        conn.close()
        return res


ZIP_QUERY = "SELECT * FROM ZipCodes WHERE zip=?"
ZIP_RANGE_QUERY = (
    "SELECT * FROM ZipCodes "
    "WHERE longitude >= ? "
    "  AND longitude <= ? "
    "  AND latitude >= ? "
    "  AND latitude <= ?"
)
ZIP_FIND_QUERY = "SELECT * FROM ZipCodes WHERE city LIKE ? AND state LIKE ?"


class ZipCode(object):
    """
    Represents one zipcode record from the database.
    """

    def __init__(self, data):
        self.zip = data[0]
        self.city = data[1]
        self.state = data[2]
        self.longitude = data[3]
        self.latitude = data[4]
        self.timezone = data[5]
        self.dst = data[6]


def format_result(zips):
    """
    Helper function to format the display of zipcode[s].
    Returns a list of ZipCode objects.
    """
    if len(zips) > 0:
        return [ZipCode(zc) for zc in zips]
    else:
        return None


class ZipNotFoundException(Exception):
    """
    Exception that is raised when a zipcode is not found in the database
    """

    pass


class ZipCodeDatabase(object):
    """
    Interface to the zipcode lookup functionality
    """

    def __init__(self, conn_manager=None):
        if conn_manager is None:
            conn_manager = ConnectionManager()
        self.conn_manager = conn_manager

    def get_zipcodes_around_radius(self, zipcode, radius):
        """
        Returns a list of ZipCode objects within radius miles of the zipcode.
        """
        zips = self.get(zipcode)
        if zips is None:
            raise ZipNotFoundException(
                "Could not find zipcode '%s' within radius %s" % (zipcode, radius)
            )
        else:
            zipcode = zips[0]

        radius = float(radius)

        long_range = (
            zipcode.longitude - (radius / 69.0),
            zipcode.longitude + (radius / 69.0),
        )
        lat_range = (
            zipcode.latitude - (radius / 49.0),
            zipcode.latitude + (radius / 49.0),
        )

        return format_result(
            self.conn_manager.query(
                ZIP_RANGE_QUERY,
                (long_range[0], long_range[1], lat_range[0], lat_range[1]),
            )
        )

    def find_zip(self, city=None, state=None):
        """
        Returns a list of ZipCode objects, optionally filtered by city and
        state. The filters are case-insensitive.
        """
        if city is None:
            city = "%"
        else:
            city = city.upper()

        if state is None:
            state = "%"
        else:
            state = state.upper()

        return format_result(self.conn_manager.query(ZIP_FIND_QUERY, (city, state)))

    def get(self, zipcode):
        """
        Return a list of one ZipCode object for the given zipcode.
        """
        return format_result(self.conn_manager.query(ZIP_QUERY, (zipcode,)))

    def __getitem__(self, zipcode):
        data = self.get(str(zipcode))
        if data is None:
            raise IndexError("Couldn't find zipcode: '%s'" % zipcode)
        else:
            return data[0]
