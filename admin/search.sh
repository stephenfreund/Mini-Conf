#
# First do:
#
#  ./regmaster_all_registered.py > r.csv
#
# Then run:
#
#  ./search.sh r.csv name/email/whatever
#

lines=`grep -i $2 $1`

while IFS= read -r line; do
    echo ""
    echo $line
    echo $line | cut -d, -f1 | xargs ./validate_email_short.py
done <<< "$lines"
