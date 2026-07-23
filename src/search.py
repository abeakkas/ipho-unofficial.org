import shutil
import util
from templates import render_page

def run():
  print("Generating search")
  util.makedirs("../search")
  shutil.copyfile("database/countries.csv", "../search/countries.csv")
  shutil.copyfile("database/participants.csv", "../search/participants.csv")
  shutil.copyfile("database/2020.csv", "../search/2020.csv")
  shutil.copyfile("templates/search/search.js", "../search/search.js")
  shutil.copyfile("templates/search/asciify.js", "../search/asciify.js")
  render_page("search/index", "../search/index.html")

if __name__ == "__main__":
  run()

