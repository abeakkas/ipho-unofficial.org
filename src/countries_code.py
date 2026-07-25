import sys
import countries_code_index
import countries_code_individual

def run(code):
  print(f"Generating countries/{code}")
  countries_code_index.run(code)
  countries_code_individual.run(code)

if __name__ == "__main__":
  run(sys.argv[1])

