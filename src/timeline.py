import timeline_index
import timeline_year
import timeline_2020
from database_timeline import database as editions

def run():
  print("Generating timeline")
  timeline_index.run()
  timeline_2020.run()
  for yeardata in editions:
    timeline_year.run(yeardata.year)

if __name__ == "__main__":
  run()

