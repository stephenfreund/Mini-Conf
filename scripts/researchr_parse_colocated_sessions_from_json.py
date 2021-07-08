#!/usr/bin/env python3
#
#
# Note: JSON file must have times in EDT.
#

import argparse
import csv
import json
import re
from collections import OrderedDict, defaultdict
from datetime import datetime

import requests
from ics.icalendar import Calendar
from pytz import timezone

tracks = list(csv.DictReader(open("../sitedata/tracks.csv")))

by_uid = {}
for p in tracks:
    by_uid[p["UID"]] = p


colocated = [x for x in tracks if "pldi" not in x["UID"]]


def parse_arguments():
    parser = argparse.ArgumentParser(description="MiniConf Calendar Command Line")

    parser.add_argument(
        "--json",
        default="sample_cal.json",
        type=str,
        help="JSON file to parse (local or via http)",
    )

    parser.add_argument(
        "--ics",
        default="sample_cal.ics",
        type=str,
        help="ICS file to parse (local or via http)",
    )

    parser.add_argument("--out", default="a.csv", help="output file")

    return parser.parse_args()


specialLocations = {
    "Infer Practitioners": "Infer",
    "Tutorials: Beyond Weak Memory Consistency": "Persist",
    "HOPL": "HOPL IV",
}


def findTrack(location):
    location = specialLocations.get(location, location)
    for track in colocated:
        if location == track["conf_abbrev"]:
            return track
    return None


def makeISO(date, time):
    return date + "T" + time + ":00-04:00"


counters = OrderedDict()


def makeUID(track):
    counter = counters.get(track, 0)
    counters[track] = counter + 1
    return f"pldi_{track}.{counter}"


def adjustStartAndEnd(calendar, room, start, end):
    roomEvents = [
        x for x in calendar.events if x.location.split(" - ")[0].strip() == room
    ]

    afterStart = [
        x.begin for x in sorted(roomEvents, key=lambda c: c.begin) if start <= x.begin
    ] + [start]
    beforeEnd = [end] + [
        x.end for x in sorted(roomEvents, key=lambda c: c.end) if x.end <= end
    ]

    newStart = afterStart[0]
    newEnd = beforeEnd[-1]
    if start != newStart or end != newEnd:
        print("Session is bigger than events in it:")
        print(
            f"  start: {room} {start} -> {newStart.astimezone(timezone('America/New_York'))}"
        )
        print(
            f"    end: {room} {end} -> {newEnd.astimezone(timezone('America/New_York'))}"
        )

    return (
        newStart.astimezone(timezone("America/New_York")),
        newEnd.astimezone(timezone("America/New_York")),
    )


# pylint: disable=redefined-outer-name
def convert(args):
    file_json: str = args.json
    with open(file_json, "r") as f:
        c = json.load(f)

    file_ics: str = args.ics
    if not file_ics.startswith("http"):
        with open(file_ics, "r") as f:
            cal = Calendar(f.read())
    else:
        cal = Calendar(requests.get(file_ics).text)

    with (open(args.out, "w")) as f:
        f.write(
            "UID,title,start,end,trackUID,gather,zoom,info_link,category,session_chairs\n"
        )
        for e in c["Sessions"]:
            loc = e["Location"].split("Online | ")[1]
            room = loc
            rTitle = e["Title"]

            if "Tutorials" in loc:
                if "Weak" in e["Title"]:
                    loc = "Persist"
                    rTitle = "Memory Persistency Tutorial"
                elif "IMOP" in e["Title"]:
                    loc = "IMOP"
                    rTitle = "IMOP Tutorial"
                else:
                    loc = "Contracts"
                    rTitle = "Smart Contracts Security Analysis Tutorial"

            times = e["Time"].split(" - ")
            start = makeISO(e["Day"], times[0])
            end = makeISO(e["Day"], times[1])

            start, end = adjustStartAndEnd(
                cal, room, datetime.fromisoformat(start), datetime.fromisoformat(end)
            )

            # colocated
            track = findTrack(loc)
            if track != None:
                # UID,title,start,end,trackUID,gather,zoom,info_link,category
                if "Tutorial" in rTitle:
                    title = rTitle
                elif ":" in rTitle:
                    title = (
                        track["title"] + ": " + rTitle.split(":")[1].strip()
                    )  # track["title"]
                else:
                    title = track["title"]

                uid = makeUID(track["UID"])
                trackUID = track["UID"]
                chairs = e.get("ChairsString", "")
                infoLink = f"/track_{trackUID}.html"
                category = "colocated-session"
                f.write(
                    f'{uid},"{title}",{start},{end},{trackUID},,,{infoLink},{category},"{chairs}"\n'
                )


if __name__ == "__main__":
    args = parse_arguments()
    convert(args)
