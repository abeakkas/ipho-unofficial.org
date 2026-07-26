import countries_code
import countries_index
from database_countries import countries

def run():
  print("Generating countries")
  countries_index.run()
  for country in countries:
    countries_code.run(country.code)

if __name__ == "__main__":
  run()

