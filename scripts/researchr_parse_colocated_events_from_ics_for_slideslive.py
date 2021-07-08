#!/usr/bin/env python3

# usage: python3 researchr_parse_colocated_events_from_ics.py --room SOAP --ics workshop-researchr-example.ics --json pldi-researchr-full.json

import argparse
import json
import re

import dateutil
import pytz
import requests
import unidecode
from ics.icalendar import Calendar


def parse_arguments():
    parser = argparse.ArgumentParser(description="MiniConf Calendar Command Line")

    parser.add_argument(
        "--room",
        default="SOAP",
        type=str,
        help="Researchr room we're processing",
    )

    parser.add_argument(
        "--ics",
        default="researchr.ics",
        type=str,
        help="calendar entries from Researchr",
    )

    parser.add_argument(
        "--json",
        default="researchr.json",
        type=str,
        help="JSON file from Researchr",
    )

    parser.add_argument("--out", default="calendar.csv", help="output file")

    return parser.parse_args()


researchrToTrack = {
    "SOAP": "soap",
    "PLDI Fake Track": "soap",
    "PLDI-A": "pldi-a",
    "PLDI-B": "pldi-b",
    "IMOP": "imop",
    "PLMW@PLDI": "plmw",
    "ARRAY": "array",
    "LCTES": "lctes",
    "HOPL IV": "hopl",
    "ISMM": "ismm",
    "PLanQC": "planqc",
    "Infer Practitioners": "infer",
    "MAPS": "maps",
    "PLDI Tutorials": "tutorials",
}


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
        s
        for s in jsonData["Sessions"]
        if (s["Location"].split("Online | ")[1] == room and "Items" in s)
    ]
    sortedEvents = list(sorted(sessions, key=sessionTime))
    events = [e for s in sortedEvents for e in s["Items"]]
    return events


def chairsForEvent(jsonData, key):
    for s in jsonData["Sessions"]:
        if key in s.get("Items", []):
            return s.get("ChairsString", "")
    return ""


def convert(args):

    file_ics: str = args.ics
    if not file_ics.startswith("http"):
        with open(file_ics, "r") as f:
            c = Calendar(f.read())
    else:
        c = Calendar(requests.get(file_ics).text)

    file_json: str = args.json
    with open(file_json, "r") as f:
        jsonData = json.load(f)

    types = [
        (typeOfEvent(jsonData, x), chairsForEvent(jsonData, x))
        for x in collectEventKeys(jsonData, args.room)
    ]

    regex = "\[([^\\]]*)\] (.*)"
    pattern = re.compile(regex)

    eastern = pytz.timezone("US/Eastern")

    with (open(args.out, "w")) as f:
        f.write("event,date,start,end,title,authors,notes,session chairs\n")
        roomEvents = [
            x
            for x in c.events
            if x.location.split(" - ")[0].strip() == args.room
            and x.name.startswith("[")
        ]
        sortedEvents = list(sorted(roomEvents, key=lambda c: c.begin))
        assert len(types) == len(sortedEvents)
        for e, (t, chairs) in zip(sortedEvents, types):
            parts = e.name.rsplit(" - ", 1)
            title = parts[0]
            m = pattern.match(title)
            event = researchrToTrack[m.group(1).strip()]
            title = m.group(2)
            if len(parts) > 1:
                authors = parts[1].split(", ")
            else:
                authors = ""

            authors = ", ".join(authors)
            authors = unidecode.unidecode(authors)

            if chairs != "":
                chairs = f',"{chairs}"'

            if t != "Social Event":
                extra = ""
                if t == "Live Q&A":
                    extra = "Discussion or post-talk Q&A in Zoom"

                f.write(
                    f'{event},{e.begin.astimezone(None).strftime("%Y-%m-%d")},{e.begin.astimezone(None).strftime("%H:%M")},{e.end.astimezone(None).strftime("%H:%M")},"{title}","{authors}","{extra}"{chairs}\n'
                )


if __name__ == "__main__":
    args = parse_arguments()
    convert(args)
