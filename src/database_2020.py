import csv
from typing import NamedTuple
from database_countries import Country
from database_countries import code_to_country
from database_participants import Medal

class Participant(NamedTuple):
  rank: str
  name: str
  country: Country
  medal: Medal
  website: str

participants: list[Participant] = []

with open("database/2020.csv") as file:
  for row in csv.reader(file):
    assert len(row) == 5, f"2020 row error: {row}"
    rank, name, code, medal, website = row
    participants.append(Participant(rank, name, code_to_country[code], Medal(medal), website))
