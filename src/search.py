import templates
import util

def run():
    print("Generating search")
    util.makedirs("../search")
    util.copyfile("database/countries.csv", "../search/countries.csv")
    util.copyfile("database/estudiantes.csv", "../search/estudiantes.csv")
    util.copyfile("database/2020.csv", "../search/2020.csv")
    util.copyfile("templates/search/search.js", "../search/search.js")
    util.copyfile("templates/search/asciify.js", "../search/asciify.js")
    html = templates.get("search/index")
    html = templates.set_headers(html, "search")
    html = templates.finalize(html, "..")
    util.writefile("../search/index.html", html)

if __name__ == "__main__":
    run()
