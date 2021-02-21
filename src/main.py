import countries
import e404
import index
import search
import static_files
import timeline

def run():
    print("Creating the whole project")
    index.run()
    e404.run()
    timeline.run()
    countries.run()
    search.run()
    static_files.run()

if __name__ == "__main__":
    run()
