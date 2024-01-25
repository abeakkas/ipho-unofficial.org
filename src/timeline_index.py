import config
import templates
import util
from database_countries import code_to_country
from database_timeline import database as t_db

def monospace_date(date):
    if "-" not in date:
        return date
    if len(date.split("-")[0]) == 4:
        date = "&nbsp;" + date
    if len(date.split("-")[1]) == 4:
        # date = date.replace("-", "-&nbsp;")
        date = date + "&nbsp;"
    return date

def run():
    print("Generating timeline/index")
    html = templates.get("timeline/index")
    html = templates.set_headers(html, "timeline")

    tablehtml = ""
    upcominghtml = ""
    upcoming_row_ctr = 0
    for row in t_db:
        rowhtml = templates.get("timeline/index_row")
        rowhtml = rowhtml.replace("__NUMBER__", row.number)
        rowhtml = rowhtml.replace("__YEAR__", row.year)
        rowhtml = rowhtml.replace("__DATE__", monospace_date(row.date))
        rowhtml = rowhtml.replace("__CODE__", row.code)
        rowhtml = rowhtml.replace("__CITY__", row.city)
        rowhtml = rowhtml.replace("__COUNTRY__", code_to_country[row.code])
        rowhtml = rowhtml.replace("__P_COUNTRY__", row.p_country)
        rowhtml = rowhtml.replace("__P_STUDENT__", row.p_student)
        if row.code2:
            rowhtml = rowhtml.replace("__CODE2__", row.code2)
            rowhtml = rowhtml.replace("__COUNTRY2__", code_to_country[row.code2])
            rowhtml = rowhtml.replace("__CODE2_STYLE__", "")
        else:
            rowhtml = rowhtml.replace("__CODE2_STYLE__", "display: none;")
            rowhtml = rowhtml.replace("__CODE2__", ".") # Google crawler fix
        if int(row.year) <= int(config.next_year) + 2:
            # Reverse list
            tablehtml = rowhtml + tablehtml
        else:
            upcominghtml = rowhtml + upcominghtml
            upcoming_row_ctr += 1
        if int(row.year) == 2019:
            tablehtml = templates.get("timeline/index_row_2020") + tablehtml

    # Append an empty row to preserve row parity between tables for styling purposes
    if upcoming_row_ctr % 2:
        upcominghtml = "<tr style=\"display:none;\"></tr>" + upcominghtml

    html = html.replace("__TABLE__", tablehtml)
    html = html.replace("__UPCOMING__", upcominghtml)

    html = templates.finalize(html, "..")
    util.writefile("../timeline/index.html", html)

if __name__ == "__main__":
    run()
