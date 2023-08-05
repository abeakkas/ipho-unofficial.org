import csv
from collections import namedtuple
from database_countries import code_to_country as c_t_c

database = []

Row = namedtuple('Row', 'rank,name,code,medal,website')

with open("database/2020.csv") as file:
    reader = csv.reader(file)
    for row in reader:
        assert len(row) == 5, "2020 row error: {}".format(row)
        entry = Row(*row)

        if (entry.medal not in ["G", "S", "B", "H", "P"]
                or (entry.code != "" and entry.code not in c_t_c)):
            raise Exception("2020 database is corrupted! Row: {}".format(row))

        database.append(entry)
