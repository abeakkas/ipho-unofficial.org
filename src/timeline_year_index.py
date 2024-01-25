import sys
import templates
import util
from database_timeline import year_indexed as t_db_y
from database_timeline import previous_year
from database_timeline import next_year
from database_countries import code_to_country
from database_students import year_grouped as s_db_y

def run(year):
    print("Generating timeline/" + year + "/index")
    html = templates.get("timeline/year/index")
    html = templates.set_headers(html, "timeline")
    yeardata = t_db_y[year]
    html = html.replace("__YEAR__", year)
    html = html.replace("__NUMBER__", yeardata.number)
    html = html.replace("__ORDINAL__", util.ordinal(yeardata.number))
    html = html.replace("__DATE__", yeardata.date)
    html = html.replace("__CODE__", yeardata.code)
    html = html.replace("__COUNTRY__", code_to_country[yeardata.code])

    if yeardata.code2:
        html = html.replace("__CODE2__", yeardata.code2)
        html = html.replace("__COUNTRY2__", code_to_country[yeardata.code2])
        html = html.replace("__CODE2_STYLE__", "")
    else:
        html = html.replace("__CODE2_STYLE__", "display: none;")
        html = html.replace("__CODE2__", ".") # Google crawler fix

    if yeardata.city:
        html = html.replace("__CITY__", yeardata.city + ",")
    else:
        html = html.replace("__CITY__", "")

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

    if yeardata.p_student:
        html = html.replace("__P_STUDENT_STYLE__", "")
        html = html.replace("__P_STUDENT__", yeardata.p_student)
    else:
        html = html.replace("__P_STUDENT_STYLE__", "display: none;")

    if yeardata.p_country:
        html = html.replace("__P_COUNTRY_STYLE__", "")
        html = html.replace("__P_COUNTRY__", yeardata.p_country)
    else:
        html = html.replace("__P_COUNTRY_STYLE__", "display: none;")

    if yeardata.homepage:
        html = html.replace("__HOMEPAGE_STYLE__", "")
        html = html.replace("__HOMEPAGE__", yeardata.homepage)
    else:
        html = html.replace("__HOMEPAGE_STYLE__", "display: none;")
        html = html.replace("__HOMEPAGE__", ".") # Google crawler fix

    if year in s_db_y:
        medals = {"G": 0, "S": 0, "B": 0, "H": 0, "P": 0}
        for studentdata in s_db_y[year]:
            medals[studentdata.medal] += 1
        html = html.replace("__AWARDS_STYLE__", "")
        html = html.replace("__GOLD__", str(medals["G"]))
        html = html.replace("__SILVER__", str(medals["S"]))
        html = html.replace("__BRONZE__", str(medals["B"]))
        html = html.replace("__HONOURABLE__", str(medals["H"]))
    else:
        html = html.replace("__AWARDS_STYLE__", "display: none;")

    html = templates.finalize(html, "../..")
    util.writefile("../timeline/" + year + "/index.html", html)

if __name__ == "__main__":
    run(sys.argv[1])
