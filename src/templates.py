#!/usr/bin/python
import util
import config
from database_timeline import year_indexed as t_db_y

def get(path, templates={}):
    """
    Load HTML from file and return as string
    templates is used for memoization
    """
    if path not in templates:
        templates[path] = util.readfile("templates/" + path + ".html")
    return templates[path]

def initial_replace(html, type):
    """
    Fill header and footer in given template string
    type=0 is for top header pages
    type=[1,2,3] is for side header with different highlights
    """
    if type == 0:
        html = html.replace("__HEADER_TOP__", get("header_top"))
    else:
        side = get("header_side")
        side = side.replace("__HIGHLIGHT_" + str(type) + "__", "highlight")
        side = side.replace("__HIGHLIGHT_1__", "")
        side = side.replace("__HIGHLIGHT_2__", "")
        side = side.replace("__HIGHLIGHT_3__", "")
        html = html.replace("__HEADER_SIDE__", side)
    html = html.replace("__HEADER_PREVIOUS_YEAR__", config.previous_year)
    html = html.replace("__HEADER_PREVIOUS_YEAR_HOMEPAGE__", t_db_y[config.previous_year]["homepage"])
    html = html.replace("__HEADER_NEXT_YEAR__", config.next_year)
    html = html.replace("__HEADER_NEXT_YEAR_HOMEPAGE__", t_db_y[config.next_year]["homepage"])
    html = html.replace("__FOOTER__", get("footer"))
    return html

def final_replace(html, root):
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
