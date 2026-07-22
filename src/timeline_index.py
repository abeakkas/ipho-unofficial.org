import util
from database_countries import code_to_country
from database_participants import next_year
from database_timeline import database as editions
from templates import render

def monospace_date(date):
  if "-" not in date:
    return date
  if len(date.split("-")[0]) == 4:
    date = "&nbsp;" + date
  if len(date.split("-")[1]) == 4:
    date = date + "&nbsp;"
  return date

def run():
  print("Generating timeline/index")

  tablehtml = ""
  upcominghtml = ""
  upcoming_row_ctr = 0
  for row in editions:
    if row.code2:
      code2 = row.code2
      country2 = code_to_country[row.code2]
      code2_style = ""
    else:
      code2 = "." # Google crawler fix
      country2 = ""
      code2_style = "display: none;"

    rowhtml = render(
      "timeline/index_row",
      root="..",
      number=row.number,
      year=row.year,
      date=monospace_date(row.date),
      code=row.code,
      city=row.city,
      country=code_to_country[row.code],
      p_country=row.p_country,
      p_participant=row.p_participant,
      code2=code2,
      country2=country2,
      code2_style=code2_style,
    )

    if int(row.year) <= int(next_year) + 2:
      # Reverse list
      tablehtml = rowhtml + tablehtml
    else:
      upcominghtml = rowhtml + upcominghtml
      upcoming_row_ctr += 1
    # IPhO 2020 was a special event and is not listed in timeline database.
    if int(row.year) == 2019:
      tablehtml = render("timeline/index_row_2020", root="..") + tablehtml

  # Append an empty row to preserve row parity between tables for styling purposes
  if upcoming_row_ctr % 2:
    upcominghtml = "<tr style=\"display:none;\"></tr>" + upcominghtml

  html = render(
    "timeline/index",
    root="..",
    table=tablehtml,
    upcoming=upcominghtml,
  )
  util.writefile("../timeline/index.html", html)

if __name__ == "__main__":
  run()

