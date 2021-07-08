#!/bin/bash

curl -X POST -d "action=validate&password=nope&email=$1" https://regmaster.com/2021conf/PLDI21/PLDIgetName.php
