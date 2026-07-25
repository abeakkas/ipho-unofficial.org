import csv
from typing import NamedTuple
from typing import Optional
from database_countries import Country
from database_countries import code_to_country

class Edition(NamedTuple):
  number: str
  year: str
  date: str
  host: Country
  host2: Optional[Country]
  city: str
  homepage: str
  p_country: str
  p_participant: str

  @property
  def ordinal(self):
    """Ordinal suffix for the edition number, e.g. "st" for 41 (as in 41st)."""
    if self.number[-2:] in ("11", "12", "13"):
      return "th"
    return {"1": "st", "2": "nd", "3": "rd"}.get(self.number[-1], "th")

database: list[Edition] = []
year_indexed: dict[str, Edition] = {}
# Technically, years can be non-consecutive, and wow that actually happened in 2020.
get_previous_year: dict[str, str] = {}
get_next_year: dict[str, str] = {}

def editions_hosted_by(country: Country):
  return [e for e in database if country in (e.host, e.host2)]

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

    entry = Edition(number, year, date, code_to_country[code], code_to_country[code2] if code2 else None, city, homepage,
                    p_country, p_participant)

    database.append(entry)
    year_indexed[entry.year] = entry
    if prev != "":
      get_previous_year[entry.year] = prev
      get_next_year[prev] = entry.year
    prev = entry.year
