import csv
import io
import json
import time
import zlib
import sys

import requests
import yaml

from libgather import Gather

if __name__ == "__main__":
    roomName = sys.argv[1]
    jsonContents = sys.argv[2]
    config = yaml.load(open("../admin/config.yml").read(), Loader=yaml.SafeLoader) | yaml.load(open("config.yml").read(), Loader=yaml.SafeLoader)

    gather = Gather(config["gather_api_key"], config["gather_space_id"])

    with open(jsonContents) as f:
        data = json.load(f)

    gather.setMap(roomName, data)
