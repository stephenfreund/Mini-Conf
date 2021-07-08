#!/usr/bin/env python3

import csv
import io
import json
import time
import argparse

import requests
import yaml

from libgather import Gather

def parse_arguments():
    parser = argparse.ArgumentParser(description="MiniConf Portal Command Line")
    parser.add_argument("email", help="email address of user")
    return parser.parse_args()

if __name__ == "__main__":
    config = yaml.load(open("config.yml").read(), Loader=yaml.SafeLoader)

    args = parse_arguments()

    gather = Gather(config["gather_api_key"], config["gather_space_id"])
    dict = gather.getGatherEmailDictionary()

    del dict[args.email]

    gather.setGatherEmailDictionary(
        dict,
        True  # Must overwrite here...  This is racy with other updates!
    )

