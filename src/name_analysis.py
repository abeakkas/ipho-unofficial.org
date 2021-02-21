# Tries to find similar names in successive years
from database_students import database as db
from database_students import year_grouped as dby
from database_students import code_grouped as dbc
from difflib import SequenceMatcher
from unidecode import unidecode

def massive(from_year, to_year):
    for year in dby:
        for row in dby[year]:
            row['supername'] = row['code'] + " " + " ".join(sorted(unidecode(row['name']).split(" ")))
    threshold = .9
    for year1 in range(from_year, to_year + 1):
        print(year1)
        for year2 in range(year1 + 1, year1 + 5):
            if str(year1) in dby and str(year2) in dby:
                for row1 in dby[str(year1)]:
                    for row2 in dby[str(year2)]:
                        ratio = SequenceMatcher(None, row1['supername'], row2['supername']).ratio()
                        if ratio > threshold:
                            print(row1)
                            print(row2)

def comp(s1, s2):
    r1 = min(max(SequenceMatcher(None, x1, x2).ratio() for x2 in s2) for x1 in s1)
    r2 = min(max(SequenceMatcher(None, x2, x1).ratio() for x1 in s1) for x2 in s2)
    return max(r1, r2)

def withincountry(start_year=1967):
    threshold = .7
    for code in dbc:
        for row in dbc[code]:
            row['seq'] = unidecode(row['name']).replace("-", " ").split(" ")
        for i, row1 in enumerate(dbc[code]):
            for j, row2 in enumerate(dbc[code]):
                if int(row1['year']) < start_year or int(row2['year']) < start_year:
                    continue
                if i == j:
                    break
                if abs(int(row1['year']) - int(row2['year'])) < 3 and row1['name'] != row2['name']:
                    c = comp(row1['seq'], row2['seq'])
                    if c > threshold:
                        print(code)
                        print(c)
                        print(row1['year'], row1['name'])
                        print(row2['year'], row2['name'])

def samenamedifferentcountry():
    names = {}
    for row in db:
        row['ascii'] = row['name']#''.join(sorted(unidecode(row['name']).lower().replace("-", " ").split(" ")))
    for row in db:
        if row['ascii'] in names:
            if names[row['ascii']]['code'] != row['code'] or abs(int(names[row['ascii']]['year']) - int(row['year'])) > 2:
                print("wowowow")
                print(names[row['ascii']])
                print(row)
        else:
            names[row['ascii']] = row

withincountry(2017)
# samenamedifferentcountry()
# massive(2016, 2019)
