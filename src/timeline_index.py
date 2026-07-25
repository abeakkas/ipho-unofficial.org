from database_participants import next_year
from database_timeline import database as editions
from templates import render_fragment
from templates import render_page

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
  for edition in editions:
    if edition.host2:
      code2 = edition.host2.code
      country2 = edition.host2.name
      code2_style = ""
    else:
      code2 = "."
      country2 = ""
      code2_style = "display: none;"

    rowhtml = render_fragment(
      "timeline/index_row",
      number=edition.number,
      year=edition.year,
      date=monospace_date(edition.date),
      code=edition.host.code,
      city=edition.city,
      country=edition.host.name,
      p_country=edition.p_country,
      p_participant=edition.p_participant,
      code2=code2,
      country2=country2,
      code2_style=code2_style,
    )

    if int(edition.year) <= int(next_year) + 2:
      # Reverse list
      tablehtml = rowhtml + tablehtml
    else:
      upcominghtml = rowhtml + upcominghtml
      upcoming_row_ctr += 1
    # IPhO 2020 was a special event and is not listed in timeline database.
    if int(edition.year) == 2019:
      tablehtml = render_fragment("timeline/index_row_2020") + tablehtml

  # Append an empty row to preserve row parity between tables for styling purposes
  if upcoming_row_ctr % 2:
    upcominghtml = "<tr style=\"display:none;\"></tr>" + upcominghtml

  render_page(
    "timeline/index",
    table=tablehtml,
    upcoming=upcominghtml,
  )

if __name__ == "__main__":
  run()

