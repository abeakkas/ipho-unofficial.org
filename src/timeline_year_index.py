import sys
import templates
import util
from database_timeline import year_indexed as editions_by_year
from database_timeline import get_previous_year
from database_timeline import get_next_year
from database_countries import code_to_country
from database_participants import year_grouped as participants_by_year
from database_participants import count_medals
from templates import render

def run(year):
  print("Generating timeline/" + year + "/index")
  yeardata = editions_by_year[year]

  if yeardata.code2:
    code2 = yeardata.code2
    country2 = code_to_country[yeardata.code2]
    code2_style = ""
  else:
    code2 = "." # Google crawler fix
    country2 = ""
    code2_style = "display: none;"

  city = yeardata.city + "," if yeardata.city else ""

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

  if yeardata.p_participant:
    p_participant = yeardata.p_participant
    p_participant_style = ""
  else:
    p_participant = ""
    p_participant_style = "display: none;"

  if yeardata.p_country:
    p_country = yeardata.p_country
    p_country_style = ""
  else:
    p_country = ""
    p_country_style = "display: none;"

  if yeardata.homepage:
    homepage = yeardata.homepage
    homepage_style = ""
  else:
    homepage = "." # Google crawler fix
    homepage_style = "display: none;"

  minutes_style = "" if templates.hasminutes(year) else "display: none;"

  if year in participants_by_year:
    medals = count_medals(participants_by_year[year])
    awards_style = ""
    gold = str(medals["G"])
    silver = str(medals["S"])
    bronze = str(medals["B"])
    honourable = str(medals["H"])
  else:
    awards_style = "display: none;"
    gold = ""
    silver = ""
    bronze = ""
    honourable = ""

  html = render(
    "timeline/year/index",
    root="../..",
    section="timeline",
    year=year,
    number=yeardata.number,
    ordinal=util.ordinal(yeardata.number),
    date=yeardata.date,
    code=yeardata.code,
    country=code_to_country[yeardata.code],
    code2=code2,
    country2=country2,
    code2_style=code2_style,
    city=city,
    previous_year=previous_year,
    previous_year_style=previous_year_style,
    next_year=next_year,
    next_year_style=next_year_style,
    p_participant=p_participant,
    p_participant_style=p_participant_style,
    p_country=p_country,
    p_country_style=p_country_style,
    homepage=homepage,
    homepage_style=homepage_style,
    minutes_style=minutes_style,
    awards_style=awards_style,
    gold=gold,
    silver=silver,
    bronze=bronze,
    honourable=honourable,
  )
  util.writefile("../timeline/" + year + "/index.html", html)

if __name__ == "__main__":
  run(sys.argv[1])
