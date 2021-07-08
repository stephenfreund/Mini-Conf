import csv
import io
import json
import time
import zlib
import sys
import os
import yaml

styles = yaml.load(open("styles.yml").read(), Loader=yaml.SafeLoader)
signs = csv.DictReader(open("signs.csv"))


COMMAND = """
    convert -background transparent  -fill %s -font %s -pointsize %d -size %dx  \
    %s caption:"%s" signs/%s
   """

def nameForCaption(text, id):
    t = "-".join(text.split(" ")[0:4])
    c = [x.lower() for x in t if x.isalnum() or x == "-"]
    return str(id) + "-" + "".join(c)[:60] + ".png"


def makeCaption(caption, id):
    style = styles[caption["style"]]
    text = caption["text"]
    command = COMMAND % (style["color"], style["font"], style["size"], int(caption["squares"]) * 32, style.get("extras", ""), text, nameForCaption(text, id))
    os.system(command)

if __name__ == "__main__":
    for index, c in enumerate(signs):
        makeCaption(c, index)
