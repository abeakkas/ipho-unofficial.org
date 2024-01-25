import timeline_index
import timeline_year
import timeline_2020
import util
from database_timeline import database as t_db

def run():
    print("Generating timeline")
    util.makedirs("../timeline")
    timeline_index.run()
    timeline_2020.run()
    for yeardata in t_db:
        timeline_year.run(yeardata.year)

if __name__ == "__main__":
    run()
