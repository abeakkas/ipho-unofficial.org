import csv
from typing import NamedTuple
from typing import Optional
from database_countries import Country
from database_countries import code_to_country

class Edition(NamedTuple):
  number: int
  year: int
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
    if self.number % 100 in (11, 12, 13):
      return "th"
    return {1: "st", 2: "nd", 3: "rd"}.get(self.number % 10, "th")

editions: list[Edition] = []
editions_by_year: dict[int, Edition] = {}
# Technically, years can be non-consecutive, and wow that actually happened in 2020.
get_previous_year: dict[int, int] = {}
get_next_year: dict[int, int] = {}

def editions_hosted_by(country: Country):
  return [e for e in editions if country in (e.host, e.host2)]

with open("database/timeline.csv") as file:
  prev = None
  for row in csv.reader(file):
    assert len(row) == 8, f"Timeline row error: {row}"
    number, year, date, code, city, homepage, p_country, p_participant = row

    if "&" in code:
      code, code2 = code.split("&")
    else:
      code2 = ""

    edition = Edition(
      int(number),
      int(year),
      date,
      code_to_country[code],
      code_to_country[code2] if code2 else None,
      city,
      homepage,
      p_country,
      p_participant,
    )

    editions.append(edition)
    editions_by_year[edition.year] = edition
    if prev is not None:
      get_previous_year[edition.year] = prev
      get_next_year[prev] = edition.year
    prev = edition.year
