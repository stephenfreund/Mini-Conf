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
        imageFromCPC = f"pictures/pldi21main-p{id}-p-ThumbnailPicture.png"
        # posterFromCPC = f"pictures/pldi21main-p{id}-p-PosterPicture.png"
        if os.path.exists(imageFromCPC):
            pi = f"../static/paper_images/pldi.{id}.png"
            if True or not os.path.exists(pi) or os.path.getmtime(pi) < os.path.getmtime(imageFromCPC):
                print(f"New file: {imageFromCPC}")
                os.system(f"convert {imageFromCPC}  -resize 600x600\>  {pi}")
            # shutil.copyfile(imageFromCPC, f"../static/paper_images/pldi.{id}.png" )
            done.append(id)
        else:
            shutil.copyfile("default-thumbnail.png", f"../static/paper_images/pldi.{id}.png" )
            notDone.append(id)
    
    print(f"Not Done({len(notDone)}): {notDone}")
    print(f"Done({len(done)}):     {done}")    