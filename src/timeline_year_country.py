import sys
import templates
import util
from database_countries import code_to_country
from database_students import year_grouped as s_db_y
from database_timeline import year_indexed as t_db_y
from database_timeline import previous_year
from database_timeline import next_year

def run(year):
    print("Generating timeline/" + year + "/country")
    html = templates.get("timeline/year/country")
    html = templates.set_headers(html, "timeline")
    yeardata = t_db_y[year]
    html = html.replace("__YEAR__", year)
    html = html.replace("__NUMBER__", yeardata.number)
    html = html.replace("__ORDINAL__", util.ordinal(yeardata.number))

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
            if row.code == "":
                continue
            if row.code not in medals:
                medals[row.code] = {"G": 0, "S": 0, "B": 0, "H": 0, "P": 0}
            medals[row.code][row.medal] += 1
        html = html.replace("__NOTE__", "")
    else:
        html = html.replace("__NOTE__", "Results will be added once they are published on the official website.<br>")

    def keyfn(code):
        m = medals[code]
        return (-m["G"], -m["S"], -m["B"], -m["H"], code)

    sortedcodes = sorted(medals, key = keyfn)

    tablehtml = ""
    prevcode = ""
    prevrank = 0
    for i, code in enumerate(sortedcodes):
        rowhtml = templates.get("timeline/year/country_row")
        rowhtml = rowhtml.replace("__CODE__", code)
        rowhtml = rowhtml.replace("__COUNTRY__", code_to_country[code])
        if prevcode != "" and keyfn(prevcode)[:-1] == keyfn(code)[:-1]:
            rowhtml = rowhtml.replace("__RANK__", prevrank)
        else:
            rowhtml = rowhtml.replace("__RANK__", str(i + 1))
            prevcode = code
            prevrank = str(i + 1)
        rowhtml = rowhtml.replace("__GOLD__", str(medals[code]["G"]))
        rowhtml = rowhtml.replace("__SILVER__", str(medals[code]["S"]))
        rowhtml = rowhtml.replace("__BRONZE__", str(medals[code]["B"]))
        rowhtml = rowhtml.replace("__HONOURABLE__", str(medals[code]["H"]))
        tablehtml += rowhtml
    html = html.replace("__TABLE__", tablehtml)

    html = templates.finalize(html, "../..")
    util.writefile("../timeline/" + year + "/country.html", html)

if __name__ == "__main__":
    run(sys.argv[1])
