from database_2020 import participants
from templates import medal_fragment
from templates import render_fragment
from templates import render_page

def run():
  print("Generating timeline/2020")

  tablehtml = ""
  for participant in participants:
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
      code=participant.country.code,
      country=participant.country.name,
      name=name,
      rank=participant.rank,
      medal=medal_fragment(participant.medal),
      points_style="display: none;",
      theoretical="",
      experimental="",
      total="",
    )

  render_page(
    "timeline/2020/index",
    table=tablehtml,
  )

if __name__ == "__main__":
  run()

