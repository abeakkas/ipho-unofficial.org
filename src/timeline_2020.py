import templates
import util
from database_countries import code_to_country
from database_2020 import database
from templates import render_fragment
from templates import render_page

def run():
  print("Generating timeline/2020")
  util.makedirs("../timeline/2020")

  tablehtml = ""
  for participant in database:
    if participant.website:
      name = render_fragment(
        "timeline/year/individual_participant_link",
        link=participant.website,
        name=participant.name,
      )
    else:
      name = participant.name

    tablehtml += render_fragment(
      "timeline/year/individual_row",
      code=participant.code,
      country=code_to_country[participant.code],
      name=name,
      rank=participant.rank,
      medal=templates.medal(participant.medal),
      points_style="display: none;",
      theoretical="",
      experimental="",
      total="",
    )

  render_page(
    "timeline/2020/index",
    "../timeline/2020/index.html",
    table=tablehtml,
  )

if __name__ == "__main__":
  run()

