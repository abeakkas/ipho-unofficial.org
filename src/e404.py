#!/usr/bin/python
import util
import templates

def run():
    print("Creating 404")
    html = templates.get("404")
    html = templates.initial_replace(html, -1)
    html = templates.final_replace(html, ".")
    util.writefile("../404.html", html)

if __name__ == "__main__":
    run()
