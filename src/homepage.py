import util
from templates import render

def run():
  print("Generating homepage")
  html = render(
    "homepage",
    root=".",
    section="homepage",
  )
  util.writefile("../index.html", html)

if __name__ == "__main__":
  run()
