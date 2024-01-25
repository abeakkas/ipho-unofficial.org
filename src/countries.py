import countries_code
import countries_index
import util
from database_countries import database as c_db

def run():
    print("Generating countries")
    util.makedirs("../countries")
    countries_index.run()
    for codedata in c_db:
        countries_code.run(codedata.code)

if __name__ == "__main__":
    run()
