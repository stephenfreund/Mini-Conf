import csv
import io
import json
import time
import zlib
import sys
import os

import requests
import yaml
from libgather import Gather


if __name__ == "__main__":
    config = yaml.load(open("../admin/config.yml").read(), Loader=yaml.SafeLoader) | yaml.load(open("config.yml").read(), Loader=yaml.SafeLoader)
    rooms = yaml.load(open("poster-rooms.yml").read(), Loader=yaml.SafeLoader)
    gather = Gather(config["gather_api_key"], config["gather_space_id"])
    for room in rooms:
        roomName = f'room-{room["UID"]}'
        jsonContents = json.load(open(f'auto/room-{room["UID"]}.json'))
        gather.setMap(roomName, jsonContents)
