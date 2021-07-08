#!/usr/bin/env python3

import csv
import io
import json
import time
import zlib

import requests
import yaml
import argparse

from libauth0 import Auth0

def parse_arguments():
    parser = argparse.ArgumentParser(description="MiniConf Portal Command Line")
    parser.add_argument("email", help="email address of user")
    return parser.parse_args()

if __name__ == "__main__":
    config = yaml.load(open("config.yml").read(), Loader=yaml.SafeLoader)
    auth0 = Auth0(config["auth0_domain"], config["auth0_connection"], config["auth0_client_id"], config["auth0_client_secret"])
    
    args = parse_arguments()

    result = auth0.getUser(args.email)
    if len(result) == 0:
        print("Email address is not in Database.")
    else:
        print(json.dumps(result, indent=2))