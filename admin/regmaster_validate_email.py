#!/usr/bin/env python3

import csv
import io
import json
import time
import argparse

import requests
import yaml

from libregmaster import RegMaster

def parse_arguments():
    parser = argparse.ArgumentParser(description="MiniConf Portal Command Line")
    parser.add_argument("email", help="email address of user")
    return parser.parse_args()

if __name__ == "__main__":
    config = yaml.load(open("config.yml").read(), Loader=yaml.SafeLoader)

    args = parse_arguments()

    rm = RegMaster(config["regmaster_password"], config["regmaster_endpoint"])

    result = rm.validate(args.email)
    if result == None:
        print(f"Registered")
    else:
        print(f"Not Registered: {result}")
