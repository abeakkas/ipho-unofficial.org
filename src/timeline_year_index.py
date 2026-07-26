import os
import sys
from database_timeline import editions_by_year
from database_timeline import year_before
from database_timeline import year_after
from database_participants import participants_by_year
from database_participants import count_medals
from database_participants import Medal
from templates import render_page

def run(year):
  print(f"Generating timeline/{year}/index")
  edition = editions_by_year[year]

  if edition.host2:
    code2 = edition.host2.code
    country2 = edition.host2.name
    code2_style = ""
  else:
    code2 = "."
    country2 = ""
    code2_style = "display: none;"

  city = edition.city + "," if edition.city else ""

  if year in year_before:
    previous_year = year_before[year]
    previous_year_style = ""
  else:
    previous_year = "."
    previous_year_style = "display: none;"

  if year in year_after:
    next_year = year_after[year]
    next_year_style = ""
  else:
    next_year = "."
    next_year_style = "display: none;"

  if edition.participant_count:
    participant_count = edition.participant_count
    participant_count_style = ""
  else:
    participant_count = ""
    participant_count_style = "display: none;"

  if edition.country_count:
    country_count = edition.country_count
    country_count_style = ""
  else:
    country_count = ""
    country_count_style = "display: none;"

  if edition.homepage:
    homepage = edition.homepage
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
    number=edition.number,
    ordinal=edition.ordinal,
    date=edition.date,
    code=edition.host.code,
    country=edition.host.name,
    code2=code2,
    country2=country2,
    code2_style=code2_style,
    city=city,
    previous_year=previous_year,
    previous_year_style=previous_year_style,
    next_year=next_year,
    next_year_style=next_year_style,
    participant_count=participant_count,
    participant_count_style=participant_count_style,
    country_count=country_count,
    country_count_style=country_count_style,
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
