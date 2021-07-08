#!/usr/bin/env python3

import csv
import io
import json
import time
import zlib

import requests
import yaml
import argparse
import datetime

from libauth0 import Auth0

def pretty_date(time=False):
    """
    Get a datetime object or a int() Epoch timestamp and return a
    pretty string like 'an hour ago', 'Yesterday', '3 months ago',
    'just now', etc
    """
    from datetime import datetime
    now = datetime.utcnow()
    if type(time) is int:
        diff = now - datetime.fromtimestamp(time)
    elif isinstance(time,datetime):
        diff = now - time
    elif not time:
        diff = now - now
    second_diff = int(diff.seconds)
    day_diff = int(diff.days)

    if day_diff < 0:
        return ''

    if day_diff == 0:
        if second_diff < 10:
            return "just now"
        if second_diff < 60:
            return str(second_diff) + " seconds ago"
        if second_diff < 120:
            return "a minute ago"
        if second_diff < 7200:
            return str(int(second_diff / 60)) + " minutes ago"
        if second_diff < 7200:
            return "an hour ago"
        if second_diff < 86400:
            return str(int(second_diff / 3600)) + " hours ago"
    if day_diff == 1:
        return "Yesterday"
    if day_diff < 7:
        return str(day_diff) + " days ago"
    if day_diff < 31:
        return str(day_diff / 7) + " weeks ago"
    if day_diff < 365:
        return str(day_diff / 30) + " months ago"
    return str(day_diff / 365) + " years ago"


def parse_arguments():
    parser = argparse.ArgumentParser(description="MiniConf Portal Command Line")
    parser.add_argument('-v', default=False, action='store_true')
    return parser.parse_args()

if __name__ == "__main__":
    config = yaml.load(open("config.yml").read(), Loader=yaml.SafeLoader)
    auth0 = Auth0(config["auth0_domain"], config["auth0_connection"], config["auth0_client_id"], config["auth0_client_secret"])
    
    args = parse_arguments()

    result = auth0.getLog("NOT (type:s*) AND NOT (type:fsa) OR (type:ss)")
    if (args.v):
        print(json.dumps(result, indent=2))
    else:
        for e in result:
            date = datetime.datetime.fromisoformat(e["date"][:-1])
            print(f'{pretty_date(date): <16} -- {str(date): <16} -- {e["type"]: <6} -- {e.get("user_name", ""): <12} -- {e["description"]}')