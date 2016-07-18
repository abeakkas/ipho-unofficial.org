#!/usr/bin/python
import csv

database = []
code_grouped = {}
year_grouped = {}

with open("database/estudiantes.csv") as file:
    reader = csv.reader(file)
    for row in reader:
        entry = {
            "year": row[0],
            "rank": row[1],
            "name": row[2],
            "code": row[3],
            "medal": row[4]
        }
        database.append(entry)
        if entry["code"] not in code_grouped:
            code_grouped[entry["code"]] = []
        code_grouped[entry["code"]].append(entry)
        if entry["year"] not in year_grouped:
            year_grouped[entry["year"]] = []
        year_grouped[entry["year"]].append(entry)