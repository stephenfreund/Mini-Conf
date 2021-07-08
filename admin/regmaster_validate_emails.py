#!/usr/bin/env python3

import csv
import io
import json
import time
import argparse

import requests
import yaml
import sys

from libregmaster import RegMaster

def parse_arguments():
    parser = argparse.ArgumentParser(description="MiniConf Portal Command Line")
    return parser.parse_args()

if __name__ == "__main__":
    config = yaml.load(open("config.yml").read(), Loader=yaml.SafeLoader)

    args = parse_arguments()

    rm = RegMaster(config["regmaster_password"], config["regmaster_endpoint"])

    for line in sys.stdin:
        email = line[:-1]
        result = rm.validate(email)
        if result == None:
            print(f"{email} Registered")
        else:
            print(f"{email} Not Registered: {result}")
        time.sleep(2)