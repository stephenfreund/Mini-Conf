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

config = yaml.load(open("../admin/config.yml").read(), Loader=yaml.SafeLoader) | yaml.load(open("config.yml").read(), Loader=yaml.SafeLoader)
mySpace = config["gather_space_id"]
rooms = yaml.load(open("poster-rooms.yml").read(), Loader=yaml.SafeLoader)
assets = yaml.load(open("auto/assets.yml").read(), Loader=yaml.SafeLoader)
calendar = list(csv.DictReader(open(config["sitedata"] + "/calendar_papers.csv")))
papers = dict([(x["UID"], x) for x in list(csv.DictReader(open(config["sitedata"] + "/papers.csv")))])


def buildDefaultPoster(mySpace, initialPoster, posterNumber):
    fileName = f"user_{posterNumber}.png"
    command = f"convert -background transparent {initialPoster} -fill white -font ArialNarrowB -pointsize 36 -annotate +26+38 '%2.2d' /tmp/{fileName}" % posterNumber
    os.system(command)

    upload_gather_image.uploadGatherImage(mySpace, f"default_{posterNumber}", f"/tmp/{fileName}" )

if __name__ == "__main__":
    for i in range(1,100):
        buildDefaultPoster(mySpace, "gather-assets/gray-9x8.png", i)

    upload_gather_image.uploadGatherImage(mySpace, "fancy-background", "gather-assets/new-background-big.png")
    upload_gather_image.uploadGatherImage(mySpace, "fancy-foreground", "gather-assets/new-foreground-big.png")
    upload_gather_image.uploadGatherImage(mySpace, "fancy-background-green", "gather-assets/new-background-big-green.png")
    upload_gather_image.uploadGatherImage(mySpace, "fancy-background-purple", "gather-assets/new-background-big-purple.png")

