#!/usr/bin/env python3
import argparse
import json
import re

import dateutil
import pytz
import requests
import unidecode
from bs4 import BeautifulSoup


def parse_arguments():
    parser = argparse.ArgumentParser(description="MiniConf Calendar Command Line")

    parser.add_argument(
        "--html",
        default="abs.html",
        type=str,
        help="html file from cpc",
    )

    parser.add_argument("--out", default="pldi-abstracts.json", help="output file")

    return parser.parse_args()


def convert(args):

    with open(args.html, "r") as f:
        html = f.read()
    soup = BeautifulSoup(html, "html.parser")
    j = {}
    for span in soup.find_all("span", id=re.compile("pldi21main.*")):
        UID = "pldi." + span["id"].split("-")[1][1:]
        s = str(span)
        c = s.find(">")
        o = s.rfind("<")
        s = s[c + 1 : o]
        j[UID] = s
    with open(args.out, "w") as outfile:
        outfile.write(json.dumps(j, indent=4))


if __name__ == "__main__":
    args = parse_arguments()
    convert(args)
