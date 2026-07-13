import templates
import util
from database_countries import code_to_country
from database_countries import database as countries
from database_participants import code_grouped as participants_by_code
from database_timeline import code_grouped as editions_by_code

def run():
  print("Generating countries/index")
  html = templates.get("countries/index")
  html = templates.set_headers(html, "countries")

  tablehtml = ""
  for row in countries:
    rowhtml = templates.get("countries/index_row")
    rowhtml = rowhtml.replace("__CODE__", row.code)
    rowhtml = rowhtml.replace("__COUNTRY__", code_to_country[row.code])

    if row.website:
      rowhtml = rowhtml.replace("__NATIONAL_SITE__", row.website)
      if len(row.website) < 50:
        rowhtml = rowhtml.replace("__NATIONAL_SITE_TEXT__", row.website)
      else:
        rowhtml = rowhtml.replace("__NATIONAL_SITE_TEXT__", row.website[0:35] + "...")
      rowhtml = rowhtml.replace("__NATIONAL_SITE_STYLE__", "")
    else:
      rowhtml = rowhtml.replace("__NATIONAL_SITE_STYLE__", "display: none;")

    if row.code in editions_by_code:
      hosts = ""
      flag = False
      for year in editions_by_code[row.code]:
        if flag:
          hosts += ", "
        hosts += templates.get("countries/index_hostyear").replace("__YEAR__", year.year)
        flag = True
      rowhtml = rowhtml.replace("__HOSTS__", hosts)
    else:
      rowhtml = rowhtml.replace("__HOSTS__", "")

    medals = {"G": 0, "S": 0, "B": 0, "H": 0, "P": 0}
    if row.code in participants_by_code:
      for participant in participants_by_code[row.code]:
        medals[participant.medal] += 1
    rowhtml = rowhtml.replace("__GOLD__", str(medals["G"]))
    rowhtml = rowhtml.replace("__SILVER__", str(medals["S"]))
    rowhtml = rowhtml.replace("__BRONZE__", str(medals["B"]))
    rowhtml = rowhtml.replace("__HONOURABLE__", str(medals["H"]))

    rowhtml = rowhtml.replace("__CLASS__", "tr-former" if row.former else "")

    tablehtml += rowhtml
  html = html.replace("__TABLE__", tablehtml)

  html = templates.finalize(html, "..")
  util.writefile("../countries/index.html", html)

if __name__ == "__main__":
  run()
