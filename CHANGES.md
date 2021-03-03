# ChangeLog

## 3.0.1 (unreleased)

- Fix release

## 3.0.0 (2021-03-03)

- ZipCodeDatabase objects now behave like dictionaries
  - Looking up a non-existent zipcode raises a KeyError instead of IndexError
  - .get() now returns a ZipCode object instead of a list containing 1 ZipCode object
  - they now have a len(), can be iterated over and reversed()
  - they now have .keys() .values() and .items() methods
- ZipCode objects are created by passing multiple arguments, one for
  each value, instead of a tuple
- Support looking up 4 and 3 digit zip codes as integers
- Drop Python 2 support

  2.0.3 (unreleased)

---

- Nothing changed yet.

## 2.0.2 (2021-02-28)

- license update

## 2.0.1 (2021-02-25)

- Fix error message for unknown zip code[mpcusack]

## 2.0.0 (2020-04-07)

- updated to work with py3
  [David Schneider]

  1.0 (2016-01-20)

---

- Fix import code so that it is not run when the module is imported (for
  example, when building Sphinx API Documentation).
- Rename the import.py module to import_zipcode.py because `import` is a
  reserved Python keyword.
- Document the import_zipcode module.

  0.4

---

- updated to use maxmind database http://www.maxmind.com/app/postalcode

- now also keeps timezone and dst values

- longitude and latitude is now contains negative numbers

## 0.3

- use strings instead of integer for storing zip codes since zip codes can start
  with a Zero.

## 0.2

- catch sqlite db file reading errors and keep trying in case
  another process is trying to access the file at the same time.

## 0.1

- initial release
