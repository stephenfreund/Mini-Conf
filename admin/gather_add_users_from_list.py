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
    return parser.parse_args()

if __name__ == "__main__":
    config = yaml.load(open("config.yml").read(), Loader=yaml.SafeLoader)

    args = parse_arguments()

    gather = Gather(config["gather_api_key"], config["gather_space_id"])
    originalGatherDict = gather.getGatherEmailDictionary()

    # remove any blacklisted users
    blacklist = yaml.load(requests.get(config["blacklist"]).text, Loader=yaml.SafeLoader)
    if args.email in blacklist:
        print("Blacklisted email!")
    else:
        # emailDict = { args.email: { "name": args.first + " " + args.last } }
        emailDict = { args.email: {  } }

        gather.setGatherEmailDictionary(
            emailDict,
            len(originalGatherDict) == 0,
        )

