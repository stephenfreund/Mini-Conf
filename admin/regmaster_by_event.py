#!/usr/bin/env python3

import csv
import io
import json
import time
import argparse

import requests
import yaml

def parse_arguments():
    parser = argparse.ArgumentParser(description="MiniConf Portal Command Line")
    parser.add_argument("file", help="csv file from regmaster")
    return parser.parse_args()

colAndKey = [ 
    ("t1", "HOPL"),
    ("t2", "ARRAY"),
    ("t3", "Infer"),
    ("t4", "MAPS"),
    ("t5", "IMOP"),
    ("t6", "PLMW"),
    ("t7", "SOAP"),
    ("t8", "PLanQC"),
    ("t9", "ISMM"),
    ("t10", "LCTES"),
    ("t11", "CONTRACTS"),
    ("t12", "PERSIST"),
    ("c31", "PLMW-Mentor"),
    ("c32", "SIGPLAN-Mentor"),
    ("c34", "Match-with-Mentor")]

if __name__ == "__main__":
    args = parse_arguments()

    with open(args.file) as f:
        content = f.readlines()
    data = [ content[2] ] + content[4:]

    attendees = list(csv.DictReader(data))

    for col, key in colAndKey:
        with open(f'auto/attendees-{key}.csv', "w") as f:    
            f.write("email,first,last\n")
            for a in attendees: 
                if a[col] == "1":
                    f.write(f'{a["email"]},{a["firstna"]},{a["lastna"]}\n')
