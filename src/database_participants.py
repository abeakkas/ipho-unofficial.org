import csv
from collections import defaultdict
from enum import Enum
from typing import NamedTuple
from database_countries import code_to_country
from database_timeline import get_next_year

class Medal(str, Enum):
  GOLD = "G"
  SILVER = "S"
  BRONZE = "B"
  HONOURABLE = "H"
  PARTICIPANT = "P"

class Participant(NamedTuple):
  year: str
  rank: str
  rank_geq: bool
  name: str
  code: str
  medal: Medal
  theoretical: str
  experimental: str
  total: str
  website: str

def count_medals(participants: list[Participant]) -> dict[Medal, int]:
  counts = {m: 0 for m in Medal}
  for p in participants:
    counts[p.medal] += 1
  return counts

database: list[Participant] = []
code_grouped: dict[str, list[Participant]] = defaultdict(list)
year_grouped: dict[str, list[Participant]] = defaultdict(list)

with open("database/participants.csv") as file:
  reader = csv.reader(file)
  for row in reader:
    assert len(row) == 9, f"Expecting 9 elements per row: {row}"
    year, rank, name, code, medal, theoretical, experimental, total, website = row

    rank_geq = rank.startswith(">=")
    if rank_geq:
      rank = rank.removeprefix(">=")

    if code != "" and code not in code_to_country:
      raise Exception(f"Participant database is corrupted! Row: {row}")

    entry = Participant(year, rank, rank_geq, name, code, Medal(medal),
                        theoretical, experimental, total, website)

    database.append(entry)
    code_grouped[entry.code].append(entry)
    year_grouped[entry.year].append(entry)

last_year = max(year_grouped, key=int)
assert last_year in get_next_year, "Next year doesn't exist in timeline!"
next_year = get_next_year[last_year]
