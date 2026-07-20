import os

def makedirs(path):
  os.makedirs(path, exist_ok=True)

def readfile(path):
  with open(path, 'r') as file:
    return file.read()

def writefile(path, content):
  with open(path, 'w') as file:
    return file.write(content)

def copyfile(_from, to):
  writefile(to, readfile(_from))

def ordinal(number: str) -> str:
  if number[-2:] in ("11", "12", "13"):
    return "th"
  elif number[-1] == "1":
    return "st"
  elif number[-1] == "2":
    return "nd"
  elif number[-1] == "3":
    return "rd"
  else:
    return "th"

