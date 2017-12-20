# Source code
Run main.py to create the project:
```
python2.7 -B main.py
```

You can run individual scripts with command line arguments.

## Assumptions

CSV files don't actually obey CSV format. They are literally "comma separated values". Thus, names should not include commas.

##### database/estudiantes.csv:
* Columns: year, rank, name, country-code, medal, theoretical, experimental, total.
* Medal is one of: G, S, B, H, P.
* Ordered first by year then by rank.
* Don't assume ranks are numbers. They can be in two forms: 1234 or >=1234
* Country-code can be empty if unknown.

##### database/timeline.csv:
* Ordered by year
