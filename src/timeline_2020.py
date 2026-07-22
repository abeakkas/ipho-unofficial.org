import templates
import util
from database_countries import code_to_country
from database_2020 import database
from templates import render

def run():
  print("Generating timeline/2020")
  util.makedirs("../timeline/2020")

  tablehtml = ""
  for participant in database:
    if participant.website:
      name = render(
        "timeline/year/individual_participant_link",
        root="../..",
        link=participant.website,
        name=participant.name,
      )
    else:
      name = participant.name

    tablehtml += render(
      "timeline/year/individual_row",
      root="../..",
      code=participant.code,
      country=code_to_country[participant.code],
      name=name,
      rank=participant.rank,
      medal=templates.medal(participant.medal, root="../.."),
      points_style="display: none;",
      theoretical="",
      experimental="",
      total="",
    )

  html = render(
    "timeline/2020/index",
    root="../..",
    table=tablehtml,
  )
  util.writefile("../timeline/2020/index.html", html)

if __name__ == "__main__":
  run()

