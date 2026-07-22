import csv
from collections import defaultdict
from typing import NamedTuple

class Edition(NamedTuple):
  number: str
  year: str
  date: str
  code: str
  code2: str
  city: str
  homepage: str
  p_country: str
  p_participant: str

database: list[Edition] = []
year_indexed: dict[str, Edition] = {}
code_grouped: dict[str, list[Edition]] = defaultdict(list)
# Technically, years can be non-consecutive, and wow that actually happened in 2020.
get_previous_year: dict[str, str] = {}
get_next_year: dict[str, str] = {}

with open("database/timeline.csv") as file:
  reader = csv.reader(file)
  prev = ""
  for row in reader:
    assert len(row) == 8, f"Timeline row error: {row}"
    number, year, date, code, city, homepage, p_country, p_participant = row

    if "&" in code:
      code, code2 = code.split("&")
    else:
      code2 = ""

    entry = Edition(number, year, date, code, code2, city, homepage,
                    p_country, p_participant)

    database.append(entry)
    year_indexed[entry.year] = entry
    code_grouped[entry.code].append(entry)
    if entry.code2:
      code_grouped[entry.code2].append(entry)
    if prev != "":
      get_previous_year[entry.year] = prev
      get_next_year[prev] = entry.year
    prev = entry.year
