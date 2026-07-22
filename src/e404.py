import util
from templates import render

def run():
  print("Generating 404")
  # This can't both work local and Github :/
  # but it only works on Github anyways
  html = render(
    "404",
    root="",
    section="",
  )
  util.writefile("../404.html", html)

if __name__ == "__main__":
  run()

