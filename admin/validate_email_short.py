#!/usr/bin/env python3

import csv
import io
import json
import time
import zlib

import requests
import yaml
import argparse

from libregmaster import RegMaster
from libauth0 import Auth0
from libgather import Gather

def parse_arguments():
    parser = argparse.ArgumentParser(description="MiniConf Portal Command Line")
    parser.add_argument("email", help="email address of user")
    return parser.parse_args()

if __name__ == "__main__":
    config = yaml.load(open("config.yml").read(), Loader=yaml.SafeLoader)

    args = parse_arguments()

    rm = RegMaster(config["regmaster_password"], config["regmaster_endpoint"])
    # result = rm.validate(args.email)
    # if "error" in result:
    #     print(f"Not Registered: {result['error']}")
    # else:
    #     print(f"Registered: {json.dumps(result, indent=2)}")
    result = rm.validate(args.email)
    if result == None:
        print(f"Registered")
    else:
        print(f"Not Registered: {result}")

    auth0 = Auth0(config["auth0_domain"], config["auth0_connection"], config["auth0_client_id"], config["auth0_client_secret"])
    result = auth0.getUser(args.email)
    if len(result) == 0:
        print("No In Auth0.")
    else:
        print("In Auth0")

    gather = Gather(config["gather_api_key"], config["gather_space_id"])
    dict = gather.getGatherEmailDictionary()

    if args.email in dict: 
        print("In Gather")
    else:
        print("Not In Gather")