#!/usr/bin/python
import sys
import util
import templates
from database_timeline import year_indexed as t_db_y
from database_timeline import previous_year
from database_timeline import next_year
from database_countries import code_to_country

def run(year):
    print "Creating timeline/" + year + "/index"
    html = templates.get("timeline/year/index")
    html = templates.initial_replace(html, 1)
    yeardata = t_db_y[year]
    html = html.replace("__YEAR__", year)
    html = html.replace("__NUMBER__", yeardata["number"])
    html = html.replace("__ORDINAL__", util.ordinal(yeardata["number"]))
    html = html.replace("__DATE__", yeardata["date"])
    html = html.replace("__CODE__", yeardata["code"])
    html = html.replace("__COUNTRY__", code_to_country[yeardata["code"]])
    
    if yeardata["city"] != "":
        html = html.replace("__CITY__", yeardata["city"] + ", ")
    else:
        html = html.replace("__CITY__", "")
    
    if year in previous_year:
        html = html.replace("__PREVIOUS_YEAR__", previous_year[year])
        html = html.replace("__PREVIOUS_YEAR_STYLE__", "")
    else:
        html = html.replace("__PREVIOUS_YEAR_STYLE__", "display: none;")
        
    if year in next_year:
        html = html.replace("__NEXT_YEAR__", next_year[year])
        html = html.replace("__NEXT_YEAR_STYLE__", "")
    else:
        html = html.replace("__NEXT_YEAR_STYLE__", "display: none;")
    
    if yeardata["p_student"] != "":
        html = html.replace("__P_STUDENT_STYLE__", "")
        html = html.replace("__P_STUDENT__", yeardata["p_student"])
    else:
        html = html.replace("__P_STUDENT_STYLE__", "display: none;")
    
    if yeardata["p_country"] != "":
        html = html.replace("__P_COUNTRY_STYLE__", "")
        html = html.replace("__P_COUNTRY__", yeardata["p_country"])
    else:
        html = html.replace("__P_COUNTRY_STYLE__", "display: none;")
    
    if yeardata["homepage"] != "":
        html = html.replace("__HOMEPAGE_STYLE__", "")
        html = html.replace("__HOMEPAGE__", yeardata["homepage"])
    else:
        html = html.replace("__HOMEPAGE_STYLE__", "display: none;")
    
    if yeardata["gold"] != "":
        html = html.replace("__AWARDS_STYLE__", "")
        html = html.replace("__GOLD__", yeardata["gold"])
        html = html.replace("__SILVER__", yeardata["silver"])
        html = html.replace("__BRONZE__", yeardata["bronze"])
        html = html.replace("__HONOURABLE__", yeardata["honourable"])
    else:
        html = html.replace("__AWARDS_STYLE__", "display: none;")
    
    html = templates.final_replace(html, "../..")
    util.writefile("../timeline/" + year + "/index.html", html)
    
if __name__ == "__main__":
    run(sys.argv[1])