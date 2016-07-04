#!/bin/bash
echo "Creating search"
mkdir -p ../search
cp ./database/countries.csv ../search/
cp ./database/estudiantes.csv ../search/
cp ./templates/search/search.js ../search/

source header_side.sh 3
source footer.sh
# load file:
html="$(cat templates/search/index.html)"
# replace templates
html="${html/__HEADER_SIDE__/$header_side}"
html="${html/__FOOTER__/$footer}"

html="${html//__BASE__/..}"
source final_replacer.sh
# write
echo "$html" > ../search/index.html