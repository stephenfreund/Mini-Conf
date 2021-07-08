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

    blacklist = yaml.load(requests.get(config["blacklist"]).text, Loader=yaml.SafeLoader)
    for blacklisted in blacklist:
        print(f"{blacklisted}")

