import csv
from typing import NamedTuple

class Country(NamedTuple):
  code: str
  country: str
  website: str
  former: bool

database: list[Country] = []
code_indexed: dict[str, Country] = {}
code_to_country: dict[str, str] = {}
previous_code: dict[str, str] = {}
next_code: dict[str, str] = {}

with open("database/countries.csv") as file:
  reader = csv.reader(file)
  prev = ""
  for row in reader:
    assert len(row) == 4, "Country row error: {}".format(row)
    entry = Country(row[0], row[1], row[2], bool(row[3]))

    database.append(entry)
    code_indexed[entry.code] = entry
    code_to_country[entry.code] = entry.country
    if prev:
      previous_code[entry.code] = prev
      next_code[prev] = entry.code
    prev = entry.code
