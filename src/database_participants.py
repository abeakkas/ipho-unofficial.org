import csv
from collections import defaultdict
from enum import Enum
from typing import NamedTuple
from database_countries import Country
from database_countries import code_to_country
from database_timeline import get_next_year

class Medal(str, Enum):
  GOLD = "G"
  SILVER = "S"
  BRONZE = "B"
  HONOURABLE = "H"
  PARTICIPANT = "P"

class Participant(NamedTuple):
  year: int
  rank: str
  rank_geq: bool
  name: str
  country: Country
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

participants: list[Participant] = []
participants_by_code: dict[str, list[Participant]] = defaultdict(list)
participants_by_year: dict[int, list[Participant]] = defaultdict(list)

with open("database/participants.csv") as file:
  for row in csv.reader(file):
    assert len(row) == 9, f"Expecting 9 elements per row: {row}"
    year, rank, name, code, medal, theoretical, experimental, total, website = row

    rank_geq = rank.startswith(">=")
    if rank_geq:
      rank = rank.removeprefix(">=")

    participant = Participant(
      int(year),
      rank,
      rank_geq,
      name,
      code_to_country[code],
      Medal(medal),
      theoretical,
      experimental,
      total,
      website,
    )

    participants.append(participant)
    participants_by_code[code].append(participant)
    participants_by_year[participant.year].append(participant)

last_year = max(participants_by_year)
assert last_year in get_next_year, "Next year doesn't exist in timeline!"
next_year = get_next_year[last_year]
