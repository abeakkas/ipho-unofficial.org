import shutil

def run():
  print("Copying static files")
  shutil.copytree("templates/img", "../img", dirs_exist_ok=True)
  shutil.copytree("templates/css", "../css", dirs_exist_ok=True)
  shutil.copytree("templates/minutes", "../minutes", dirs_exist_ok=True)

if __name__ == "__main__":
  run()
