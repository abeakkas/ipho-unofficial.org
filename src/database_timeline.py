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
  country_count: str
  participant_count: str

  @property
  def ordinal(self):
    """Ordinal suffix for the edition number, e.g. "st" for 41 (as in 41st)."""
    if self.number % 100 in (11, 12, 13):
      return "th"
    return {1: "st", 2: "nd", 3: "rd"}.get(self.number % 10, "th")

editions: list[Edition] = []
editions_by_year: dict[int, Edition] = {}
# Technically, years can be non-consecutive, and wow that actually happened in 2020.
year_before: dict[int, int] = {}
year_after: dict[int, int] = {}

def editions_hosted_by(country: Country):
  return [e for e in editions if country in (e.host, e.host2)]

with open("database/timeline.csv") as file:
  previous_year = None
  for row in csv.reader(file):
    assert len(row) == 8, f"Timeline row error: {row}"
    number, year, date, code, city, homepage, country_count, participant_count = row

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
      country_count,
      participant_count,
    )

    editions.append(edition)
    editions_by_year[edition.year] = edition
    if previous_year is not None:
      year_before[edition.year] = previous_year
      year_after[previous_year] = edition.year
    previous_year = edition.year
