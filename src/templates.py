import config
import os
from functools import cache
from string import Template
from database_participants import last_completed_year
from database_participants import Medal
from database_timeline import editions_by_year
from database_timeline import year_after

@cache
def _load(path):
  """
  Load HTML from file and resolve the common substitutions.
  """
  with open(f"templates/{path}.html") as file:
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

def render_page(path, **substitutions):
  """
  Render a full page and write it. The output location is derived from the
  template path, and {{root}} is resolved from that location.
  """
  html = _load(path)

  # Every page has a header and footer. Nav highlight is from the path's first segment.
  section = path.split("/")[0]
  if last_completed_year in year_after:
    next_year = year_after[last_completed_year]
    next_homepage = editions_by_year[next_year].homepage
  else:
    # No upcoming edition in timeline.csv yet; show the year with no homepage link.
    next_year = last_completed_year + 1
    next_homepage = "."

  # The homepage carries the header inline; every other page pulls in header_side.
  if "${header_side}" in html:
    substitutions["header_side"] = render_fragment(
      "header_side",
      section=section,
      header_previous_year=last_completed_year,
      header_previous_year_homepage=editions_by_year[last_completed_year].homepage,
      header_next_year=next_year,
      header_next_year_homepage=next_homepage,
    )
  else:
    substitutions["header_previous_year"] = last_completed_year
    substitutions["header_previous_year_homepage"] = editions_by_year[last_completed_year].homepage
    substitutions["header_next_year"] = next_year
    substitutions["header_next_year_homepage"] = next_homepage

  substitutions["footer"] = render_fragment("footer")

  # Header/footer are added as values, so a '$' in a homepage URL is inserted
  # literally rather than being re-parsed as a placeholder.
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

def medal_fragment(kind):
  paths = {
    Medal.GOLD: "medal_gold",
    Medal.SILVER: "medal_silver",
    Medal.BRONZE: "medal_bronze",
    Medal.HONOURABLE: "medal_honourable",
  }
  if kind not in paths:
    return ""
  return _load(paths[kind])
