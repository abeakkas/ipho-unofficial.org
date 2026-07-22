import sys
import templates
import util
from database_countries import code_indexed as countries_by_code
from database_countries import previous_code
from database_countries import next_code
from database_participants import code_grouped as participants_by_code
from templates import render

def run(code):
  print("Generating countries/" + code + "/individual")

  if code in previous_code:
    previous_code_value = previous_code[code]
    previous_code_style = ""
  else:
    previous_code_value = "." # Google crawler fix
    previous_code_style = "display: none;"

  if code in next_code:
    next_code_value = next_code[code]
    next_code_style = ""
  else:
    next_code_value = "." # Google crawler fix
    next_code_style = "display: none;"

  tablehtml = ""
  if code in participants_by_code:
    yearhtml = ""
    lastyear = ""
    for participant in participants_by_code[code]:
      if participant.website:
        name = render(
          "timeline/year/individual_participant_link",
          root="../..",
          link=participant.website,
          name=participant.name,
        )
      else:
        name = participant.name

      rowhtml = render(
        "countries/code/individual_row",
        root="../..",
        name=name,
        rank=("&ge;" if participant.rank_geq else "") + participant.rank,
        year=participant.year,
        medal=templates.medal(participant.medal, root="../.."),
        css_class="" if lastyear == participant.year else "doubleTopLine",
      )
      if lastyear == participant.year:
        yearhtml += rowhtml
      else:
        lastyear = participant.year
        # reverse ordered:
        tablehtml = yearhtml + tablehtml
        yearhtml = rowhtml
    # Hacky way of removing first double top line:
    yearhtml = yearhtml.replace("doubleTopLine", "", 1)
    tablehtml = yearhtml + tablehtml

  html = render(
    "countries/code/individual",
    root="../..",
    code=code,
    country=countries_by_code[code].country,
    previous_code=previous_code_value,
    previous_code_style=previous_code_style,
    next_code=next_code_value,
    next_code_style=next_code_style,
    table=tablehtml,
  )
  util.writefile("../countries/" + code + "/individual.html", html)


if __name__ == "__main__":
  run(sys.argv[1])
