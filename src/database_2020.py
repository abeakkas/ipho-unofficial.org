import csv
from database_countries import code_to_country as c_t_c

database = []

with open("database/2020.csv") as file:
    reader = csv.reader(file)
    for row in reader:
        assert len(row) == 5, "2020 row error: {}".format(row)
        entry = {
            "rank": row[0],
            "name": row[1],
            "code": row[2],
            "medal": row[3],
            "website": row[4],
        }
        if (entry["medal"] not in ["G", "S", "B", "H", "P"]
                or (entry["code"] != "" and entry["code"] not in c_t_c)):
            raise Exception("2020 database is corrupted! Row: {}".format(row))
        database.append(entry)
