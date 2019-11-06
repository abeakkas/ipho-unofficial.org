#!/usr/bin/python
import csv

database = []
code_indexed = {}
code_to_country = {}
previous_code = {}
next_code = {}

with open("database/countries.csv") as file:
    reader = csv.reader(file)
    prev = ""
    for row in reader:
        assert len(row) == 4, "Country row error: {}".format(row)
        entry = {
            "code": row[0],
            "country": row[1],
            "website": row[2],
            "former": row[3] == "former"
        }
        database.append(entry)
        code_indexed[entry["code"]] = entry
        code_to_country[entry["code"]] = entry["country"]
        if prev != "":
            previous_code[entry["code"]] = prev
            next_code[prev] = entry["code"]
        prev = entry["code"]
