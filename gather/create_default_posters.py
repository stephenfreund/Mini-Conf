import csv
import io
import json
import time
import zlib
import sys
import os
import shutil

import requests
import yaml

COMMAND = """
    convert \( %s \) \
    \( -fill black -font ArialNarrowB -pointsize 48 -size 940x -gravity North caption:"%s" \
       -fill dimgray -font ArialNarrowB -pointsize 36 -size 940x  caption:"%s" -append \) \
    -gravity north -compose over -composite %s
"""


def build(png, paper, output):
    title = paper["title"]
    authors = ", ".join(paper["authors"].split("|"))
    command = COMMAND % (png, title, authors, output) 
    os.system(command) 

if __name__ == "__main__":
    posterPNG = sys.argv[1]
    config = yaml.load(open("../admin/config.yml").read(), Loader=yaml.SafeLoader) | yaml.load(open("config.yml").read(), Loader=yaml.SafeLoader)
    papers = list(csv.DictReader(open(config["sitedata"] + "/papers.csv")))
    done = []
    notDone = []
    for paper in papers:
        id = paper["UID"].split(".")[1]
        posterFromCPC = f"../author-content/pictures/pldi21main-p{id}-p-PosterPicture.png"
        output = f"build/poster_{paper['UID']}.png"
        if os.path.exists(posterFromCPC):
            print(paper["UID"] + " * ")
            shutil.copyfile(posterFromCPC, output)
            done.append(id)
        else:
            print(paper["UID"])
            build(posterPNG, paper, output)
            notDone.append(id)
    
    print(f"Not Done: {notDone}")
    print(f"Done:     {done}")    



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