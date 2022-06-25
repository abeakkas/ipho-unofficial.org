# Source code
Run main.py to build the project:
```
python3 -B main.py
```

This generates the whole website to the parent folder of src. templates folder
contains HTML files and database folder contains CSV data files.

You can generate individual pages with scripts as well.

After adding a new year increment config.py counters.

## Database format

CSV files don't strictly obey CSV format. They are literally "comma separated values". Thus, names should not include commas.
If you change the database structure update search.js script as well.

##### database/estudiantes.csv:
* Columns: year, rank, name, country-code, medal, theoretical, experimental, total, website
* Medal is one of: G, S, B, H, P.
* Ordered first by year then by rank.
* Don't assume ranks are numbers. They can be in two forms: 1234 or >=1234
* Country-code can be empty if unknown.

##### database/timeline.csv:
* Columns: number, year, date, country code, city, website, # of countries, # of students
* Ordered by year
* Years are not necessarily consecutive
* If there are multiple countries hosting the competition, codes are separated by '&'

##### database/countries.csv:
* Columns: country-code, name, website, if-former

##### database/2020.csv:
* Columns: rank, name, country-code, medal, website

## Notes
* Fahim Tajwar@2017 and Mohammad Fahim Tajwar@2014 from Bangladesh are not the same person
