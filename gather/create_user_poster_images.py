import csv
import io
import json
import time
import zlib
import sys
import os

import requests
import yaml
import upload_gather_image
import argparse

config = yaml.load(open("../admin/config.yml").read(), Loader=yaml.SafeLoader) | yaml.load(open("config.yml").read(), Loader=yaml.SafeLoader)
mySpace = config["gather_space_id"]
rooms = yaml.load(open("poster-rooms.yml").read(), Loader=yaml.SafeLoader)
assets = yaml.load(open("auto/assets.yml").read(), Loader=yaml.SafeLoader)
calendar = list(csv.DictReader(open(config["sitedata"] + "/calendar_papers.csv")))
papers = dict([(x["UID"], x) for x in list(csv.DictReader(open(config["sitedata"] + "/papers.csv")))])


def parse_arguments():
    parser = argparse.ArgumentParser(description="MiniConf Calendar Command Line")
    parser.add_argument("-d", default=False, action='store_true')

    return parser.parse_args()

def buildUserPoster(mySpace, initialPoster, posterNumber, paperNumber, title):
    fileName = f"user_{posterNumber}.png"
    command = f"convert -background transparent {initialPoster} -fill white -font ArialNarrowB -pointsize 36 -annotate +26+38 '%2.2d' /tmp/{fileName}" % posterNumber
    os.system(command)

    command = f'convert -background transparent  -fill LightSteelBlue1 -font fonts/Lato-Bold.ttf -pointsize 14 -size 192x50  -gravity North caption:"{title}" /tmp/title.png'
    os.system(command)

    os.system(f"composite -background transparent -geometry  +64+0 /tmp/title.png /tmp/{fileName} /tmp/{fileName}")

    author_thumb = f"../author-content/pictures/pldi21main-p{paperNumber.split('.')[1]}-p-ThumbnailPicture.png"
    if os.path.exists(author_thumb):
        print(f"{paperNumber} *")
        #os.system(f"convert {author_thumb} -background white -alpha remove -bordercolor white -border 5 -gravity center /tmp/x.png")
        os.system(f"convert {author_thumb} -alpha remove -gravity center /tmp/x.png")

        os.system(f"convert /tmp/x.png -resize 256x148 -background none -gravity center -extent 288x160 /tmp/img.png")
    else:
        print(f"{paperNumber}")
        os.system(f"convert ../author-content/default-thumbnail.png  -resize 256x148 -background none -gravity center -extent 288x160 /tmp/img.png")

    os.system(f"composite -background transparent -geometry  +0+96 /tmp/img.png /tmp/{fileName} /tmp/{fileName}")

    if not dryRun:
        upload_gather_image.uploadGatherImage(mySpace, f"user_{posterNumber}", f"/tmp/{fileName}" )


def buildDefaultPoster(mySpace, initialPoster, posterNumber):
    fileName = f"user_{posterNumber}.png"
    command = f"convert -background transparent {initialPoster} -fill white -font ArialNarrowB -pointsize 36 -annotate +26+38 '%2.2d' /tmp/{fileName}" % posterNumber
    os.system(command)

    if not dryRun:
        upload_gather_image.uploadGatherImage(mySpace, f"default_{posterNumber}", f"/tmp/{fileName}" )


def addUserPostersForSession(room, map, session):
    spapers = [x for x in calendar if x["session"] == session]
    for paper in spapers:
        paperUID = paper["paperUID"]
        posterNumber = int(paper["posterNumber"])
        buildUserPoster(mySpace, "gather-assets/gray-9x8.png", posterNumber, paperUID, papers[paperUID]["title"])
    


def createRoom(room):
    for session in room["sessions"]:
        addUserPostersForSession(room, map, session)

if __name__ == "__main__":
    dryRun = parse_arguments().d
    for room in rooms:
        createRoom(room)

