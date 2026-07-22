import config
import os
import util
from functools import cache
from string import Template
from database_participants import last_year
from database_participants import next_year
from database_participants import Medal
from database_timeline import year_indexed as editions_by_year

@cache
def _load(path, root):
  """
  Load HTML from file and resolve root/index/html_ext/webmaster substitutions.
  """
  html = util.readfile("templates/" + path + ".html")
  return Template(html).safe_substitute(
    root=root,
    index="." if config.github else "index.html",
    html_ext="" if config.github else ".html",
    webmaster=config.webmaster_email,
  )

def _fill_header_footer(html, root, path):
  """
  Fill header/footer. Nav highlight comes from path's first segment.
  """
  section = path.split("/")[0]
  side = Template(_load("header_side", root)).substitute(
    highlight_timeline="highlight" if section == "timeline" else "",
    highlight_countries="highlight" if section == "countries" else "",
    highlight_search="highlight" if section == "search" else "",
    highlight_hall_of_fame="highlight" if section == "hall_of_fame" else "",
    header_previous_year=last_year,
    header_previous_year_homepage=editions_by_year[last_year].homepage,
    header_next_year=next_year,
    header_next_year_homepage=editions_by_year[next_year].homepage,
  )

  return Template(html).safe_substitute(
    header_side=side,
    header_previous_year=last_year,
    header_previous_year_homepage=editions_by_year[last_year].homepage,
    header_next_year=next_year,
    header_next_year_homepage=editions_by_year[next_year].homepage,
    footer=_load("footer", root),
  )

def render(path, *, root, **substitutions):
  """
  Render a template to the final HTML. All substitutions must be complete.
  """
  html = _load(path, root)
  if "${footer}" in html:
    html = _fill_header_footer(html, root, path)
  return Template(html).substitute(**substitutions)

def hasminutes(year):
  return os.path.exists(f"templates/minutes/{year}.pdf")

def medal(kind, *, root):
  paths = {
    Medal.GOLD: "medal_gold",
    Medal.SILVER: "medal_silver",
    Medal.BRONZE: "medal_bronze",
    Medal.HONOURABLE: "medal_honourable",
  }
  if kind not in paths:
    return ""
  return _load(paths[kind], root)

