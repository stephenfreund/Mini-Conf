import csv
import io
import json
import time
import zlib
import sys
import os

import requests
import yaml

COMMAND = """
    convert -background transparent  -fill LightSteelBlue1 -font fonts/Lato-Bold.ttf -pointsize 14 -size 160x50  -gravity North \
    caption:"%s" %s
   """


def build(paper):
    title = paper["title"]
    output = f"build/title_{paper['UID']}.png"
    command = COMMAND % (title, output) 
    print(command)
    os.system(command) 

if __name__ == "__main__":
    config = yaml.load(open("../admin/config.yml").read(), Loader=yaml.SafeLoader) | yaml.load(open("config.yml").read(), Loader=yaml.SafeLoader)
    papers = list(csv.DictReader(open(config["sitedata"] + "/papers.csv")))
    for p in papers:
        build(p)


# <markup><!--
# This is of course a SGML/XML comment which can be ignored and
# as such can also be used to add hidden newlines into this demo.

# Markup language syntax...
#   http://www.pygtk.org/docs/pygtk/pango-markup-language.html
#   http://www.ibm.com/developerworks/library/l-u-pango1/

# Viewing this file...
#   pango-view --dpi=72 --markup pango_test.txt

#   convert pango:@pango_test.txt show:

# --><span size="49152">Pango Markup Demo</span>
# Size: <small><small><small>smallest</small> smaller</small> small</small><!--
# -->  normal <!--
# --> <big>big <big>bigger <big>biggest</big></big></big>

# Styles:<!--
# --> <b>bold</b><!--
# --> <i>italic</i><!--
# --> <u>underlined</u><!--
# --> <s>strikethrough</s><!--
# --> <tt>monospaced</tt>

# <sup>superscript</sup> --normal-- <sub>subscript</sub>

# Underline:<!--
# --> <span underline="single">single</span><!--
# --> <span underline="double">double</span><!--
# --> <span underline="low">low</span><!--
# --> <span underline="error">error</span>

# Colors:<!--
# --> <span fgcolor="red">red</span><!--
# --> <span fgcolor="blue">blue</span><!--
# --> -- <!--
# --> <span bgcolor="yellow">yellow bg</span><!--
# --> <span bgcolor="skyblue">skyblue bg</span><!--
# --> -- <!--
# --> <span underline_color="blue"><u>underline</u></span><!--
# --> <span strikethrough_color="red"><s>strikethrough</s></span>

# Rise: ---<!--
# --><span rise="10240">-</span><!--
# --><span rise="20480">---</span><!--
# --><span rise="10240">-</span><!--
# -->-<!--
# --><span rise="-10240">-</span><!--
# --><span rise="-20480">---</span><!--
# --><span rise="-10240">-</span><!--
# -->---</markup>