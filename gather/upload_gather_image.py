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

def uploadGatherImage(mySpace, key, image):
    url = os.popen(f"node gather_upload_image.js {mySpace} {image}").read().strip('\n')
    with open("auto/assets.yml", "a") as f:
        f.write(f"\"{key}\": \"{url}\"\n")

if __name__ == "__main__":
    key = sys.argv[1]
    image = sys.argv[2]
    config = yaml.load(open("../admin/config.yml").read(), Loader=yaml.SafeLoader) | yaml.load(open("config.yml").read(), Loader=yaml.SafeLoader)
    uploadGatherImage(config['gather_space_id'], key, image)
