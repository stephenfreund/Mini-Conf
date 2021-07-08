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
    parser.add_argument("first", help="first name")
    parser.add_argument("last", help="last name")
    return parser.parse_args()

if __name__ == "__main__":
    config = yaml.load(open("config.yml").read(), Loader=yaml.SafeLoader)
    auth0 = Auth0(config["auth0_domain"], config["auth0_connection"], config["auth0_client_id"], config["auth0_client_secret"])
    
    args = parse_arguments()

    auth0.addUser(
        args.email,
        args.first + " " + args.last)
