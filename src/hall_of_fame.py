import templates
import util
from asciify import asciify
from collections import defaultdict
from database_countries import code_to_country
from database_students import code_grouped as dbc

def run():
    print("Creating hall_of_fame")

    bins = []
    key_to_bin = {}

    def row_to_key(row):
        return row.year + row.code + row.name

    def is_similar(name1, name2):
        name1 = " ".join(sorted(asciify(name1.replace("-", " ")).split(" ")))
        name2 = " ".join(sorted(asciify(name2.replace("-", " ")).split(" ")))
        return name1 == name2

    def merge(row1, row2):
        key1 = row_to_key(row1)
        key2 = row_to_key(row2)
        if key1 in key_to_bin:
            if key2 in key_to_bin:
                bin1 = key_to_bin[key1]
                bin2 = key_to_bin[key2]
                if bin1 != bin2:
                    bin1.extend(bin2)
                    for row in bin2:
                        key_to_bin[row_to_key(row)] = bin1
                    bins.remove(bin2)
            else:
                key_to_bin[key2] = key_to_bin[key1]
                key_to_bin[key2].append(row2)
        elif key2 in key_to_bin:
            key_to_bin[key1] = key_to_bin[key2]
            key_to_bin[key1].append(row1)
        else:
            bins.append([row1, row2])
            key_to_bin[key1] = bins[-1]
            key_to_bin[key2] = bins[-1]

    for code_rows in dbc.values():
       years = defaultdict(list)
       for row in code_rows:
           years[int(row.year)].append(row)
       for year, rows in years.items():
           for row1 in rows:
               for y in range(year - 2, year):
                   if y not in years:
                       continue
                   for row2 in years[y]:
                       if is_similar(row1.name, row2.name):
                           merge(row1, row2)

    def sort_key(bin):
        m = {"G": 0, "S": 0, "B": 0, "H": 0, "P": 0}
        for row in bin:
            m[row.medal] += 1
        return (-m["G"], -m["S"], -m["B"], -m["H"], row_to_key(bin[0]))

    sorted_bins = sorted(bins, key=sort_key)

    html = templates.get("hall_of_fame/index")
    html = templates.initial_replace(html, 2)

    tablehtml = ""
    for bin in sorted_bins:
        rowhtml = templates.get("hall_of_fame/index_row")
        rowhtml = rowhtml.replace("__NAME__", bin[0].name)
        rowhtml = rowhtml.replace("__CODE__", bin[0].code)
        rowhtml = rowhtml.replace("__COUNTRY__", code_to_country[bin[0].code])

        medals = {"G": 0, "S": 0, "B": 0, "H": 0, "P": 0}
        for row in bin:
            medals[row.medal] += 1

        # Cutoff at 2 golds
        if medals["G"] < 2:
            break

        rowhtml = rowhtml.replace("__GOLD__", str(medals["G"]))
        rowhtml = rowhtml.replace("__SILVER__", str(medals["S"]))
        rowhtml = rowhtml.replace("__BRONZE__", str(medals["B"]))
        rowhtml = rowhtml.replace("__HONOURABLE__", str(medals["H"]))

        participations = ""
        for row in sorted(bin, key=lambda row: row.year):
            if participations:
                participations += ", "
            year_html = templates.get("hall_of_fame/index_participation_year").strip()
            year_html = year_html.replace("__YEAR__", row.year)
            year_html = year_html.replace("__TITLE__", "Appeared as " + row.name)
            participations += year_html

        rowhtml = rowhtml.replace("__PARTICIPATIONS__", participations)

        tablehtml += rowhtml

    html = html.replace("__TABLE__", tablehtml)

    html = templates.final_replace(html, "..")
    util.makedirs("../hall_of_fame")
    util.writefile("../hall_of_fame/index.html", html)

if __name__ == "__main__":
    run()

