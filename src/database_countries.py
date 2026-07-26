import csv
from typing import NamedTuple

class Country(NamedTuple):
  code: str
  name: str
  website: str
  former: bool

countries: list[Country] = []
code_to_country: dict[str, Country] = {}
code_before: dict[str, str] = {}
code_after: dict[str, str] = {}

with open("database/countries.csv") as file:
  previous_code = None
  for row in csv.reader(file):
    assert len(row) == 4, f"Expecting 4 elements per row: {row}"
    code, name, website, former = row

    country = Country(code, name, website, former != "")

    countries.append(country)
    code_to_country[code] = country
    if previous_code:
      code_before[code] = previous_code
      code_after[previous_code] = code
    previous_code = code
