from database_countries import code_to_country
from database_countries import database as countries
from database_participants import code_grouped as participants_by_code
from database_participants import count_medals
from database_participants import Medal
from database_timeline import code_grouped as editions_by_code
from templates import render_fragment
from templates import render_page

def run():
  print("Generating countries/index")

  tablehtml = ""
  for row in countries:
    if row.code in editions_by_code:
      hosts = ", ".join(
        render_fragment("countries/index_hostyear", year=year.year)
        for year in editions_by_code[row.code]
      )
    else:
      hosts = ""

    medals = count_medals(participants_by_code.get(row.code, []))

    if row.website:
      national_site = row.website
      national_site_text = row.website if len(row.website) < 50 else row.website[0:35] + "..."
      national_site_style = ""
    else:
      national_site = "." # Google crawler fix
      national_site_text = ""
      national_site_style = "display: none;"

    tablehtml += render_fragment(
      "countries/index_row",
      code=row.code,
      country=code_to_country[row.code],
      hosts=hosts,
      gold=str(medals[Medal.GOLD]),
      silver=str(medals[Medal.SILVER]),
      bronze=str(medals[Medal.BRONZE]),
      honourable=str(medals[Medal.HONOURABLE]),
      css_class="tr-former" if row.former else "",
      national_site=national_site,
      national_site_text=national_site_text,
      national_site_style=national_site_style,
    )

  render_page("countries/index", table=tablehtml)

if __name__ == "__main__":
  run()
