#!/usr/bin/python
import util
from database_timeline import year_indexed as t_db_y

templates = {}
# Technically, these don't have to be consecutive
previous_year = util.readfile("database/previous_year.txt").strip()
next_year = util.readfile("database/next_year.txt").strip()

def get(path):
    if path not in templates:
        templates[path] = util.readfile("templates/" + path + ".html")
    return templates[path]

def initial_replace(html, type):
    if type == 0:
        html = html.replace("__HEADER_TOP__", get("header_top"))
    else:
        side = get("header_side")
        if type == 1:
            side = side.replace("__HIGHLIGHT_1__", "highlight")
        elif type == 2:
            side = side.replace("__HIGHLIGHT_2__", "highlight")
        elif type == 3:
            side = side.replace("__HIGHLIGHT_3__", "highlight")
        side = side.replace("__HIGHLIGHT_1__", "")
        side = side.replace("__HIGHLIGHT_2__", "")
        side = side.replace("__HIGHLIGHT_3__", "")
        html = html.replace("__HEADER_SIDE__", side)
    html = html.replace("__HEADER_PREVIOUS_YEAR__", previous_year)
    html = html.replace("__HEADER_PREVIOUS_YEAR_HOMEPAGE__", t_db_y[previous_year]["homepage"])
    html = html.replace("__HEADER_NEXT_YEAR__", next_year)
    html = html.replace("__HEADER_NEXT_YEAR_HOMEPAGE__", t_db_y[next_year]["homepage"])
    html = html.replace("__FOOTER__", get("footer"))
    return html

def final_replace(html, base):
    html = html.replace("__BASE__", base)
    github = True
    if github:
        html = html.replace("__INDEX__", ".")
        html = html.replace("__HTML_EXT__", "")
    else:
        html = html.replace("__INDEX__", "index.html")
        html = html.replace("__HTML_EXT__", ".html")
    html = html.replace("__WEBMASTER__", "iphounofficial@gmail.com")
    return html
