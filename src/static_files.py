import shutil

def run():
  print("Copying static files")
  shutil.copytree("static_files", "..", dirs_exist_ok=True)

if __name__ == "__main__":
  run()
