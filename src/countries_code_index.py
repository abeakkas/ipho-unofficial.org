import sys
from database_countries import code_to_country
from database_countries import code_before
from database_countries import code_after
from database_participants import participants_by_code
from database_participants import count_medals
from database_participants import Medal
from database_timeline import editions_hosted_by
from templates import render_fragment
from templates import render_page

def run(code):
  print(f"Generating countries/{code}/index")
  country = code_to_country[code]

  if country.website != "":
    contact_style = ""
    national_site = country.website
    national_site_text = country.website if len(country.website) < 50 else country.website[0:50] + "..."
  else:
    contact_style = "display: none;"
    national_site = "."
    national_site_text = ""

  if code in code_before:
    previous_code = code_before[code]
    previous_code_style = ""
  else:
    previous_code = "."
    previous_code_style = "display: none;"

  if code in code_after:
    next_code_value = code_after[code]
    next_code_style = ""
  else:
    next_code_value = "."
    next_code_style = "display: none;"

  hostshtml = ""
  for edition in editions_hosted_by(country):
    if edition.homepage:
      homepagehtml = render_fragment(
        "countries/code/index_host_homepage",
        link=edition.homepage,
        year=edition.year,
      )
    else:
      homepagehtml = ""
    hostshtml += render_fragment(
      "countries/code/index_host",
      city=" - " + edition.city if edition.city else "",
      homepage=homepagehtml,
      year=edition.year,
    )
  if hostshtml:
    hostshtml = "<dt>IPhO Host</dt>" + hostshtml

  medals = count_medals(participants_by_code.get(code, []))

  render_page(
    "countries/code/index",
    code=code,
    country=country.name,
    contact_style=contact_style,
    national_site=national_site,
    national_site_text=national_site_text,
    previous_code=previous_code,
    previous_code_style=previous_code_style,
    next_code=next_code_value,
    next_code_style=next_code_style,
    host=hostshtml,
    gold=medals[Medal.GOLD],
    silver=medals[Medal.SILVER],
    bronze=medals[Medal.BRONZE],
    honourable=medals[Medal.HONOURABLE],
  )

if __name__ == "__main__":
  run(sys.argv[1])
