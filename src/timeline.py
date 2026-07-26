import timeline_index
import timeline_year
import timeline_2020
from database_timeline import editions

def run():
  print("Generating timeline")
  timeline_index.run()
  timeline_2020.run()
  for edition in editions:
    timeline_year.run(edition.year)

if __name__ == "__main__":
  run()

