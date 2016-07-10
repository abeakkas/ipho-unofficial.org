#!/bin/bash
echo "Creating index"
source header_top.sh
source footer.sh
# load file:
html="$(cat templates/index.html)"
# replace templates
html="${html/__HEADER_TOP__/$header_top}"
html="${html/__FOOTER__/$footer}"

html="${html//__BASE__/.}"
source final_replacer.sh
# write
echo "$html" > ../index.html