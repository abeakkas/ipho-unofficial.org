#!/bin/bash
echo "Creating countries/index"

source countrycodes.sh
source header_side.sh 2
source footer.sh

# load file:
html="$(cat templates/countries/index.html)"
# replace templates
html="${html/__HEADER_SIDE__/$header_side}"
html="${html/__FOOTER__/$footer}"

table=""
rowt="$(cat templates/countries/index_row.html)"
# Read from CSV
while IFS=, read code country nationalsite newline
do
    row="$rowt"
    row="${row//__CODE__/$code}"
    row="${row//__COUNTRY__/${countrycodes[$code]}}"
    if [ "$nationalsite" != "" ]
    then
        temp="$(cat templates/countries/index_national_site.html)"
        temp="${temp//__LINK__/$nationalsite}"
        if [ ${#nationalsite} -lt 50 ]
        then
            temp="${temp//__NAME__/$nationalsite}"
        else
            temp="${temp//__NAME__/${nationalsite:0:50}...}"
        fi
        row="${row//__NATIONAL_SITE__/$temp}"
    else
        row="${row//__NATIONAL_SITE__/}"
    fi
    hosts=""
    flag=0
    # as inefficient as possible
    while IFS=, read number year date _code city website p_country p_student gold silver bronze honourable newline
    do 
        if [ $code == $_code ]
        then
            if [ $flag != 0 ]
            then
                hosts=$hosts", "
            fi
            temp="$(cat templates/countries/index_year.html)"
            temp="${temp//__YEAR__/$year}"
            hosts=$hosts$temp
            ((flag++))
        fi
    done < database/timeline.csv
    row="${row//__HOSTS__/$hosts}"
    table+="$row"
done < database/countries.csv
html="${html/__TABLE__/$table}"

html="${html//__BASE__/..}"
source final_replacer.sh
# write
echo "$html" > ../countries/index.html