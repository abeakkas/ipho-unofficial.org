import sys
import templates
from database_participants import year_grouped as participants_by_year
from database_timeline import year_indexed as editions_by_year
from database_timeline import get_previous_year
from database_timeline import get_next_year
from templates import render_fragment
from templates import render_page

def run(year):
  print(f"Generating timeline/{year}/individual")
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

  show_points = year in participants_by_year and participants_by_year[year] and participants_by_year[year][0].theoretical
  points_style = "" if show_points else "display: none;"

  if year in participants_by_year:
    tablehtml = ""
    for participant in participants_by_year[year]:
      code = participant.country.code
      country = participant.country.name

      if participant.website:
        name = render_fragment(
          "timeline/year/individual_participant_link",
          link=participant.website,
          name=participant.name,
        )
      else:
        name = participant.name

      if show_points:
        row_points_style = ""
        theoretical = participant.theoretical
        experimental = participant.experimental
        total = participant.total
      else:
        row_points_style = "display: none;"
        theoretical = ""
        experimental = ""
        total = ""

      tablehtml += render_fragment(
        "timeline/year/individual_row",
        code=code,
        country=country,
        name=name,
        rank=("&ge;" if participant.rank_geq else "") + participant.rank,
        medal=templates.medal(participant.medal),
        points_style=row_points_style,
        theoretical=theoretical,
        experimental=experimental,
        total=total,
      )
  else:
    tablehtml = "<tr><td colspan=4>Results will be added once they are published on the official website.</td></tr>"

  render_page(
    "timeline/year/individual",
    year=year,
    number=yeardata.number,
    ordinal=yeardata.ordinal,
    previous_year=previous_year,
    previous_year_style=previous_year_style,
    next_year=next_year,
    next_year_style=next_year_style,
    points_style=points_style,
    table=tablehtml,
  )

if __name__ == "__main__":
  run(sys.argv[1])
