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
    dict = gather.getGatherEmailDictionary()

    # remove any blacklisted users
    blacklist = yaml.load(requests.get(config["blacklist"]).text, Loader=yaml.SafeLoader)
    for blacklisted in blacklist:
        if blacklisted in dict:
            print(f"Removing {blacklisted}")
            del dict[blacklisted]

    gather.setGatherEmailDictionary(
        dict,
        True  # Must overwrite here...  This is racy with other updates!
    )

