import sys
import util
from database_countries import code_to_country
from database_participants import year_grouped as participants_by_year
from database_timeline import year_indexed as editions_by_year
from database_timeline import get_previous_year
from database_timeline import get_next_year
from templates import render

def run(year):
  print("Generating timeline/" + year + "/country")
  yeardata = editions_by_year[year]

  if year in get_previous_year:
    previous_year = get_previous_year[year]
    previous_year_style = ""
  else:
    previous_year = "." # Google crawler fix
    previous_year_style = "display: none;"

  if year in get_next_year:
    next_year = get_next_year[year]
    next_year_style = ""
  else:
    next_year = "." # Google crawler fix
    next_year_style = "display: none;"

  medals = {}
  if year in participants_by_year:
    for row in participants_by_year[year]:
      if row.code == "":
        continue
      if row.code not in medals:
        medals[row.code] = {"G": 0, "S": 0, "B": 0, "H": 0, "P": 0}
      medals[row.code][row.medal] += 1

  def keyfn(code):
    m = medals[code]
    return (-m["G"], -m["S"], -m["B"], -m["H"], code)

  sortedcodes = sorted(medals, key = keyfn)

  if year not in participants_by_year:
    tablehtml = "<tr><td colspan=6>Results will be added once they are published on the official website.</td></tr>"
  else:
    tablehtml = ""
    prevcode = ""
    prevrank = 0
    for i, code in enumerate(sortedcodes):
      if prevcode != "" and keyfn(prevcode)[:-1] == keyfn(code)[:-1]:
        rank = prevrank
      else:
        rank = str(i + 1)
        prevcode = code
        prevrank = str(i + 1)
      tablehtml += render(
        "timeline/year/country_row",
        root="../..",
        code=code,
        country=code_to_country[code],
        rank=rank,
        gold=str(medals[code]["G"]),
        silver=str(medals[code]["S"]),
        bronze=str(medals[code]["B"]),
        honourable=str(medals[code]["H"]),
      )

  html = render(
    "timeline/year/country",
    root="../..",
    year=year,
    number=yeardata.number,
    ordinal=util.ordinal(yeardata.number),
    previous_year=previous_year,
    previous_year_style=previous_year_style,
    next_year=next_year,
    next_year_style=next_year_style,
    table=tablehtml,
  )
  util.writefile("../timeline/" + year + "/country.html", html)

if __name__ == "__main__":
  run(sys.argv[1])
