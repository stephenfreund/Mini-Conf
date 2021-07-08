import csv
import io
import json
import time
import zlib
import sys
import os
import shutil

import requests
import yaml

config = yaml.load(open("../admin/config.yml").read(), Loader=yaml.SafeLoader) | yaml.load(open("config.yml").read(), Loader=yaml.SafeLoader)

papers = list(csv.DictReader(open(config["sitedata"] + "/papers.csv")))

if __name__ == "__main__":
    done = []
    notDone = []
    for paper in papers:
        id = paper["UID"].split(".")[1]
        imageFromCPC = f"pictures/pldi21main-p{id}-p-PosterPicture.png"
        if os.path.exists(imageFromCPC):
            done.append(id)
        else:
            notDone.append(id)
    
    print(f"Not Done({len(notDone)}): {notDone}")
    print(f"Done({len(done)}):     {done}")    