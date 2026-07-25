from database_countries import countries
from database_participants import participants_by_code
from database_participants import count_medals
from database_participants import Medal
from database_timeline import editions_hosted_by
from templates import render_fragment
from templates import render_page

def run():
  print("Generating countries/index")

  tablehtml = ""
  for country in countries:
    hosts = ", ".join(
      render_fragment("countries/index_hostyear", year=edition.year)
      for edition in editions_hosted_by(country)
    )

    medals = count_medals(participants_by_code.get(country.code, []))

    if country.website:
      national_site = country.website
      national_site_text = country.website if len(country.website) < 50 else country.website[0:35] + "..."
      national_site_style = ""
    else:
      national_site = "."
      national_site_text = ""
      national_site_style = "display: none;"

    tablehtml += render_fragment(
      "countries/index_row",
      code=country.code,
      country=country.name,
      hosts=hosts,
      gold=str(medals[Medal.GOLD]),
      silver=str(medals[Medal.SILVER]),
      bronze=str(medals[Medal.BRONZE]),
      honourable=str(medals[Medal.HONOURABLE]),
      css_class="tr-former" if country.former else "",
      national_site=national_site,
      national_site_text=national_site_text,
      national_site_style=national_site_style,
    )

  render_page("countries/index", table=tablehtml)

if __name__ == "__main__":
  run()
