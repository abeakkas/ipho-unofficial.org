import csv
from collections import defaultdict
from enum import Enum
from typing import NamedTuple
from database_countries import code_to_country

class Medal(str, Enum):
  GOLD = "G"
  SILVER = "S"
  BRONZE = "B"
  HONOURABLE = "H"
  PARTICIPANT = "P"

class Participant(NamedTuple):
  year: str
  rank: str
  name: str
  code: str
  medal: Medal
  theoretical: str
  experimental: str
  total: str
  website: str
  rank_geq: bool

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

    rank_geq = False
    if row[1][:2] == ">=":
      rank_geq = True
      row[1] = row[1][2:]

    if row[3] != "" and row[3] not in code_to_country:
      raise Exception(f"Participant database is corrupted! Row: {row}")

    entry = Participant(*row[:4], Medal(row[4]), *row[5:], rank_geq)

    database.append(entry)
    code_grouped[entry.code].append(entry)
    year_grouped[entry.year].append(entry)
