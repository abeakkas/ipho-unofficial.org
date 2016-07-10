#!/usr/bin/python
import csv

database = []
year_indexed = {}
number_indexed = {}
code_grouped = {}
previous_year = {}
next_year = {}

with open("database/timeline.csv") as file:
    reader = csv.reader(file)
    prev = ""
    for row in reader:
        entry = {
            "number": row[0],
            "year": row[1],
            "date": row[2],
            "code": row[3],
            "city": row[4],
            "homepage": row[5],
            "p_country": row[6],
            "p_student": row[7],
            "gold": row[8],
            "silver": row[9],
            "bronze": row[10],
            "honourable": row[11]
        }
        database.append(entry)
        number_indexed[entry["number"]] = entry
        year_indexed[entry["year"]] = entry
        if entry["code"] not in code_grouped:
            code_grouped[entry["code"]] = []
        code_grouped[entry["code"]].append(entry)
        if prev != "":
            previous_year[entry["year"]] = prev
            next_year[prev] = entry["year"]
        prev = entry["year"]