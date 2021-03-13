"""
A script to update the timezone data in the zipcode CSV file
============================================================

Reads the zipcode CSV file and updates the timezone/dst fields using
the lat/long coordinates.

Requires pytz and timezonefinder

Example usage::

   # Assumes the file ./zipcode.csv exists and contains zipcode data
   python update_timezones.py

"""

import csv
import datetime
import shutil
import tempfile
import sys
from pathlib import Path

import pytz
from timezonefinder import TimezoneFinder

try:
    from settings import db_location, csv_location
except ImportError:
    from pyzipcode.settings import db_location, csv_location

BEFORE_DST_DATE = datetime.datetime(2021, 2, 1)
DST_DATE = datetime.datetime(2021, 4, 1)

tf = TimezoneFinder()


def coords_to_utcoffset_and_isdst(lng, lat):
    timezone_name = tf.timezone_at(lng=lng, lat=lat)
    timezone = pytz.timezone(timezone_name)
    offset = timezone.utcoffset(BEFORE_DST_DATE).total_seconds() / 60 / 60
    dst = timezone.dst(DST_DATE).total_seconds() / 60 / 60
    return offset, dst, timezone_name


def run_update():
    """Run the import code."""
    with open(csv_location, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)

        new_rows = []
        for i, row in enumerate(reader, start=1):
            zip, city, state, lat, longt, timezone, dst = row
            longt, lat = float(longt), float(lat)
            timezone, dst = float(timezone), float(dst)

            new_timezone, new_dst, tz_name = coords_to_utcoffset_and_isdst(longt, lat)
            if timezone != new_timezone or dst != new_dst:
                print(
                    f"line {i: >5}: {zip}, {city: <26}, {state}, {lat}, {longt}\n"
                    f"{timezone},{dst} -> {new_timezone},{new_dst} ({tz_name})\n",
                    file=sys.stderr,
                )

            if new_timezone != int(new_timezone):
                raise ValueError("USA has fractional-hour timezones now")
            if new_dst not in [1, 0]:
                raise ValueError("expected dst to be either +1 or 0")

            new_timezone, new_dst = int(new_timezone), int(new_dst)
            new_rows.append([zip, city, state, lat, longt, new_timezone, new_dst])

    with tempfile.TemporaryDirectory() as tempdir:
        out_filename = Path(tempdir) / "zipcode.csv"

        with open(out_filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f, lineterminator="\n")
            writer.writerow(header)
            writer.writerows(new_rows)

        Path(csv_location).unlink()
        shutil.move(out_filename, csv_location)


if __name__ == "__main__":
    run_update()
