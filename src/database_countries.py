import csv
from typing import NamedTuple

class Country(NamedTuple):
  code: str
  name: str
  website: str
  former: bool

database: list[Country] = []
code_indexed: dict[str, Country] = {}
previous_code: dict[str, str] = {}
next_code: dict[str, str] = {}

with open("database/countries.csv") as file:
  reader = csv.reader(file)
  prev = ""
  for row in reader:
    assert len(row) == 4, f"Expecting 4 elements per row: {row}"
    code, name, website, former = row
    entry = Country(code, name, website, former != "")

    database.append(entry)
    code_indexed[entry.code] = entry
    if prev:
      previous_code[entry.code] = prev
      next_code[prev] = entry.code
    prev = entry.code
