import sys
import templates
import util
from database_countries import code_indexed as c_db_c
from database_countries import previous_code
from database_countries import next_code
from database_students import code_grouped as s_db_c

def run(code):
    print("Generating countries/" + code + "/individual")
    html = templates.get("countries/code/individual")
    html = templates.set_headers(html, "countries")

    html = html.replace("__CODE__", code)
    html = html.replace("__COUNTRY__", c_db_c[code].country)

    if code in previous_code:
        html = html.replace("__PREVIOUS_CODE__", previous_code[code])
        html = html.replace("__PREVIOUS_CODE_STYLE__", "")
    else:
        html = html.replace("__PREVIOUS_CODE_STYLE__", "display: none;")
        html = html.replace("__PREVIOUS_CODE__", ".") # Google crawler fix

    if code in next_code:
        html = html.replace("__NEXT_CODE__", next_code[code])
        html = html.replace("__NEXT_CODE_STYLE__", "")
    else:
        html = html.replace("__NEXT_CODE_STYLE__", "display: none;")
        html = html.replace("__NEXT_CODE__", ".") # Google crawler fix

    tablehtml = ""
    if code in s_db_c:
        yearhtml = ""
        lastyear = ""
        for studentdata in s_db_c[code]:
            rowhtml = templates.get("countries/code/individual_row")
            if studentdata.website:
                link = templates.get("timeline/year/individual_student_link")
                link = link.replace("__LINK__", studentdata.website)
                link = link.replace("__NAME__", studentdata.name)
                rowhtml = rowhtml.replace("__NAME__", link)
            else:
                rowhtml = rowhtml.replace("__NAME__", studentdata.name)
            rowhtml = rowhtml.replace("__RANK__", ("&ge;" if studentdata.rank_geq else "") + studentdata.rank)
            rowhtml = rowhtml.replace("__YEAR__", studentdata.year)
            rowhtml = rowhtml.replace("__MEDAL__", templates.medal[studentdata.medal])
            if lastyear == studentdata.year:
                rowhtml = rowhtml.replace("__CLASS__", "")
                yearhtml += rowhtml
            else:
                lastyear = studentdata.year
                # reverse ordered:
                tablehtml = yearhtml + tablehtml
                rowhtml = rowhtml.replace("__CLASS__", "doubleTopLine")
                yearhtml = rowhtml
        # Hacky way of removing first double top line:
        yearhtml = yearhtml.replace("doubleTopLine", "", 1)
        tablehtml = yearhtml + tablehtml

    html = html.replace("__TABLE__", tablehtml)
    html = templates.finalize(html, "../..")
    util.writefile("../countries/" + code + "/individual.html", html)


if __name__ == "__main__":
    run(sys.argv[1])
