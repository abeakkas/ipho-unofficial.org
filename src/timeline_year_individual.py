import sys
import templates
import util
from database_countries import code_to_country
from database_participants import year_grouped as participants_by_year
from database_timeline import year_indexed as editions_by_year
from database_timeline import get_previous_year
from database_timeline import get_next_year

def run(year):
  print("Generating timeline/" + year + "/individual")
  html = templates.get("timeline/year/individual")
  html = templates.set_headers(html, "timeline")
  yeardata = editions_by_year[year]
  html = html.replace("__YEAR__", year)
  html = html.replace("__NUMBER__", yeardata.number)
  html = html.replace("__ORDINAL__", util.ordinal(yeardata.number))

  if year in get_previous_year:
    html = html.replace("__PREVIOUS_YEAR__", get_previous_year[year])
    html = html.replace("__PREVIOUS_YEAR_STYLE__", "")
  else:
    html = html.replace("__PREVIOUS_YEAR_STYLE__", "display: none;")
    html = html.replace("__PREVIOUS_YEAR__", ".") # Google crawler fix

  if year in get_next_year:
    html = html.replace("__NEXT_YEAR__", get_next_year[year])
    html = html.replace("__NEXT_YEAR_STYLE__", "")
  else:
    html = html.replace("__NEXT_YEAR_STYLE__", "display: none;")
    html = html.replace("__NEXT_YEAR__", ".") # Google crawler fix

  show_points = year in participants_by_year and participants_by_year[year] and participants_by_year[year][0].theoretical

  if show_points:
    html = html.replace("__POINTS_STYLE__", "")
  else:
    html = html.replace("__POINTS_STYLE__", "display: none;")

  tablehtml = ""
  if year in participants_by_year:
    for row in participants_by_year[year]:
      rowhtml = templates.get("timeline/year/individual_row")
      if row.code == "":
        # Unknown country: filler code keeps the link path valid; name is hidden.
        rowhtml = rowhtml.replace("__CODE__", "TUR")
        rowhtml = rowhtml.replace("__COUNTRY__", "")
      else:
        rowhtml = rowhtml.replace("__CODE__", row.code)
        rowhtml = rowhtml.replace("__COUNTRY__", code_to_country[row.code])
      if row.website:
        link = templates.get("timeline/year/individual_participant_link")
        link = link.replace("__LINK__", row.website)
        link = link.replace("__NAME__", row.name)
        rowhtml = rowhtml.replace("__NAME__", link)
      else:
        rowhtml = rowhtml.replace("__NAME__", row.name)
      rowhtml = rowhtml.replace("__RANK__", ("&ge;" if row.rank_geq else "") + row.rank)
      rowhtml = rowhtml.replace("__MEDAL__", templates.medal[row.medal])
      if show_points:
        rowhtml = rowhtml.replace("__POINTS_STYLE__", "")
        rowhtml = rowhtml.replace("__THEORETICAL__", row.theoretical)
        rowhtml = rowhtml.replace("__EXPERIMENTAL__", row.experimental)
        rowhtml = rowhtml.replace("__TOTAL__", row.total)
      else:
        rowhtml = rowhtml.replace("__POINTS_STYLE__", "display: none;")
      tablehtml += rowhtml
  else:
    tablehtml = "<tr><td colspan=4>Results will be added once they are published on the official website.</td></tr>"
  html = html.replace("__TABLE__", tablehtml)

  html = templates.finalize(html, "../..")
  util.writefile("../timeline/" + year + "/individual.html", html)

if __name__ == "__main__":
  run(sys.argv[1])
