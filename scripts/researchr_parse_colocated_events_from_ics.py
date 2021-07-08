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
        "--room",
        default="SOAP",
        type=str,
        help="Researchr room we're processing",
    )

    parser.add_argument(
        "--ics",
        default="sample_cal.ics",
        type=str,
        help="ICS file to parse (local or via http)",
    )

    parser.add_argument(
        "--json",
        default="sample_cal.json",
        type=str,
        help="JSON file to parse (local or via http)",
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
}


def makeISO(date, time):
    return date + "T" + time + ":00-04:00"


def sessionTime(session):
    times = session["Time"].split(" - ")
    start = makeISO(session["Day"], times[0])
    return start


def typeOfEvent(jsonData, key):
    return [x["Type"] for x in jsonData["Items"] if x["Key"] == key][0]


def urlOfEvent(jsonData, key):
    return [x.get("URL", "") for x in jsonData["Items"] if x["Key"] == key][0]


def collectEventKeys(jsonData, room):
    sessions = [
        s
        for s in jsonData["Sessions"]
        if (s["Location"].split("Online | ")[1] == room and "Items" in s)
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

    file_json: str = args.json
    with open(file_json, "r") as f:
        jsonData = json.load(f)

    types = [typeOfEvent(jsonData, x) for x in collectEventKeys(jsonData, args.room)]
    urls = [urlOfEvent(jsonData, x) for x in collectEventKeys(jsonData, args.room)]

    regex = "\[([^\\]]*)\] (.*)"
    pattern = re.compile(regex)

    with (open(args.out, "w")) as f:
        f.write(
            "event,start,end,title,authors,category,trackUID,gather,zoom,info_link\n"
        )
        roomEvents = [
            x
            for x in c.events
            if x.location.split(" - ")[0].strip() == args.room
            and x.name.startswith("[")
        ]
        sortedEvents = list(sorted(roomEvents, key=lambda c: c.begin))
        # for e,t in zip(sortedEvents, types):

        #     print (f"{e.name} {e.begin} {e.end}: {t} {e}")

        # print(len(types))
        # print(len(sortedEvents))
        assert len(types) == len(sortedEvents)
        for e, t, url in zip(sortedEvents, types, urls):
            parts = e.name.rsplit(" - ", 1)
            title = parts[0]
            m = pattern.match(title)
            event = researchrToTrack[m.group(1).strip()]
            title = m.group(2)
            title = title.replace('"', "&quot;")
            # print(url)
            if len(parts) > 1:
                authors = parts[1].split(", ")
            else:
                authors = ""

            if t == "Social Event":
                f.write(
                    f'{event},{e.begin.for_json()},{e.end.for_json()},"{title}",{"|".join(authors)},gather,,Gather,,{url}\n'
                )
            elif t == "Live Q&A":
                f.write(
                    f'{event},{e.begin.for_json()},{e.end.for_json()},"{title}",{"|".join(authors)},colocated,{event},,Q&A in Zoom,{url}\n'
                )
            elif t == "Break" or t == "Coffee break":
                f.write(
                    f'{event},{e.begin.for_json()},{e.end.for_json()},"{title}",{"|".join(authors)},break,{event},,,\n'
                )
            else:
                f.write(
                    f'{event},{e.begin.for_json()},{e.end.for_json()},"{title}",{"|".join(authors)},colocated,{event},,,{url}\n'
                )


if __name__ == "__main__":
    args = parse_arguments()
    convert(args)
