import sys
from database_countries import code_indexed as countries_by_code
from database_countries import previous_code
from database_countries import next_code
from database_participants import code_grouped as participants_by_code
from database_participants import count_medals
from database_participants import Medal
from database_timeline import code_grouped as editions_by_code
from templates import render_fragment
from templates import render_page

def run(code):
  print("Generating countries/" + code + "/index")
  codedata = countries_by_code[code]

  if codedata.website != "":
    contact_style = ""
    national_site = codedata.website
    national_site_text = codedata.website if len(codedata.website) < 50 else codedata.website[0:50] + "..."
  else:
    contact_style = "display: none;"
    national_site = "." # Google crawler fix
    national_site_text = ""

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

  if code in editions_by_code:
    hostshtml = ""
    for yeardata in editions_by_code[code]:
      if yeardata.homepage:
        homepagehtml = render_fragment(
          "countries/code/index_host_homepage",
          link=yeardata.homepage,
          year=yeardata.year,
        )
      else:
        homepagehtml = ""
      hostshtml += render_fragment(
        "countries/code/index_host",
        city=" - " + yeardata.city if yeardata.city else "",
        homepage=homepagehtml,
        year=yeardata.year,
      )
    host = "<dt>IPhO Host</dt>" + hostshtml
  else:
    host = ""

  medals = count_medals(participants_by_code.get(code, []))

  render_page(
    "countries/code/index",
    "../countries/" + code + "/index.html",
    code=code,
    country=codedata.country,
    contact_style=contact_style,
    national_site=national_site,
    national_site_text=national_site_text,
    previous_code=previous_code_value,
    previous_code_style=previous_code_style,
    next_code=next_code_value,
    next_code_style=next_code_style,
    host=host,
    gold=str(medals[Medal.GOLD]),
    silver=str(medals[Medal.SILVER]),
    bronze=str(medals[Medal.BRONZE]),
    honourable=str(medals[Medal.HONOURABLE]),
  )

if __name__ == "__main__":
  run(sys.argv[1])
