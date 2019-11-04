#!/usr/bin/python
import sys
import util
import templates
from database_countries import code_to_country
from database_students import year_grouped as s_db_y
from database_timeline import year_indexed as t_db_y
from database_timeline import previous_year
from database_timeline import next_year
from functools import cmp_to_key

def run(year):
    print("Creating timeline/" + year + "/country")
    html = templates.get("timeline/year/country")
    html = templates.initial_replace(html, 1)
    yeardata = t_db_y[year]
    html = html.replace("__YEAR__", year)
    html = html.replace("__NUMBER__", yeardata["number"])
    html = html.replace("__ORDINAL__", util.ordinal(yeardata["number"]))

    if year in previous_year:
        html = html.replace("__PREVIOUS_YEAR__", previous_year[year])
        html = html.replace("__PREVIOUS_YEAR_STYLE__", "")
    else:
        html = html.replace("__PREVIOUS_YEAR_STYLE__", "display: none;")
        html = html.replace("__PREVIOUS_YEAR__", ".") # Google crawler fix

    if year in next_year:
        html = html.replace("__NEXT_YEAR__", next_year[year])
        html = html.replace("__NEXT_YEAR_STYLE__", "")
    else:
        html = html.replace("__NEXT_YEAR_STYLE__", "display: none;")
        html = html.replace("__NEXT_YEAR__", ".") # Google crawler fix

    medals = {}
    if year in s_db_y:
        for row in s_db_y[year]:
            if row["code"] == "":
                # Country unknown
                continue
            if row["code"] not in medals:
                medals[row["code"]] = {
                    "bestrank": int(row["rank"]),
                    "bestrank>=": "&ge;" if row["rank>="] else "",
                    "gold": 0,
                    "silver": 0,
                    "bronze": 0,
                    "honourable": 0
                    }
            if row["medal"] == "G":
                medals[row["code"]]["gold"] += 1
            elif row["medal"] == "S":
                medals[row["code"]]["silver"] += 1
            elif row["medal"] == "B":
                medals[row["code"]]["bronze"] += 1
            elif row["medal"] == "H":
                medals[row["code"]]["honourable"] += 1

    def keyfn(code):
        m = medals[code]
        return (-m["gold"], -m["silver"], -m["bronze"], -m["honourable"],
                m["bestrank"], code)

    sortedcodes = sorted(medals, key = keyfn)

    tablehtml = ""
    prevcode = ""
    prevrank = 0
    for i, code in enumerate(sortedcodes):
        rowhtml = templates.get("timeline/year/country_row")
        rowhtml = rowhtml.replace("__CODE__", code)
        rowhtml = rowhtml.replace("__COUNTRY__", code_to_country[code])
        if prevcode != "" and keyfn(prevcode) == keyfn(code):
            rowhtml = rowhtml.replace("__RANK__", prevrank)
        else:
            rowhtml = rowhtml.replace("__RANK__", str(i + 1))
            prevcode = code
            prevrank = str(i + 1)
        rowhtml = rowhtml.replace("__GOLD__", str(medals[code]["gold"]))
        rowhtml = rowhtml.replace("__SILVER__", str(medals[code]["silver"]))
        rowhtml = rowhtml.replace("__BRONZE__", str(medals[code]["bronze"]))
        rowhtml = rowhtml.replace("__HONOURABLE__", str(medals[code]["honourable"]))
        rowhtml = rowhtml.replace("__BEST_RANK__", medals[code]["bestrank>="] + str(medals[code]["bestrank"]))
        tablehtml += rowhtml
    html = html.replace("__TABLE__", tablehtml)

    html = templates.final_replace(html, "../..")
    util.writefile("../timeline/" + year + "/country.html", html)

if __name__ == "__main__":
    run(sys.argv[1])
