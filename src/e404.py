from templates import render_page

def run():
  print("Generating 404")
  # This can't both work local and Github :/
  # but it only works on Github anyways
  render_page("404", "../404.html")

if __name__ == "__main__":
  run()

