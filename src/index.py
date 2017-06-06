#!/usr/bin/python
import util
import templates

def run():
    print("Creating index")
    html = templates.get("index")
    html = templates.initial_replace(html, 0)
    html = templates.final_replace(html, ".")
    util.writefile("../index.html", html)
    
if __name__ == "__main__":
    run()
