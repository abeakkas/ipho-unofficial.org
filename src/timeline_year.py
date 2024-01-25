import sys
import util
import timeline_year_country
import timeline_year_index
import timeline_year_individual

def run(year):
    print("Generating timeline/" + year)
    util.makedirs("../timeline/" + year)
    timeline_year_index.run(year)
    timeline_year_country.run(year)
    timeline_year_individual.run(year)

if __name__ == "__main__":
    run(sys.argv[1])
