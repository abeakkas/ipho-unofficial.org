# Source code
Run main.py from src to build the project:
```
python3 main.py
```

This generates the whole website to the parent folder of src. templates folder
contains HTML files and database folder contains CSV data files.

You can generate individual pages with scripts as well.
```
python3 timeline_year.py 2024
```

## How to maintain

After every competition:
- Pull the rankings/medals from the official website and add to `archive` folder
- Update `participants.csv` using the rankings data
- Pull that year's minutes document from IPhO official website and add it to `templates/minutes`
- Update `timeline.csv` using the minutes
- Run `main.py` and `validate.py`

## Database format

> If you change the database structure update `templates/search/search.js` script as well.

##### database/participants.csv:
* Columns: year, rank, name, country-code, medal, theoretical, experimental, total, website
* Medal is one of: G, S, B, H, P
* Ordered first by year then by rank
* Rank can be in two forms: `123`, `>=123`
* Country-code can be empty if unknown

##### database/timeline.csv:
* Columns: number, year, date, country code, city, website, # of countries, # of participants
* Ordered by year
* Years are not necessarily consecutive
* If there are multiple countries hosting the competition, codes are separated by '&'

##### database/countries.csv:
* Columns: country-code, name, website, if-former

##### database/2020.csv:
* Columns: rank, name, country-code, medal, website

##### Run validate.py to check for database issues:
```
python3 validate.py
```

## Notes
* Fahim Tajwar@2017 and Mohammad Fahim Tajwar@2014 from Bangladesh are not the same person
* Kazhymurat Aknazar@2017's name originally had a typo and was written as Kazhymurat Aknar
* Delia Cropper@2018's name was changed from Daniel Cropper due to contestant request
* Ophelia Evelyn Sommer@2017/2018's name was changed from Oscar Emil Sommer due to contestant request
* Eleni Claire Shor@2019's name was changed from Guilhermo Cutrim Costa due to contestant request
* Joshua Zexi Lin@2015's theoretical and experimental scores reported in the official release don't add up the to total score
* 2006, 2014 Minutes and data don't match
