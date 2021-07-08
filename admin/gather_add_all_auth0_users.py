#!/usr/bin/env python3

import csv
import io
import json
import time
import zlib

import requests
import yaml

from libgather import Gather
from libauth0 import Auth0


def makeGatherEmailDictionary(auth0Users):
    return dict([(x["email"], { }) for x in auth0Users])


if __name__ == "__main__":
    config = yaml.load(open("config.yml").read(), Loader=yaml.SafeLoader)

    gather = Gather(config["gather_api_key"], config["gather_space_id"])
    originalGatherDict = gather.getGatherEmailDictionary()

    auth0 = Auth0(config["auth0_domain"], config["auth0_connection"], config["auth0_client_id"], config["auth0_client_secret"])
    
    # remove any blocked users
    users = [x for x in auth0.userList() if not x.get("blocked", False)]

    # remove any blacklisted users
    blacklist = yaml.load(requests.get(config["blacklist"]).text, Loader=yaml.SafeLoader)
    users = [x for x in users if x["email"] not in blacklist]

    emailDict = makeGatherEmailDictionary(users)

    gather.setGatherEmailDictionary(
        emailDict,
        len(originalGatherDict) == 0,
    )

    gatherDict = gather.getGatherEmailDictionary()
    
    added = "\n".join(sorted([x for x in gatherDict if x not in originalGatherDict]))
    print("Added:")
    print(added)
