echo "Bad Password"

curl -X POST -d "action=validate&password=nope&email=..." https://regmaster.com/2021conf/PLDI21/PLDIgetName.php

echo ""
echo ""

echo "Registered and Paid lookup"

curl -X POST -d "action=validate&password=UZHgcjZdzsGg&email=..." https://regmaster.com/2021conf/PLDI21/PLDIgetName.php

echo ""
echo ""


echo "Registered and UnPaid lookup"

curl -X POST -d "action=validate&password=UZHgcjZdzsGg&email=..." https://regmaster.com/2021conf/PLDI21/PLDIgetName.php

echo ""
echo ""

echo "Not Registered  lookup"

curl -X POST -d "action=validate&password=UZHgcjZdzsGg&email=..." https://regmaster.com/2021conf/PLDI21/PLDIgetName.php

echo ""
echo ""

echo "all lookup"

curl -X POST -d "action=listall&password=UZHgcjZdzsGg" https://regmaster.com/2021conf/PLDI21/PLDIgetName.php

echo ""
echo ""

echo "all paid lookup"

curl -X POST -d "action=listpaid&password=UZHgcjZdzsGg" https://regmaster.com/2021conf/PLDI21/PLDIgetName.php

echo ""
echo ""




