import csv
import io
import json
import time
import zlib
import sys
import os

import requests
import yaml
from jinja2 import Environment, PackageLoader, select_autoescape, FileSystemLoader

current_directory = os.path.dirname(os.path.abspath(__file__))
env = Environment(
    loader=FileSystemLoader(current_directory),
    autoescape=select_autoescape(['html', 'xml'])
)

config = yaml.load(open("../admin/config.yml").read(), Loader=yaml.SafeLoader) | yaml.load(open("config.yml").read(), Loader=yaml.SafeLoader)
rooms = yaml.load(open("poster-rooms.yml").read(), Loader=yaml.SafeLoader)
calendar = list(csv.DictReader(open(config["sitedata"] + "/calendar_papers.csv")))
pldi_tracks = list(csv.DictReader(open(config["sitedata"] + "/track_pldi.csv")))
papers = list(csv.DictReader(open(config["sitedata"] + "/papers.csv")))

def getPaperInfo(paper):
    paperInfo = next(x for x in papers if x["UID"] == paper["paperUID"])
    return (paperInfo["title"],paperInfo["authors"].split("|"),paper["posterNumber"])

def createDirectory(room):

    # tuple of (session name, list of (title,authors,posterNumber))
    sessions = [(next(x["title"] for x in pldi_tracks if x["UID"] == session),
      sorted([getPaperInfo(x) for x in calendar if x["session"] == session], key=lambda x: int(x[2]))) for session in room["sessions"]]
    template = env.get_template('templates/directory.html')
    html = template.render(sessions=sessions)
    with open(f"build/directory-{room['UID']}.html", "w") as f:
        f.write(html)

def createFullDirectory(rooms):

    # tuple of (session name, list of (title,authors,posterNumber))
    sessions = [(next(x["title"] for x in pldi_tracks if x["UID"] == session),
      sorted([getPaperInfo(x) for x in calendar if x["session"] == session], key=lambda x: int(x[2]))) for room in rooms for session in room["sessions"]]
    template = env.get_template('templates/directory.html')
    html = template.render(sessions=sessions)
    with open(f"build/directory.html", "w") as f:
        f.write(html)


if __name__ == "__main__":
    createFullDirectory(rooms)
    for room in rooms:
        createDirectory(room)
    