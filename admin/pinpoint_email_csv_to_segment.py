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
    parser.add_argument("file", help="csv file of email,name lines")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()
    users = list(csv.DictReader(open(args.file)))
    print("ChannelType,Address")
    for p in users:
        print(f"EMAIL,{p['email']}")
