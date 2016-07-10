#!/bin/bash
echo "Creating timeline/index"

source countrycodes.sh
source header_side.sh 1
source footer.sh

# load file:
html="$(cat templates/timeline/index.html)"
# replace templates
html="${html/__HEADER_SIDE__/$header_side}"
html="${html/__FOOTER__/$footer}"

table=""
rowt="$(cat templates/timeline/index_row.html)"
# Read from CSV
while IFS=, read number year date code city website p_country p_student gold silver bronze honourable newline
do 
    row="$rowt"
    row="${row//__NUMBER__/$number}"
    row="${row//__YEAR__/$year}"
    row="${row//__DATE__/$date}"
    row="${row//__CODE__/$code}"
    row="${row//__CITY__/$city}"
    row="${row//__COUNTRY__/${countrycodes[$code]}}"
    row="${row//__P_COUNTRY__/$p_country}"
    row="${row//__P_STUDENT__/$p_student}"
    table="$row$table"
done < database/timeline.csv
html="${html/__TABLE__/$table}"

html="${html//__BASE__/..}"
source final_replacer.sh
# write
echo "$html" > ../timeline/index.html