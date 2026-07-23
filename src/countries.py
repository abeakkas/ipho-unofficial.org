import countries_code
import countries_index
from database_countries import database as countries

def run():
  print("Generating countries")
  countries_index.run()
  for codedata in countries:
    countries_code.run(codedata.code)

if __name__ == "__main__":
  run()

