#!/usr/bin/env python3
import mycsv
import re
import sys

max_toks = 5
max_channel_name_len = 70 # 80 is the upper-bound on Slack

stopwords = [line.rstrip('\n') for line in open('stopwords.txt').readlines()]

def make_channel_title(paper_title: str) -> str:
    # When the title is "Toolname: Long description of it", use Toolname
    colon_index = paper_title.find(':')
    if colon_index > 0:
        paper_title = paper_title[0:colon_index]
    as_lower = paper_title.lower()
    no_special = re.sub(r'[^a-z0-9 ]+', '', as_lower)
    tokens = no_special.split() # space is the default delimiter
    if len(no_special) < max_channel_name_len - 6:
        return "paper-" + "-".join(tokens)
    # Paper title is too long, so we are abbreviating
    toks_without_stopwords = [ tok for tok in tokens if not (tok in stopwords)]
    first_n_toks = toks_without_stopwords[:max_toks]
    print(paper_title)
    return "paper-" + "-".join(first_n_toks)

if __name__ == "__main__": 
    if len(sys.argv) != 3:
        print("Usage:")
        print("  python3 make_channel_csv.py ../sitedata/papers.csv ../sitedata/slack_channels.csv")
        sys.exit(1)
    papers_csv = mycsv.read_csv(sys.argv[1])
    channels_csv = sys.argv[2]
    slack_channels = [ ]
    for paper in papers_csv:
        slack_channels.append({ 
            'UID': paper['UID'], 
            'Channel Name': make_channel_title(paper['title']),
            'Purpose': f"Q&A for the PLDI paper {paper['title']}",
        })
    
    mycsv.write_csv(channels_csv, slack_channels)
