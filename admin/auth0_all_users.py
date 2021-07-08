#!/usr/bin/env python3

import csv
import io
import json
import time
import zlib

import requests
import yaml

from libauth0 import Auth0

if __name__ == "__main__":
    config = yaml.load(open("config.yml").read(), Loader=yaml.SafeLoader)
    auth0 = Auth0(config["auth0_domain"], config["auth0_connection"], config["auth0_client_id"], config["auth0_client_secret"])
    
    result = sorted(auth0.userList(), key=lambda x : x["email"])
    print("email,name")
    for attendee in result:
        print(f"{attendee['email']},{attendee['name']}")

