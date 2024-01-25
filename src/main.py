import countries
import e404
import hall_of_fame
import homepage
import search
import static_files
import timeline

def run():
    print("Generating the whole project")
    homepage.run()
    e404.run()
    timeline.run()
    countries.run()
    search.run()
    hall_of_fame.run()
    static_files.run()

if __name__ == "__main__":
    run()
