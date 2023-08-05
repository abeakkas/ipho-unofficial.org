import csv
from collections import defaultdict
from collections import namedtuple

database = []
year_indexed = {}
code_grouped = defaultdict(list)
previous_year = {}
next_year = {}

Row = namedtuple('Row', 'number,year,date,code,city,homepage,p_country,p_student,code2')

with open("database/timeline.csv") as file:
    reader = csv.reader(file)
    prev = ""
    for row in reader:
        assert len(row) == 8, "Timeline row error: {}".format(row)
        code2 = ""
        if "&" in row[3]:
            row[3], code2 = row[3].split("&")
        entry = Row(*row, code2)

        database.append(entry)
        year_indexed[entry.year] = entry
        code_grouped[entry.code].append(entry)
        if entry.code2:
            code_grouped[entry.code2].append(entry)
        if prev != "":
            previous_year[entry.year] = prev
            next_year[prev] = entry.year
        prev = entry.year
