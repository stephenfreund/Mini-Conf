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
rooms = yaml.load(open("poster-rooms.yml").read(), Loader=yaml.SafeLoader)
assets = yaml.load(open("auto/assets.yml").read(), Loader=yaml.SafeLoader)
calendar = list(csv.DictReader(open(config["sitedata"] + "/calendar_papers.csv")))

# https://gather.town/app/fqYKZyOAnXGK2J7U/posterRoomE3?spawnx=7&spawny=9&map=custom-entrance

def positionKey(p):
    return (p["y"], p["x"])

def getPosterObjects(map):
    posters = [o for o in map["objects"] if o.get("_name", "") == "poster"]
    return sorted(posters, key=positionKey)
        
def createPosterPinPointers(room):
    map = json.load(open(room["template"]))
    posters = getPosterObjects(map)
    start = room["start"]
    for i in range(len(posters)):
        x = posters[i]["x"] + 4
        y = posters[i]["y"] + 5
        roomName = f'room-{room["UID"]}'
        query = f'?spawnx={x}&spawny={y}&map={roomName}'
        print('Gather Poster %2.2d: %s' % (i + start,query))

if __name__ == "__main__":
    for room in rooms:
        createPosterPinPointers(room)
