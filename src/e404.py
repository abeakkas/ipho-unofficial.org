import templates
import util

def run():
    print("Generating 404")
    html = templates.get("404")
    html = templates.set_headers(html, "")
    # This can't both work local and Github :/
    # but it only works on Github anyways
    html = templates.finalize(html, "")
    util.writefile("../404.html", html)

if __name__ == "__main__":
    run()
