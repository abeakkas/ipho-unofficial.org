import sys
import templates
import util
from database_countries import code_to_country
from database_participants import year_grouped as participants_by_year
from database_timeline import year_indexed as editions_by_year
from database_timeline import get_previous_year
from database_timeline import get_next_year
from templates import render

def run(year):
  print("Generating timeline/" + year + "/individual")
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
    for row in participants_by_year[year]:
      if row.code == "":
        # Unknown country: filler code keeps the link path valid; name is hidden.
        code = "TUR"
        country = ""
      else:
        code = row.code
        country = code_to_country[row.code]

      if row.website:
        name = render(
          "timeline/year/individual_participant_link",
          root="../..",
          link=row.website,
          name=row.name,
        )
      else:
        name = row.name

      if show_points:
        row_points_style = ""
        theoretical = row.theoretical
        experimental = row.experimental
        total = row.total
      else:
        row_points_style = "display: none;"
        theoretical = ""
        experimental = ""
        total = ""

      tablehtml += render(
        "timeline/year/individual_row",
        root="../..",
        code=code,
        country=country,
        name=name,
        rank=("&ge;" if row.rank_geq else "") + row.rank,
        medal=templates.medal(row.medal, root="../.."),
        points_style=row_points_style,
        theoretical=theoretical,
        experimental=experimental,
        total=total,
      )
  else:
    tablehtml = "<tr><td colspan=4>Results will be added once they are published on the official website.</td></tr>"

  html = render(
    "timeline/year/individual",
    root="../..",
    year=year,
    number=yeardata.number,
    ordinal=util.ordinal(yeardata.number),
    previous_year=previous_year,
    previous_year_style=previous_year_style,
    next_year=next_year,
    next_year_style=next_year_style,
    points_style=points_style,
    table=tablehtml,
  )
  util.writefile("../timeline/" + year + "/individual.html", html)

if __name__ == "__main__":
  run(sys.argv[1])
