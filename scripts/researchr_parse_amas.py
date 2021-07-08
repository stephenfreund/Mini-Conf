#!/usr/bin/env python3

# usage: python3 researchr_parse_colocated_events_from_ics.py --room SOAP --ics workshop-researchr-example.ics --json pldi-researchr-full.json

import argparse
import json
import re

import requests
from ics.icalendar import Calendar


def parse_arguments():
    parser = argparse.ArgumentParser(description="MiniConf Calendar Command Line")

    parser.add_argument(
        "--ics",
        default="sample_cal.ics",
        type=str,
        help="ICS file to parse (local or via http)",
    )

    parser.add_argument("--out", default="calendar.csv", help="output file")

    return parser.parse_args()


def makeISO(date, time):
    return date + "T" + time + ":00-04:00"


def sessionTime(session):
    times = session["Time"].split(" - ")
    start = makeISO(session["Day"], times[0])
    return start


def typeOfEvent(jsonData, key):
    return [x["Type"] for x in jsonData["Items"] if x["Key"] == key][0]


def collectEventKeys(jsonData, room):
    sessions = [
        s for s in jsonData["Sessions"] if s["Location"].split("Online | ")[1] == room
    ]
    sortedEvents = list(sorted(sessions, key=sessionTime))
    events = [e for s in sortedEvents for e in s["Items"]]
    return events


def convert(args):

    file_ics: str = args.ics
    if not file_ics.startswith("http"):
        with open(file_ics, "r") as f:
            c = Calendar(f.read())
    else:
        c = Calendar(requests.get(file_ics).text)

    regex = "\[PLDI Ask Me Anything\] [^-]*- (.*)"
    pattern = re.compile(regex)

    with (open(args.out, "w")) as f:
        f.write("event,start,end,title,authors,category,trackUID,gather,zoom,info\n")
        roomEvents = [x for x in c.events if pattern.match(x.name) != None]
        sortedEvents = list(sorted(roomEvents, key=lambda c: c.begin))
        for i, e in enumerate(sortedEvents):
            m = pattern.match(e.name)
            person = m.group(1).strip()

            f.write(
                f'ama.{i},{e.begin.for_json()},{e.end.for_json()},"{person}","","qa","pldi-A",,,\n'
            )


if __name__ == "__main__":
    args = parse_arguments()
    convert(args)
