import csv
import io
import json
import time
import zlib
import sys
import os

import requests
import yaml

def buildPosters(initialPoster, n):
    for i in range(1,n+1):
        fileName = f"poster{i}.png"
        command = f"convert {initialPoster} -fill white -font ArialNarrowB -pointsize 36 -annotate +44+58 '%2.2d' /tmp/{fileName}" % i
        os.system(command) 
        url = os.popen(f"node gather_upload_image.js /tmp/{fileName}").read()
        print(f"{i}: {url}")

def getPosterTemplate():
    with open("gather-assets/poster-room.json") as f:
        return json.load(f)

def getNonPosterObjects(room):
    return [o for o in room["objects"] if o.get("_name", "") != "6x6 Poster"]

def positionKey(p):
    return (p["x"], p["y"])

def getPosterObjects(room):
    posters = [o for o in room["objects"] if o.get("_name", "") == "6x6 Poster"]
    return sorted(posters, key=positionKey)

def updatePosterObjects(room):
    nonPoster = getNonPosterObjects(room)
    poster = getPosterObjects(room)
    for i in range(len(poster)):
        poster[i]["properties"] = {
            "blurb": "poster",
            "image": f"https://pldi21.org/static/images/gather/poster{i+1}.png",
            "preview": f"https://pldi21.org/static/images/gather/poster{i+1}.png"
        }
        poster[i]["normal"] = "https://cdn.gather.town/storage.googleapis.com/gather-town.appspot.com/uploads/QhP7jFle1OkT4QRP/FhhWxij2rJ7iru5qyXsA5Z"
        poster[i]["highlighted"] = "https://cdn.gather.town/storage.googleapis.com/gather-town.appspot.com/uploads/QhP7jFle1OkT4QRP/FhhWxij2rJ7iru5qyXsA5Z"
        # poster[i]["normal"] = f"https://pldi21.org/static/images/gather/poster{i+1}.png"
        # poster[i]["highlighted"] = f"https://pldi21.org/static/images/gather/poster{i+1}.png"
        
    nonPoster.extend(poster)
    room["objects"] = nonPoster

if __name__ == "__main__":
    os.system("cp gather-assets/poster-room-background.png ../static/images/gather/poster-room-background.png")
    buildPosters("gather-assets/purple-6x6.png", 27)
    room = getPosterTemplate()
    updatePosterObjects(room)
    print(json.dumps(room, indent=2, sort_keys=True))