#!/usr/bin/python
import util
import templates
import timeline_index
import timeline_year
from database_timeline import database as t_db

def run():
    print("Creating timeline")
    util.makedirs("../timeline")
    timeline_index.run()
    for yeardata in t_db:
        timeline_year.run(yeardata["year"])
    
if __name__ == "__main__":
    run()
