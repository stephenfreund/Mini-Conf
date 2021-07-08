#!/usr/bin/env python3

import csv
import io
import json
import time
import argparse

import requests
import yaml

from libgather import Gather

if __name__ == "__main__":
    config = yaml.load(open("config.yml").read(), Loader=yaml.SafeLoader)

    gather = Gather(config["gather_api_key"], config["gather_space_id"])
    users = [(k,v.get("name", "")) for k,v in gather.getGatherEmailDictionary().items()]
    print("email,name")
    for email,name in sorted(users, key=lambda x: x[0]):
        print(f"{email},{name}")

