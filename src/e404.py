import templates
import util

def run():
    print("Creating 404")
    html = templates.get("404")
    html = templates.initial_replace(html, -1)
    # This can't both work local and Github :/
    # but it only works on Github anyways
    html = templates.final_replace(html, "")
    util.writefile("../404.html", html)

if __name__ == "__main__":
    run()
