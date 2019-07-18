# Source code
Run main.py to build the project:
```
python2.7 -B main.py
```

This generates the whole website to the parent folder by filling in the
pages in the templates folder with data from the database folder.

You can generate individual pages with scripts as well.

After adding a new year increment config.py counters.

## Assumptions

CSV files don't strictly obey CSV format. They are literally "comma separated values". Thus, names should not include commas.

##### database/estudiantes.csv:
* Columns: year, rank, name, country code, medal, theoretical, experimental, total.
* Medal is one of: G, S, B, H, P.
* Ordered first by year then by rank.
* Don't assume ranks are numbers. They can be in two forms: 1234 or >=1234
* Country-code can be empty if unknown.

##### database/timeline.csv:
* Columns: number, year, date, country code, city, website, # of countries, # of students 
* Ordered by year

##### database/countries.csv:
* Columns: country code, name, website, if former

## Notes
* Fahim Tajwar@2017 and Mohammad Fahim Tajwar@2014 from Bangladesh are not the same person
