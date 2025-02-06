# ipho-unofficial.org
The website is static, as it is hosted solely on Github pages. The pages are generated through Python scripts using database files located in src/database/.

You can build the project by running main.py from src folder. This extracts all the necessary files to parent folder of src. Building src recreates the whole codebase (except CNAME, LICENSE, and README.md files), therefore you should only make your changes in src.

### Known issues
* ~~Rankings for some years are not accurate. Some are ordered by country or name and should be fixed to >= notation for rankings.~~
* ~~&gt;= rankings should be used for students without medals.~~
* For first IPhO there were rankings of students but they were not awarded medals. So current representation is not accurate.
