#!/usr/bin/python
import util
import templates
from database_countries import database as c_db
from database_countries import code_to_country
from database_timeline import code_grouped as t_db_c

def run():
    print "Creating countries/index"
    html = templates.get("countries/index")
    html = templates.initial_replace(html, 2)
    
    tablehtml = ""
    for row in c_db:
        rowhtml = templates.get("countries/index_row")
        rowhtml = rowhtml.replace("__CODE__", row["code"])
        rowhtml = rowhtml.replace("__COUNTRY__", code_to_country[row["code"]])
        
        if row["website"] != "":
            rowhtml = rowhtml.replace("__NATIONAL_SITE__", row["website"])
            if len(row["website"]) < 50:
                rowhtml = rowhtml.replace("__NATIONAL_SITE_TEXT__", row["website"])
            else:
                rowhtml = rowhtml.replace("__NATIONAL_SITE_TEXT__", row["website"][0:50] + "...")
            rowhtml = rowhtml.replace("__NATIONAL_SITE_STYLE__", "")
        else:
            rowhtml = rowhtml.replace("__NATIONAL_SITE_STYLE__", "display: none;")
        
        if row["code"] in t_db_c:
            hosts = ""
            flag = False
            for year in t_db_c[row["code"]]:
                if flag:
                    hosts += ", "
                hosts += templates.get("countries/index_hostyear").replace("__YEAR__", year["year"])
                flag = True
            rowhtml = rowhtml.replace("__HOSTS__", hosts)
        else:
            rowhtml = rowhtml.replace("__HOSTS__", "")
        
        tablehtml += rowhtml
    html = html.replace("__TABLE__", tablehtml)
    
    html = templates.final_replace(html, "..")
    util.writefile("../countries/index.html", html)
    
if __name__ == "__main__":
    run()