import csv
from collections import namedtuple

database = []
code_indexed = {}
code_to_country = {}
previous_code = {}
next_code = {}

Row = namedtuple('Row', 'code,country,website,former')

with open("database/countries.csv") as file:
    reader = csv.reader(file)
    prev = ""
    for row in reader:
        assert len(row) == 4, "Country row error: {}".format(row)
        entry = Row(*row)

        database.append(entry)
        code_indexed[entry.code] = entry
        code_to_country[entry.code] = entry.country
        if prev:
            previous_code[entry.code] = prev
            next_code[prev] = entry.code
        prev = entry.code
