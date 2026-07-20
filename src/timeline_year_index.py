import sys
import templates
import util
from database_timeline import year_indexed as editions_by_year
from database_timeline import get_previous_year
from database_timeline import get_next_year
from database_countries import code_to_country
from database_participants import year_grouped as participants_by_year
from database_participants import count_medals

def run(year):
  print("Generating timeline/" + year + "/index")
  html = templates.get("timeline/year/index")
  html = templates.set_headers(html, "timeline")
  yeardata = editions_by_year[year]
  html = html.replace("__YEAR__", year)
  html = html.replace("__NUMBER__", yeardata.number)
  html = html.replace("__ORDINAL__", util.ordinal(yeardata.number))
  html = html.replace("__DATE__", yeardata.date)
  html = html.replace("__CODE__", yeardata.code)
  html = html.replace("__COUNTRY__", code_to_country[yeardata.code])

  if yeardata.code2:
    html = html.replace("__CODE2__", yeardata.code2)
    html = html.replace("__COUNTRY2__", code_to_country[yeardata.code2])
    html = html.replace("__CODE2_STYLE__", "")
  else:
    html = html.replace("__CODE2_STYLE__", "display: none;")
    html = html.replace("__CODE2__", ".") # Google crawler fix

  if yeardata.city:
    html = html.replace("__CITY__", yeardata.city + ",")
  else:
    html = html.replace("__CITY__", "")

  if year in get_previous_year:
    html = html.replace("__PREVIOUS_YEAR__", get_previous_year[year])
    html = html.replace("__PREVIOUS_YEAR_STYLE__", "")
  else:
    html = html.replace("__PREVIOUS_YEAR_STYLE__", "display: none;")
    html = html.replace("__PREVIOUS_YEAR__", ".") # Google crawler fix

  if year in get_next_year:
    html = html.replace("__NEXT_YEAR__", get_next_year[year])
    html = html.replace("__NEXT_YEAR_STYLE__", "")
  else:
    html = html.replace("__NEXT_YEAR_STYLE__", "display: none;")
    html = html.replace("__NEXT_YEAR__", ".") # Google crawler fix

  if yeardata.p_participant:
    html = html.replace("__P_PARTICIPANT_STYLE__", "")
    html = html.replace("__P_PARTICIPANT__", yeardata.p_participant)
  else:
    html = html.replace("__P_PARTICIPANT_STYLE__", "display: none;")
    html = html.replace("__P_PARTICIPANT__", "")

  if yeardata.p_country:
    html = html.replace("__P_COUNTRY_STYLE__", "")
    html = html.replace("__P_COUNTRY__", yeardata.p_country)
  else:
    html = html.replace("__P_COUNTRY_STYLE__", "display: none;")
    html = html.replace("__P_COUNTRY__", "")

  if yeardata.homepage:
    html = html.replace("__HOMEPAGE_STYLE__", "")
    html = html.replace("__HOMEPAGE__", yeardata.homepage)
  else:
    html = html.replace("__HOMEPAGE_STYLE__", "display: none;")
    html = html.replace("__HOMEPAGE__", ".") # Google crawler fix

  if templates.hasminutes(year):
    html = html.replace("__MINUTES_STYLE__", "")
  else:
    html = html.replace("__MINUTES_STYLE__", "display: none;")


  if year in participants_by_year:
    medals = count_medals(participants_by_year[year])
    html = html.replace("__AWARDS_STYLE__", "")
    html = html.replace("__GOLD__", str(medals["G"]))
    html = html.replace("__SILVER__", str(medals["S"]))
    html = html.replace("__BRONZE__", str(medals["B"]))
    html = html.replace("__HONOURABLE__", str(medals["H"]))
  else:
    html = html.replace("__AWARDS_STYLE__", "display: none;")
    html = html.replace("__GOLD__", "")
    html = html.replace("__SILVER__", "")
    html = html.replace("__BRONZE__", "")
    html = html.replace("__HONOURABLE__", "")

  html = templates.finalize(html, "../..")
  util.writefile("../timeline/" + year + "/index.html", html)

if __name__ == "__main__":
  run(sys.argv[1])
