import sys
import templates
from collections import defaultdict
from database_countries import code_indexed as countries_by_code
from database_countries import previous_code
from database_countries import next_code
from database_participants import code_grouped as participants_by_code
from templates import render_fragment
from templates import render_page

def run(code):
  print("Generating countries/" + code + "/individual")

  if code in previous_code:
    previous_code_value = previous_code[code]
    previous_code_style = ""
  else:
    previous_code_value = "." # Google crawler fix
    previous_code_style = "display: none;"

  if code in next_code:
    next_code_value = next_code[code]
    next_code_style = ""
  else:
    next_code_value = "." # Google crawler fix
    next_code_style = "display: none;"

  # participants.csv is ordered by ascending year then rank.
  # Group rows by year then display newest year first.
  groups = defaultdict(list)
  for participant in participants_by_code.get(code, []):
    groups[participant.year].append(participant)

  tablehtml = ""
  for year in reversed(groups):
    for i, participant in enumerate(groups[year]):
      if participant.website:
        name = render_fragment(
          "timeline/year/individual_participant_link",
          link=participant.website,
          name=participant.name,
        )
      else:
        name = participant.name

      # Divider above each year group except the topmost one.
      divider = i == 0 and tablehtml != ""
      tablehtml += render_fragment(
        "countries/code/individual_row",
        name=name,
        rank=("&ge;" if participant.rank_geq else "") + participant.rank,
        year=year,
        medal=templates.medal(participant.medal),
        css_class="doubleTopLine" if divider else "",
      )

  render_page(
    "countries/code/individual",
    code=code,
    country=countries_by_code[code].country,
    previous_code=previous_code_value,
    previous_code_style=previous_code_style,
    next_code=next_code_value,
    next_code_style=next_code_style,
    table=tablehtml,
  )


if __name__ == "__main__":
  run(sys.argv[1])
