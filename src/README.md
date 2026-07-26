# Source code
Run main.py from src to build the project:
```
python3 main.py
```

This generates the whole website to the parent folder of src.

`templates` folder contains HTML files, `static_files` folder contains images/CSS/minutes that are copied to the output as-is, and `database` folder contains CSV data files.

## How to maintain

After every competition:
- Pull the rankings/medals from the official website in some format (pdf/html) and add to `archive` folder
- Update `participants.csv` using the rankings data
- Pull that year's minutes document from IPhO official website and add it to `static_files/minutes`
- Update `timeline.csv` using the minutes
- Run `main.py` and `validate.py`

## Database format

> If you change the database structure update `templates/search/search.js` script as well.

##### database/participants.csv:
* Columns: year, rank, name, country-code, medal, theoretical, experimental, total, website
* Ordered first by year then by rank
* Medal is one of: G, S, B, H, P
* Rank can be in two forms: `123`, `>=123`

##### database/timeline.csv:
* Columns: number, year, date, country-code, city, website, # of countries, # of participants
* Ordered by year
* If there are multiple countries hosting the competition, codes are separated by '&'

##### database/countries.csv:
* Columns: country-code, name, website, if-former

##### database/2020.csv:
* Columns: rank, name, country-code, medal, website

##### Run validate.py to check for database issues:
```
python3 validate.py
```

##### Run name_analysis.py to find possible duplicate participants:
```
python3 name_analysis.py
```
Reports same country participants a year or two apart whose names look alike: reordered, missing a middle name, or spelled differently. Handy for catching data entry slip ups and repeat participants for the hall of fame.

## Notes
* Fahim Tajwar@2017 and Mohammad Fahim Tajwar@2014 from Bangladesh are not the same person
* Kazhymurat Aknazar@2017's name originally had a typo and was written as Kazhymurat Aknar
* Delia Cropper@2018's name was changed from Daniel Cropper due to contestant request
* Ophelia Evelyn Sommer@2017/2018's name was changed from Oscar Emil Sommer due to contestant request
* Eleni Claire Shor@2019's name was changed from Guilhermo Cutrim Costa due to contestant request
* Joshua Zexi Lin@2015's theoretical and experimental scores reported in the official release don't add up the to total score
* 2006, 2014 Minutes and data don't match
