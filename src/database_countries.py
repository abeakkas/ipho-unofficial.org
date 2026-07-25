import csv
from typing import NamedTuple

class Country(NamedTuple):
  code: str
  name: str
  website: str
  former: bool

database: list[Country] = []
code_to_country: dict[str, Country] = {}
previous_code: dict[str, str] = {}
next_code: dict[str, str] = {}

with open("database/countries.csv") as file:
  reader = csv.reader(file)
  prev_code = ""
  for row in reader:
    assert len(row) == 4, f"Expecting 4 elements per row: {row}"
    code, name, website, former = row
    country = Country(code, name, website, former != "")

    database.append(country)
    code_to_country[code] = country
    if prev_code:
      previous_code[code] = prev_code
      next_code[prev_code] = code
    prev_code = code
