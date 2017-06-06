#!/usr/bin/python
import util
import templates

def run():
    print("Creating search")
    util.makedirs("../search")
    util.copyfile("database/countries.csv", "../search/countries.csv")
    util.copyfile("database/estudiantes.csv", "../search/estudiantes.csv")
    util.copyfile("templates/search/search.js", "../search/search.js")
    html = templates.get("search/index")
    html = templates.initial_replace(html, 3)
    html = templates.final_replace(html, "..")
    util.writefile("../search/index.html", html)
    
if __name__ == "__main__":
    run()
