Introduction
============

This package will allow you to get zip code information. The data used in this
package can be retrieved from
https://web.archive.org/web/20101126192032/http://pablotron.org/files/zipcodes-csv-10-Aug-2004.zip

`pyzipcode` uses a local sqlite database to run. You can replace it with your
own other storage mechanism with a little effort.

Here is some basic usage...

```pycon
>>> from pyzipcode import ZipCodeDatabase
>>> zcdb = ZipCodeDatabase()
>>> zipcode = zcdb[54115]
>>> zipcode.zip
'54115'
>>> zipcode.city
'De Pere'
>>> zipcode.state
'WI'
>>> zipcode.longitude
-88.078959999999995
>>> zipcode.latitude
44.42042
>>> zipcode.timezone
-6
```

Search zip codes...

```pycon
>>> from pyzipcode import ZipCodeDatabase
>>> zcdb = ZipCodeDatabase()
>>> len(zcdb.find_zip(city="Oshkosh"))
7
```

Get a list of zipcodes around a radius of a zipcode (this actually searches a square area)

```pycon
>>> from pyzipcode import ZipCodeDatabase
>>> zcdb = ZipCodeDatabase()
>>> [z.zip for z in zcdb.get_zipcodes_around_radius('54901', 10)]
['54901', '54902', '54903', '54904', '54906', '54927', '54952', '54956', '54957', '54979', '54985']
```

The Data
========

The following is the original README file from `zipcodes-csv-10-Aug-2004.zip`:

```text
CivicSpace US ZIP Code Database
-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
written by Schuyler Erle <schuyler@geocoder.us>
5 August 2004

corrected total count and removed sql table definition
Neil Drumm <neil@civicspacelabs.org>
10 August 2004

The ZIP code database contained in 'zipcode.csv' contains 43191 ZIP
codes for the continetal United States, Alaska, Hawaii, Puerto Rico,
and American Samoa. The database is in comma separated value format,
with columns for ZIP code, city, state, latitude, longitude, timezone
(offset from GMT), and daylight savings time flag (1 if DST is observed
in this ZIP code and 0 if not).

This database was composed using ZIP code gazetteers from the US Census
Bureau from 1999 and 2000, augmented with additional ZIP code information
from the Census Bureau's TIGER/Line 2003 data set. Timezone information
was added using cartographic data sets from nationalatlas.gov. The
database is guaranteed to exclusively contain information gathered from
sources in the public domain, and thus be legal to redistribute.

The database is believed to contain over 98% of the ZIP Codes in current
use in the United States. The remaining ZIP Codes absent from this
database are entirely PO Box or Firm ZIP codes added in the last five
years, which are no longer published by the Census Bureau, but in any
event serve a very small minority of the population (probably on the
order of .1% or less). Although every attempt has been made to filter
them out, this data set may contain up to .5% false positives, that is,
ZIP codes that do not exist or are no longer in use but are included due
to erroneous data sources. The latitude and longitude given for each ZIP
code is typically (though not always) the geographic centroid of the ZIP
code; in any event, the location given can generally be expected to lie
somewhere within the ZIP code's "boundaries".

The database andthis README are copyright 2004 CivicSpace Labs, Inc.,
and are published under a Creative Commons Attribution-ShareAlike
license, which requires that all updates must be released under the same
license. See http://creativecommons.org/licenses/by-sa/2.0/ for more
details. Please contact schuyler@geocoder.us if you are interested in
receiving updates to this database as they become available.

-=- 30 -=-

Visit http://civicspacelabs.org/zipcodedb for latest information.
```

