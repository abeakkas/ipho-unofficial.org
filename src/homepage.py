import templates
import util

def run():
    print("Generating homepage")
    html = templates.get("homepage")
    html = templates.set_headers(html, "homepage")
    html = templates.finalize(html, ".")
    util.writefile("../index.html", html)

if __name__ == "__main__":
    run()
