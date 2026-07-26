import sys
from database_participants import participants_by_year
from database_timeline import editions_by_year
from database_timeline import year_before
from database_timeline import year_after
from templates import medal_fragment
from templates import render_fragment
from templates import render_page

def run(year):
  print(f"Generating timeline/{year}/individual")
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
        medal=medal_fragment(participant.medal),
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
    number=edition.number,
    ordinal=edition.ordinal,
    previous_year=previous_year,
    previous_year_style=previous_year_style,
    next_year=next_year,
    next_year_style=next_year_style,
    points_style=points_style,
    table=tablehtml,
  )

if __name__ == "__main__":
  run(int(sys.argv[1]))
