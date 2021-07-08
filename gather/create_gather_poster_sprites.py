import csv
import io
import json
import time
import zlib
import sys
import os
import random

import requests
import yaml

import upload_gather_image

def buildPosters(mySpace, initialPosters, n):
    for i in range(1,n+1):
        fileName = f"poster{i}.png"
        command = f"convert {random.choice(initialPosters)} -fill white -font ArialNarrowB -pointsize 36 -annotate +26+38 '%2.2d' /tmp/{fileName}" % i
        os.system(command)
        upload_gather_image.uploadGatherImage(mySpace, f"poster_{i}", f"/tmp/{fileName}" )

if __name__ == "__main__":
    count = int(sys.argv[1])
    config = yaml.load(open("../admin/config.yml").read(), Loader=yaml.SafeLoader)
    mySpace = config["gather_space_id"]
    buildPosters(mySpace, [ "gather-assets/gray-9x8.png" ], count) 

    upload_gather_image.uploadGatherImage(mySpace, "background", "gather-assets/new-poster-test-bg.png")
    upload_gather_image.uploadGatherImage(mySpace, "foreground", "gather-assets/with-aisles-5x5-border-foreground.png")
