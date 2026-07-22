import templates
import util
from database_countries import code_to_country
from database_2020 import database

def run():
  print("Generating timeline/2020")
  util.makedirs("../timeline/2020")
  html = templates.get("timeline/2020/index")
  html = templates.set_headers(html, "timeline")

  tablehtml = ""
  for participant in database:
    rowhtml = templates.get("timeline/year/individual_row")
    rowhtml = rowhtml.replace("__CODE__", participant.code)
    rowhtml = rowhtml.replace("__COUNTRY__", code_to_country[participant.code])
    if participant.website:
      link = templates.get("timeline/year/individual_participant_link")
      link = link.replace("__LINK__", participant.website)
      link = link.replace("__NAME__", participant.name)
      rowhtml = rowhtml.replace("__NAME__", link)
    else:
      rowhtml = rowhtml.replace("__NAME__", participant.name)
    rowhtml = rowhtml.replace("__RANK__", participant.rank)
    rowhtml = rowhtml.replace("__MEDAL__", templates.medal[participant.medal])
    rowhtml = rowhtml.replace("__POINTS_STYLE__", "display: none;")
    tablehtml += rowhtml
  html = html.replace("__TABLE__", tablehtml)

  html = templates.finalize(html, "../..")
  util.writefile("../timeline/2020/index.html", html)

if __name__ == "__main__":
  run()

