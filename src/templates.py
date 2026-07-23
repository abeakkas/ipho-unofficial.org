import config
import os
from functools import cache
from string import Template
from database_participants import last_year
from database_participants import next_year
from database_participants import Medal
from database_timeline import year_indexed as editions_by_year

@cache
def _load(path):
  """
  Load HTML from file and resolve the common substitutions.
  """
  with open("templates/" + path + ".html") as file:
    html = file.read()
  return Template(html).safe_substitute(
    index="." if config.github else "index.html",
    html_ext="" if config.github else ".html",
    webmaster=config.webmaster_email,
  )

def render_fragment(path, **substitutions):
  """
  Render a partial HTML to be used as part of a page.
  """
  return Template(_load(path)).substitute(**substitutions)

def _fill_header_footer(html, path):
  """
  Fill header/footer. Nav highlight is determined from path's first segment.
  """
  section = path.split("/")[0]
  side = render_fragment(
    "header_side",
    highlight_timeline="highlight" if section == "timeline" else "",
    highlight_countries="highlight" if section == "countries" else "",
    highlight_search="highlight" if section == "search" else "",
    highlight_hall_of_fame="highlight" if section == "hall-of-fame" else "",
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
    footer=render_fragment("footer"),
  )

def render_page(path, **substitutions):
  """
  Render a full page and write it. The output location is derived from the
  template path, and {{root}} is resolved from that location.
  """
  html = _load(path)

  if "${footer}" in html:
    html = _fill_header_footer(html, path)
  html = Template(html).substitute(**substitutions)

  out_path = f"../{path}.html"
  if "/code/" in out_path:
    out_path = out_path.replace("/code/", f"/{substitutions['code']}/")
  if "/year/" in out_path:
    out_path = out_path.replace("/year/", f"/{substitutions['year']}/")

  out_dir = os.path.dirname(out_path)
  if path == "404":
    # 404 can be served from any URL, so its links must be absolute (empty root).
    root = ""
  else:
    root = os.path.relpath("..", out_dir)

  # {{root}} is a relative path prefix to the site root.
  os.makedirs(out_dir, exist_ok=True)
  with open(out_path, "w") as file:
    file.write(html.replace("{{root}}", root))

def hasminutes(year):
  return os.path.exists(f"templates/minutes/{year}.pdf")

def medal(kind):
  paths = {
    Medal.GOLD: "medal_gold",
    Medal.SILVER: "medal_silver",
    Medal.BRONZE: "medal_bronze",
    Medal.HONOURABLE: "medal_honourable",
  }
  if kind not in paths:
    return ""
  return _load(paths[kind])
