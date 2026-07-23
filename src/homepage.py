from templates import render_page

def run():
  print("Generating homepage")
  render_page("homepage", "../index.html")

if __name__ == "__main__":
  run()
