# pylint: disable=global-statement,redefined-outer-name
import argparse
import csv
import glob
import json
import os
from collections import OrderedDict, defaultdict
from datetime import datetime, timedelta
from itertools import chain, groupby
from typing import Any, DefaultDict, Dict, List

import pandas
import pytz
import yaml
from flask import Flask, jsonify, redirect, render_template, send_from_directory
from flask_frozen import Freezer
from flaskext.markdown import Markdown

from libgather import Gather
from libauth0 import Auth0
from libregmaster import RegMaster

import requests

config = {}

###

def main(site_data_path):
    global config
    config = yaml.load(open("config.yml").read(), Loader=yaml.SafeLoader)
    return ["config.yml"]

###


###


app = Flask(__name__)
app.config.from_object(__name__)

@app.route("/")
def index():
    return redirect("/index.html")

@app.route("/index.html")
def login():
    data = {}

    print("Starting...")

    rm = RegMaster(config["regmaster_password"], config["regmaster_endpoint"])
    registeredAndPaid = set([x["email"] for x in rm.allRegistered()])
    registered = rm.allRegisteredWithUnpaid()
    print("Got RegMaster...")

    auth0 = Auth0(config["auth0_domain"], config["auth0_connection"], config["auth0_client_id"], config["auth0_client_secret"])        
    inAuth0 = sorted(auth0.userList(), key=lambda x : x["email"])

    print("Got Auth0...")

    gather = Gather(config["gather_api_key"], config["gather_space_id"])
    inGather = gather.getGatherEmailDictionary().keys()
    blacklist = yaml.load(requests.get(config["blacklist"]).text, Loader=yaml.SafeLoader)

    print("Got Gather...")

    names = dict([(x["email"], x["name"]) for x in registered])

    allEmails = set(names.keys())
    allEmails = allEmails.union(set([x["email"] for x in inAuth0]))
    allEmails = allEmails.union(set(inGather))
    allEmails = allEmails.union(set(blacklist))

    info = []
    for email in sorted(allEmails):

        inRegMaster = email in names
        paid = email in registeredAndPaid

        signedOn = False
        blocked = False
        for x in inAuth0:
            if x["email"] == email:
                signedOn = True
                s = x.get("blocked", "false")
                if s == "true":
                    print(str(x) + " " + s)
                    blocked = True

        info.append( {
            "order": len(info) + 1,
            "email": email,
            "name": names.get(email, "??"),
            "registered": inRegMaster,
            "paid": paid,
            "website": signedOn,
            "blocked": blocked,
            "gather": email in inGather,
            "blacklisted": email in blacklist
        })

    data["users"] = info
    # print(data)
    return render_template("index.html", **data)


if __name__ == "__main__":
    site_data_path = "."
    extra_files = main(site_data_path)

    debug_val = False
    if os.getenv("FLASK_DEBUG") == "True":
        debug_val = True

    app.run(host="0.0.0.0", port=5001, debug=debug_val, extra_files=extra_files)
