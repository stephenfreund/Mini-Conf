import csv
import io
import json
import time
import zlib
import sys

import requests
import yaml

sys.path.append("../admin")

from libgather import Gather

if __name__ == "__main__":
    roomName = sys.argv[1]
    config = yaml.load(open("../admin/config.yml").read(), Loader=yaml.SafeLoader) | yaml.load(open("config.yml").read(), Loader=yaml.SafeLoader)

    gather = Gather(config["gather_api_key"], config["gather_space_id"])

    map = gather.getMap(roomName)
    print(json.dumps(map, indent=2, sort_keys = True))
