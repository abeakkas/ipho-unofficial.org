#!/usr/bin/python
import util
import templates
from database_countries import code_to_country
from database_timeline import database as t_db

def run():
    print "Creating timeline/index"
    html = templates.get("timeline/index")
    html = templates.initial_replace(html, 1)
    
    tablehtml = ""
    for row in t_db:
        rowhtml = templates.get("timeline/index_row")
        rowhtml = rowhtml.replace("__NUMBER__", row["number"])
        rowhtml = rowhtml.replace("__YEAR__", row["year"])
        rowhtml = rowhtml.replace("__DATE__", row["date"])
        rowhtml = rowhtml.replace("__CODE__", row["code"])
        rowhtml = rowhtml.replace("__CITY__", row["city"])
        rowhtml = rowhtml.replace("__COUNTRY__", code_to_country[row["code"]])
        rowhtml = rowhtml.replace("__P_COUNTRY__", row["p_country"])
        rowhtml = rowhtml.replace("__P_STUDENT__", row["p_student"])
        if "code2" in row:
            rowhtml = rowhtml.replace("__CODE2__", row["code2"])
            rowhtml = rowhtml.replace("__COUNTRY2__", code_to_country[row["code2"]])
            rowhtml = rowhtml.replace("__CODE2_STYLE__", "")
        else:
            rowhtml = rowhtml.replace("__CODE2_STYLE__", "display: none;")
        # Reverse list
        tablehtml = rowhtml + tablehtml
    html = html.replace("__TABLE__", tablehtml)
    
    html = templates.final_replace(html, "..")
    util.writefile("../timeline/index.html", html)
    
if __name__ == "__main__":
    run()