import csv
import io
import json
import time
import zlib
import sys
import os

import requests
import yaml

config = yaml.load(open("../admin/config.yml").read(), Loader=yaml.SafeLoader) | yaml.load(open("config.yml").read(), Loader=yaml.SafeLoader)
mySpace = config["gather_space_id"]
rooms = yaml.load(open("poster-rooms.yml").read(), Loader=yaml.SafeLoader)
assets = yaml.load(open("auto/assets.yml").read(), Loader=yaml.SafeLoader)
calendar = list(csv.DictReader(open(config["sitedata"] + "/calendar_papers.csv")))

def getNonPosterObjects(map):
    return [o for o in map["objects"] if o.get("_name", "") != "poster"]

def positionKey(p):
    return (p["y"], p["x"])

def getPosterObjects(map):
    posters = [o for o in map["objects"] if o.get("_name", "") == "poster"]
    return sorted(posters, key=positionKey)

def createDefaultPosters(room, map):
    posters = getPosterObjects(map)
    start = room["start"]
    for i in range(len(posters)):
        posters[i]["properties"] = {  }
        posters[i]["normal"] = assets[f"default_{i + start}"]
        posters[i]["highlighted"] = assets[f"default_{i + start}"]
        posters[i]["distThreshold"] = "1"
        posters[i]["width"] = "9"
        posters[i]["height"] = "8"

    nonPoster = getNonPosterObjects(map)
    nonPoster.extend(posters)
    map["objects"] = nonPoster

def addUserPostersForSession(room, map, session):
    posters = getPosterObjects(map)
    papers = [x for x in calendar if x["session"] == session]
    start = room["start"]
    for paper in papers:
        paperUID = paper["paperUID"]
        posterNumber = paper["posterNumber"]
        print(paper)
        i = int(posterNumber) - start   # index into object array
        if i < len(posters):
            posterPNG = config["amplify_domain"] + f"/poster_{paperUID}.png"
            posters[i]["normal"] = assets[f"user_{i + start}"]
            posters[i]["highlighted"] = assets[f"user_{i + start}"]
            posters[i]["distThreshold"] = "0"
            posters[i]["properties"] = {
                "blurb" : f"poster {posterNumber}. position {i}. poster {paperUID}.",
                "image": posterPNG,
                "preview": posterPNG,
            }
    
    nonPoster = getNonPosterObjects(map)
    nonPoster.extend(posters)
    map["objects"] = nonPoster

def addDirectoryToPlant(room, map):
    plant = next(x for x in map["objects"] if x.get("_name", "") == "Potted Plant (directory)")
    plant["properties"] = {
            # "url": config["amplify_domain"] + f"/directory-{room['UID']}.html"
            "url": config["amplify_domain"] + f"/directory.html"   # go with one big list for now...
        }

def createRoom(room):
    map = json.load(open(room["template"]))
    map["backgroundImagePath"] = assets[room["background"]]
    if "foreground" in room:
        map["foregroundImagePath"] = assets[room["foreground"]]
    createDefaultPosters(room, map)
    for session in room["sessions"]:
        addUserPostersForSession(room, map, session)
    addDirectoryToPlant(room, map)
    with open(f'auto/room-{room["UID"]}.json', 'w') as outfile:
        json.dump(map, outfile, indent=2, sort_keys=True)

if __name__ == "__main__":
    for room in rooms:
        createRoom(room)
