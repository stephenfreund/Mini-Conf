import csv
import io
import json
import time

import requests
import yaml

from libgather import Gather

if __name__ == "__main__":
    config = yaml.load(open("../admin/config.yml").read(), Loader=yaml.SafeLoader) | yaml.load(open("config.yml").read(), Loader=yaml.SafeLoader)

    gather = Gather(config["gather_api_key"], config["gather_space_id"])
    originalGatherDict = gather.getGatherEmailDictionary()

    for i in range(50):
        emailDict = { f"d{i}": {"name": f"name{i}"} }
        gather.setGatherEmailDictionary(
            emailDict,
            len(originalGatherDict) == 0,
        )
        gatherDict = gather.getGatherEmailDictionary()
        added = [x for x in gatherDict if x not in originalGatherDict]
        print("Added: " + (" ".join(added)))
        # time.sleep(.1)

