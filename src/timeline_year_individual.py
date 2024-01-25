import sys
import templates
import util
from database_countries import code_to_country
from database_students import year_grouped as s_db_y
from database_timeline import year_indexed as t_db_y
from database_timeline import previous_year
from database_timeline import next_year

def run(year):
    print("Generating timeline/" + year + "/individual")
    html = templates.get("timeline/year/individual")
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

    show_points = year in s_db_y and s_db_y[year] and s_db_y[year][0].theoretical

    if show_points:
        html = html.replace("__POINTS_STYLE__", "")
    else:
        html = html.replace("__POINTS_STYLE__", "display: none;")

    tablehtml = ""
    if year in s_db_y:
        for row in s_db_y[year]:
            rowhtml = templates.get("timeline/year/individual_row")
            if row.code == "":
                rowhtml = rowhtml.replace("__CODE__", "TUR") # Yup, this is my hack
                rowhtml = rowhtml.replace("__COUNTRY__", "")
            else:
                rowhtml = rowhtml.replace("__CODE__", row.code)
                rowhtml = rowhtml.replace("__COUNTRY__", code_to_country[row.code])
            if row.website:
                link = templates.get("timeline/year/individual_student_link")
                link = link.replace("__LINK__", row.website)
                link = link.replace("__NAME__", row.name)
                rowhtml = rowhtml.replace("__NAME__", link)
            else:
                rowhtml = rowhtml.replace("__NAME__", row.name)
            rowhtml = rowhtml.replace("__RANK__", ("&ge;" if row.rank_geq else "") + row.rank)
            rowhtml = rowhtml.replace("__MEDAL__", templates.medal[row.medal])
            if show_points:
                rowhtml = rowhtml.replace("__POINTS_STYLE__", "")
                rowhtml = rowhtml.replace("__THEORETICAL__", row.theoretical)
                rowhtml = rowhtml.replace("__EXPERIMENTAL__", row.experimental)
                rowhtml = rowhtml.replace("__TOTAL__", row.total)
            else:
                rowhtml = rowhtml.replace("__POINTS_STYLE__", "display: none;")
            tablehtml += rowhtml
        html = html.replace("__NOTE__", "")
    else:
        html = html.replace("__NOTE__", "Results will be added once they are published on the official website.<br>")
    html = html.replace("__TABLE__", tablehtml)

    html = templates.finalize(html, "../..")
    util.writefile("../timeline/" + year + "/individual.html", html)

if __name__ == "__main__":
    run(sys.argv[1])
