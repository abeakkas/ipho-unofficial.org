import os
import sys
from database_timeline import editions_by_year
from database_timeline import get_previous_year
from database_timeline import get_next_year
from database_participants import participants_by_year
from database_participants import count_medals
from database_participants import Medal
from templates import render_page

def run(year):
  print(f"Generating timeline/{year}/index")
  yeardata = editions_by_year[year]

  if yeardata.host2:
    code2 = yeardata.host2.code
    country2 = yeardata.host2.name
    code2_style = ""
  else:
    code2 = "."
    country2 = ""
    code2_style = "display: none;"

  city = yeardata.city + "," if yeardata.city else ""

  if year in get_previous_year:
    previous_year = get_previous_year[year]
    previous_year_style = ""
  else:
    previous_year = "."
    previous_year_style = "display: none;"

  if year in get_next_year:
    next_year = get_next_year[year]
    next_year_style = ""
  else:
    next_year = "."
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
    homepage = "."
    homepage_style = "display: none;"

  if os.path.exists(f"templates/minutes/{year}.pdf"):
    minutes_style = ""
  else:
    minutes_style = "display: none;"

  if year in participants_by_year:
    medals = count_medals(participants_by_year[year])
    awards_style = ""
    gold = medals[Medal.GOLD]
    silver = medals[Medal.SILVER]
    bronze = medals[Medal.BRONZE]
    honourable = medals[Medal.HONOURABLE]
  else:
    awards_style = "display: none;"
    gold = ""
    silver = ""
    bronze = ""
    honourable = ""

  render_page(
    "timeline/year/index",
    year=year,
    number=yeardata.number,
    ordinal=yeardata.ordinal,
    date=yeardata.date,
    code=yeardata.host.code,
    country=yeardata.host.name,
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

if __name__ == "__main__":
  run(int(sys.argv[1]))
