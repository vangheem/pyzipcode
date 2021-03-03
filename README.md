Introduction
============

This package will allow you to get zip code information. The data used in this
package is retrieved from
http://pablotron.org/files/zipcodes-csv-10-Aug-2004.zip

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
