import sys
import templates
import util
from database_countries import code_indexed as countries_by_code
from database_countries import previous_code
from database_countries import next_code
from database_participants import code_grouped as participants_by_code

def run(code):
  print("Generating countries/" + code + "/individual")
  html = templates.get("countries/code/individual")
  html = templates.set_headers(html, "countries")

  html = html.replace("__CODE__", code)
  html = html.replace("__COUNTRY__", countries_by_code[code].country)

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
  if code in participants_by_code:
    yearhtml = ""
    lastyear = ""
    for participant in participants_by_code[code]:
      rowhtml = templates.get("countries/code/individual_row")
      if participant.website:
        link = templates.get("timeline/year/individual_participant_link")
        link = link.replace("__LINK__", participant.website)
        link = link.replace("__NAME__", participant.name)
        rowhtml = rowhtml.replace("__NAME__", link)
      else:
        rowhtml = rowhtml.replace("__NAME__", participant.name)
      rowhtml = rowhtml.replace("__RANK__", ("&ge;" if participant.rank_geq else "") + participant.rank)
      rowhtml = rowhtml.replace("__YEAR__", participant.year)
      rowhtml = rowhtml.replace("__MEDAL__", templates.medal[participant.medal])
      if lastyear == participant.year:
        rowhtml = rowhtml.replace("__CLASS__", "")
        yearhtml += rowhtml
      else:
        lastyear = participant.year
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
