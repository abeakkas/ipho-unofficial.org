import sys
from collections import defaultdict
from database_countries import code_to_country
from database_participants import year_grouped as participants_by_year
from database_participants import count_medals
from database_participants import Medal
from database_timeline import year_indexed as editions_by_year
from database_timeline import get_previous_year
from database_timeline import get_next_year
from templates import render_fragment
from templates import render_page

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
    by_code = defaultdict(list)
    for participant in participants_by_year[year]:
      if participant.code == "":
        continue
      by_code[participant.code].append(participant)
    medals = {code: count_medals(participants) for code, participants in by_code.items()}

  def keyfn(code):
    m = medals[code]
    return (-m[Medal.GOLD], -m[Medal.SILVER], -m[Medal.BRONZE], -m[Medal.HONOURABLE], code)

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
      tablehtml += render_fragment(
        "timeline/year/country_row",
        code=code,
        country=code_to_country[code],
        rank=rank,
        gold=str(medals[code][Medal.GOLD]),
        silver=str(medals[code][Medal.SILVER]),
        bronze=str(medals[code][Medal.BRONZE]),
        honourable=str(medals[code][Medal.HONOURABLE]),
      )

  render_page(
    "timeline/year/country",
    "../timeline/" + year + "/country.html",
    year=year,
    number=yeardata.number,
    ordinal=yeardata.ordinal,
    previous_year=previous_year,
    previous_year_style=previous_year_style,
    next_year=next_year,
    next_year_style=next_year_style,
    table=tablehtml,
  )

if __name__ == "__main__":
  run(sys.argv[1])
