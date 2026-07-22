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
  homepage has its own inline header (no sidebar), so the header_side splice
  below is a no-op for it (no ${header_side} placeholder to replace).
  """
  side = get("header_side")
  side = side.replace(f"${{highlight_{type}}}", "highlight")
  side = side.replace("${highlight_timeline}", "")
  side = side.replace("${highlight_countries}", "")
  side = side.replace("${highlight_search}", "")
  side = side.replace("${highlight_hall_of_fame}", "")
  html = html.replace("${header_side}", side)
  html = html.replace("${header_previous_year}", last_year)
  html = html.replace("${header_previous_year_homepage}", editions_by_year[last_year].homepage)
  html = html.replace("${header_next_year}", next_year)
  html = html.replace("${header_next_year_homepage}", editions_by_year[next_year].homepage)
  html = html.replace("${footer}", get("footer"))
  return html

def finalize(html, root):
  """
  Fill URL templates
  root is the relative path of the root directory of website
  See the setting config.github
  """
  html = html.replace("${root}", root)
  if config.github:
    html = html.replace("${index}", ".")
    html = html.replace("${html_ext}", "")
  else:
    html = html.replace("${index}", "index.html")
    html = html.replace("${html_ext}", ".html")
  html = html.replace("${webmaster}", config.webmaster_email)
  return html

def render(path, *, root, section=None, **values):
  """
  Render a template to final HTML.
  Fills chrome (when section is given), body values, then URL/root tokens.
  Transitional: templates use ${token} syntax, but still filled via replace; will switch to string.Template.substitute.
  """
  html = get(path)
  if section is not None:
    html = set_headers(html, section)
  for key, value in values.items():
    html = html.replace(f"${{{key}}}", value)
  html = finalize(html, root)
  return html

def hasminutes(year):
  return os.path.exists(f"templates/minutes/{year}.pdf")

medal = {
  "G": util.readfile("templates/medal_gold.html"),
  "S": util.readfile("templates/medal_silver.html"),
  "B": util.readfile("templates/medal_bronze.html"),
  "H": util.readfile("templates/medal_honourable.html"),
  "P": "",
}

