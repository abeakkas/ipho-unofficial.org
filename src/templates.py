import config
import os
import util
from functools import cache
from database_participants import last_year
from database_participants import next_year
from database_timeline import year_indexed as editions_by_year

@cache
def get(path):
  """
  Load HTML from file and return as string
  """
  return util.readfile("templates/" + path + ".html")

def set_headers(html, type):
  """
  Fill header and footer in given template string
  type is one of ["homepage", "timeline", "countries", "search", "hall_of_fame", ""]
  """
  if type == "homepage":
    html = html.replace("__HEADER_TOP__", get("header_top"))
  else:
    side = get("header_side")
    side = side.replace("__HIGHLIGHT_{}__".format(type.upper()), "highlight")
    side = side.replace("__HIGHLIGHT_TIMELINE__", "")
    side = side.replace("__HIGHLIGHT_COUNTRIES__", "")
    side = side.replace("__HIGHLIGHT_SEARCH__", "")
    side = side.replace("__HIGHLIGHT_HALL_OF_FAME__", "")
    html = html.replace("__HEADER_SIDE__", side)
  html = html.replace("__HEADER_PREVIOUS_YEAR__", last_year)
  html = html.replace("__HEADER_PREVIOUS_YEAR_HOMEPAGE__", editions_by_year[last_year].homepage)
  html = html.replace("__HEADER_NEXT_YEAR__", next_year)
  html = html.replace("__HEADER_NEXT_YEAR_HOMEPAGE__", editions_by_year[next_year].homepage)
  html = html.replace("__FOOTER__", get("footer"))
  return html

def finalize(html, root):
  """
  Fill URL templates
  root is the relative path of the root directory of website
  See the setting config.github
  """
  html = html.replace("__ROOT__", root)
  if config.github:
    html = html.replace("__INDEX__", ".")
    html = html.replace("__HTML_EXT__", "")
  else:
    html = html.replace("__INDEX__", "index.html")
    html = html.replace("__HTML_EXT__", ".html")
  html = html.replace("__WEBMASTER__", config.webmaster_email)
  return html

def hasminutes(year):
  return os.path.exists(f"templates/minutes/{year}.pdf")

medal = {
  "G": get("medal_gold"),
  "S": get("medal_silver"),
  "B": get("medal_bronze"),
  "H": get("medal_honourable"),
  "P": "",
}

