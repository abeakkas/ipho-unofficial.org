import templates
import util
from asciify import asciify
from collections import defaultdict
from database_countries import code_to_country
from database_participants import code_grouped as participants_by_code
from database_participants import count_medals
from database_participants import Medal

# Identities that algorithm can't find
identity_overrides = [
  (("2010", "SVK", "Eugen Hruska"), ("2011", "GER", "Eugen Hruska")),
]

def _find_recurring_participations():
  """Simple union-find to find participants with multiple appearences."""
  participant_bin = {}

  def merge(participant1, participant2):
    participant_bin.setdefault(participant1, [participant1])
    participant_bin.setdefault(participant2, [participant2])
    if participant_bin[participant1] is participant_bin[participant2]:
      return
    participant_bin[participant1].extend(participant_bin[participant2])
    for participant in participant_bin[participant2]:
      participant_bin[participant] = participant_bin[participant1]

  def is_similar(participant1, participant2):
    name1 = asciify(participant1.name).replace("-", " ").split(" ")
    name2 = asciify(participant2.name).replace("-", " ").split(" ")
    # Check if a name can be found in the name
    return all(s in name2 for s in name1) or all(s in name1 for s in name2)

  # For each country compare participants from each year with two previous years
  for code_rows in participants_by_code.values():
     years = defaultdict(list)
     for row in code_rows:
       years[int(row.year)].append(row)
     for year, rows in years.items():
       for row1 in rows:
         for y in range(year - 2, year):
           if y not in years:
             continue
           for row2 in years[y]:
             if is_similar(row1, row2):
               merge(row2, row1)

  for (year1, code1, name1), (year2, code2, name2) in identity_overrides:
    row1 = row2 = None
    for row in participants_by_code[code1]:
      if row.year == year1 and row.name == name1:
        row1 = row
    for row in participants_by_code[code2]:
      if row.year == year2 and row.name == name2:
        row2 = row
    if not row1 or not row2:
      raise Exception(f"Hall of fame exception not found: {(year1, code1, name1)} / {(year2, code2, name2)}")
    merge(row1, row2)

  # Return unique lists.
  return list({id(bin): bin for bin in participant_bin.values()}.values())

def _print_bin(bin, medals):
  rowhtml = templates.get("hall_of_fame/index_row")
  rowhtml = rowhtml.replace("__NAME__", bin[0].name)
  rowhtml = rowhtml.replace("__CODE__", bin[0].code)
  rowhtml = rowhtml.replace("__COUNTRY__", code_to_country[bin[0].code])

  rowhtml = rowhtml.replace("__GOLD__", str(medals[Medal.GOLD]))
  rowhtml = rowhtml.replace("__SILVER__", str(medals[Medal.SILVER]))
  rowhtml = rowhtml.replace("__BRONZE__", str(medals[Medal.BRONZE]))
  rowhtml = rowhtml.replace("__HONOURABLE__", str(medals[Medal.HONOURABLE]))

  participations = ""
  for row in sorted(bin, key=lambda row: row.year):
    if participations:
      participations += ", "
    year_html = templates.get("hall_of_fame/index_participation_year").strip()
    year_html = year_html.replace("__YEAR__", row.year)
    if row.code == bin[0].code:
      year_html = year_html.replace("__YEAR_TEXT__", row.year)
    else:
      year_html = year_html.replace("__YEAR_TEXT__", "{}({})".format(row.year, row.code))
    year_html = year_html.replace("__TITLE__", "Appeared as " + row.name)
    participations += year_html

  return rowhtml.replace("__PARTICIPATIONS__", participations)

def run():
  print("Generating hall_of_fame")

  bins = _find_recurring_participations()

  # Sort by medal quality, best is first
  def quality(bin):
    medals = count_medals(bin)
    return (
      -medals[Medal.GOLD],
      -medals[Medal.SILVER],
      -medals[Medal.BRONZE],
      -medals[Medal.HONOURABLE],
      bin[0].year,
      bin[0].name,
    )
  bins = sorted(bins, key=quality)

  html = templates.get("hall_of_fame/index")
  html = templates.set_headers(html, "hall_of_fame")

  tablehtml = ""
  i = 0
  while i < len(bins):
    medals = count_medals(bins[i])
    # Cutoff at 1 gold, 1 silver, 1 bronze
    if medals[Medal.GOLD] < 2 and medals[Medal.SILVER] < 2 and medals[Medal.BRONZE] < 1:
      break
    tablehtml += _print_bin(bins[i], medals)
    i += 1
  bins = bins[i:]

  html = html.replace("__TABLE__", tablehtml)

  # Sort by total number of medals, best is first
  def quantity(bin):
    medals = count_medals(bin)
    return (
      -(medals[Medal.GOLD] + medals[Medal.SILVER] + medals[Medal.BRONZE]),
      -medals[Medal.GOLD],
      -medals[Medal.SILVER],
      -medals[Medal.BRONZE],
      -medals[Medal.HONOURABLE],
      bin[0].year,
      bin[0].name,
    )
  bins = sorted(bins, key=quantity)

  table2html = ""
  i = 0
  while i < len(bins):
    medals = count_medals(bins[i])
    # Cutoff at 3 medals
    if medals[Medal.GOLD] + medals[Medal.SILVER] + medals[Medal.BRONZE] < 3:
      break
    table2html += _print_bin(bins[i], medals)
    i += 1

  html = html.replace("__TABLE2__", table2html)

  html = templates.finalize(html, "..")

  # Apparently Google recommends dashes over underscores :/
  util.makedirs("../hall-of-fame")
  util.writefile("../hall-of-fame/index.html", html)

if __name__ == "__main__":
  run()

