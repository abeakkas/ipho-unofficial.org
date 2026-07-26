import sys
from collections import defaultdict
from database_participants import participants_by_year
from database_participants import count_medals
from database_participants import Medal
from database_timeline import editions_by_year
from database_timeline import year_before
from database_timeline import year_after
from templates import render_fragment
from templates import render_page

def run(year):
  print(f"Generating timeline/{year}/country")
  edition = editions_by_year[year]

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

  medals = {}
  if year in participants_by_year:
    by_country = defaultdict(list)
    for participant in participants_by_year[year]:
      by_country[participant.country].append(participant)
    medals = {country: count_medals(participants) for country, participants in by_country.items()}

  def keyfn(country):
    m = medals[country]
    return (-m[Medal.GOLD], -m[Medal.SILVER], -m[Medal.BRONZE], -m[Medal.HONOURABLE], country.code)

  sortedcountries = sorted(medals, key = keyfn)

  if year not in participants_by_year:
    tablehtml = "<tr><td colspan=6>Results will be added once they are published on the official website.</td></tr>"
  else:
    tablehtml = ""
    prevcountry = None
    prevrank = 0
    for i, country in enumerate(sortedcountries):
      if prevcountry is not None and keyfn(prevcountry)[:-1] == keyfn(country)[:-1]:
        rank = prevrank
      else:
        rank = str(i + 1)
        prevcountry = country
        prevrank = str(i + 1)
      tablehtml += render_fragment(
        "timeline/year/country_row",
        code=country.code,
        country=country.name,
        rank=rank,
        gold=medals[country][Medal.GOLD],
        silver=medals[country][Medal.SILVER],
        bronze=medals[country][Medal.BRONZE],
        honourable=medals[country][Medal.HONOURABLE],
      )

  render_page(
    "timeline/year/country",
    year=year,
    number=edition.number,
    ordinal=edition.ordinal,
    previous_year=previous_year,
    previous_year_style=previous_year_style,
    next_year=next_year,
    next_year_style=next_year_style,
    table=tablehtml,
  )

if __name__ == "__main__":
  run(int(sys.argv[1]))
