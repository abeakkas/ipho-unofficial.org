#!/usr/bin/python
import util
import templates

def create(name):
    util.makedirs("../" + name + ".php")
    html = templates.get("backward_compatibility/" + name)
    html = templates.final_replace(html, "..")
    util.writefile("../" + name + ".php/index.html", html)

def run():
    print "Copying backward compatibility files"
    create("index")
    create("countries")
    create("country_individual")
    create("country_info")
    create("organizers")
    create("search")
    create("year_country")
    create("year_individual")
    create("year_info")
    
if __name__ == "__main__":
    run()