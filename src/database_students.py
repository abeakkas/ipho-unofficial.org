#!/usr/bin/python
import csv

database = []
code_grouped = {}
year_grouped = {}

with open("database/estudiantes.csv") as file:
    reader = csv.reader(file)
    for row in reader:
        entry = {
            "name": row[0],
            "code": row[1],
            "year": row[2],
            "rank": row[3],
            "medal": row[4]
        }
        database.append(entry)
        if entry["code"] not in code_grouped:
            code_grouped[entry["code"]] = []
        code_grouped[entry["code"]].append(entry)
        if entry["year"] not in year_grouped:
            year_grouped[entry["year"]] = []
        year_grouped[entry["year"]].append(entry)