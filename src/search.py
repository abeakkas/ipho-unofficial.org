import util
from templates import render

def run():
  print("Generating search")
  util.makedirs("../search")
  util.copyfile("database/countries.csv", "../search/countries.csv")
  util.copyfile("database/participants.csv", "../search/participants.csv")
  util.copyfile("database/2020.csv", "../search/2020.csv")
  util.copyfile("templates/search/search.js", "../search/search.js")
  util.copyfile("templates/search/asciify.js", "../search/asciify.js")
  html = render(
    "search/index",
    root="..",
  )
  util.writefile("../search/index.html", html)

if __name__ == "__main__":
  run()

