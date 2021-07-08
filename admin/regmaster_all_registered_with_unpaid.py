#!/usr/bin/env python3

import csv
import io
import json
import time
import argparse

import requests
import yaml

from libregmaster import RegMaster


if __name__ == "__main__":
    config = yaml.load(open("config.yml").read(), Loader=yaml.SafeLoader)

    rm = RegMaster(config["regmaster_password"], config["regmaster_endpoint"])

    result = rm.allRegisteredWithUnpaid()
    print("email,name")
    for attendee in result:
        print(f"{attendee['email']},{attendee['name']}")
