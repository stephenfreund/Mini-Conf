# pylint: disable=global-statement,redefined-outer-name
import argparse
import csv
import glob
import json
import os
from collections import OrderedDict, UserList, defaultdict
from datetime import datetime, timedelta
from itertools import chain, groupby
from typing import Any, DefaultDict, Dict, List

import pandas
import pytz
import yaml

from libgather import Gather
from libauth0 import Auth0
from libregmaster import RegMaster

import requests


if __name__ == "__main__":
    global config
    config = yaml.load(open("config.yml").read(), Loader=yaml.SafeLoader)

    rm = RegMaster(config["regmaster_password"], config["regmaster_endpoint"])
    registered = set([x["email"] for x in rm.allRegistered()])

    auth0 = Auth0(config["auth0_domain"], config["auth0_connection"], config["auth0_client_id"], config["auth0_client_secret"])        
    inAuth0 = set([x["email"] for x in auth0.userList()])

    toJoin = set(inAuth0)
    print("email")
    for t in registered:
        if t not in inAuth0:
            print(t)

