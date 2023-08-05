import csv
from collections import defaultdict
from collections import namedtuple
from database_countries import code_to_country as c_t_c

database = []
code_grouped = defaultdict(list)
year_grouped = defaultdict(list)

Row = namedtuple('Row', 'year,rank,name,code,medal,theoretical,experimental,total,website,rank_geq')

with open("database/estudiantes.csv") as file:
    reader = csv.reader(file)
    for row in reader:
        assert len(row) == 9, "Student row error: {}".format(row)
        rank_geq = False
        if row[1][:2] == ">=":
            rank_geq = True
            row[1] = row[1][2:]
        entry = Row(*row, rank_geq)

        if (entry.medal not in ["G", "S", "B", "H", "P"]
                or (entry.code != "" and entry.code not in c_t_c)):
            raise Exception("Student database is corrupted! Row: {}".format(row))

        database.append(entry)
        code_grouped[entry.code].append(entry)
        year_grouped[entry.year].append(entry)

def check_point_rank_consistency():
    for year in year_grouped:
        if not year_grouped[year][0].total:
            continue
        last_rank = 0
        last_points = 1e10
        for row in year_grouped[year]:
            rank = int(row.rank)
            points = float(row.total)
            if points > last_points or (points == last_points and rank != last_rank):
                print("Row should have higher rank: {}".format(row))
            last_rank = rank
            last_points = points

def check_point_sums():
    for year in year_grouped:
        if (not year_grouped[year][0].theoretical or
            not year_grouped[year][0].experimental or
            not year_grouped[year][0].total):
            continue
        for row in year_grouped[year]:
            th = float(row.theoretical)
            ex = float(row.experimental)
            to = float(row.total)
            if abs(th + ex - to) > .0001:
                print("Points don't add up: {}".format(row))

def check_combining_characters():
    for row in database:
        for c in row.name:
            if 768 <= ord(c) < 880:
                print("Combining character {} detected: {}".format(c, row))

if __name__ == "__main__":
    check_point_rank_consistency()
    check_point_sums()
    check_combining_characters()
