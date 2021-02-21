import util
import templates
from database_2020 import database
from database_countries import code_to_country
from database_timeline import year_indexed as t_db_y

def run():
    print("Creating timeline/2020")
    util.makedirs("../timeline/2020")
    html = templates.get("timeline/2020/index")
    html = templates.initial_replace(html, 1)

    tablehtml = ""
    for row in database:
        rowhtml = templates.get("timeline/year/individual_row")
        rowhtml = rowhtml.replace("__CODE__", row["code"])
        rowhtml = rowhtml.replace("__COUNTRY__", code_to_country[row["code"]])
        rowhtml = rowhtml.replace("__NAME__", row["name"])
        rowhtml = rowhtml.replace("__RANK__", row["rank"])
        if row["medal"] == "G":
            rowhtml = rowhtml.replace("__MEDAL__", templates.get("timeline/year/individual_gold"))
        elif row["medal"] == "S":
            rowhtml = rowhtml.replace("__MEDAL__", templates.get("timeline/year/individual_silver"))
        elif row["medal"] == "B":
            rowhtml = rowhtml.replace("__MEDAL__", templates.get("timeline/year/individual_bronze"))
        elif row["medal"] == "H":
            rowhtml = rowhtml.replace("__MEDAL__", templates.get("timeline/year/individual_honourable"))
        else:
            rowhtml = rowhtml.replace("__MEDAL__", "")
        tablehtml += rowhtml
    html = html.replace("__TABLE__", tablehtml)

    html = templates.final_replace(html, "../..")
    util.writefile("../timeline/2020/index.html", html)

if __name__ == "__main__":
    run()
