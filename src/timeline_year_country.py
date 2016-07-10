#!/usr/bin/python
import sys
import util
import templates
from database_countries import code_to_country
from database_students import year_grouped as s_db_y
from database_timeline import year_indexed as t_db_y
from database_timeline import previous_year
from database_timeline import next_year

def run(year):
    print "Creating timeline/" + year + "/country"
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
        
    if year in next_year:
        html = html.replace("__NEXT_YEAR__", next_year[year])
        html = html.replace("__NEXT_YEAR_STYLE__", "")
    else:
        html = html.replace("__NEXT_YEAR_STYLE__", "display: none;")
    
    medals = {}
    _gold = 10000000000
    _silver = 100000000
    _bronze = 1000000
    _honourable = 10000
    if year in s_db_y:
        for row in s_db_y[year]:
            if row["code"] not in medals:
                # This assures countries with same medals are sorted by their best student
                rank = int(row["rank"]) if row["rank"][0] != ">" else int(row["rank"][2:])
                medals[row["code"]] = _honourable - rank
            if row["medal"] == "1":
                medals[row["code"]] += _gold
            elif row["medal"] == "2":
                medals[row["code"]] += _silver
            elif row["medal"] == "3":
                medals[row["code"]] += _bronze
            elif row["medal"] == "4":
                medals[row["code"]] += _honourable
    
    msort = sorted(medals, key = medals.get)[::-1]
    
    tablehtml = ""
    for i in range(len(msort)):
        rowhtml = templates.get("timeline/year/country_row")
        rowhtml = rowhtml.replace("__CODE__", msort[i])
        rowhtml = rowhtml.replace("__COUNTRY__", code_to_country[msort[i]])
        rowhtml = rowhtml.replace("__RANK__", str(i + 1))
        rowhtml = rowhtml.replace("__GOLD__", str(medals[msort[i]] / _gold))
        rowhtml = rowhtml.replace("__SILVER__", str(medals[msort[i]] / _silver % 100))
        rowhtml = rowhtml.replace("__BRONZE__", str(medals[msort[i]] / _bronze % 100))
        rowhtml = rowhtml.replace("__HONOURABLE__", str(medals[msort[i]] / _honourable % 100))
        tablehtml += rowhtml
    html = html.replace("__TABLE__", tablehtml)
    
    html = templates.final_replace(html, "../..")
    util.writefile("../timeline/" + year + "/country.html", html)
    
if __name__ == "__main__":
    run(sys.argv[1])