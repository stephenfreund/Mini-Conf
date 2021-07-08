#!/usr/bin/env python3
import sys
import yaml
import urllib.request
import csv
import datetime
import channel_manager
from retry import retry

DATE_FORMAT = '%Y-%m-%d %H:%M'

# Returns a datetime or None. i.e., suppresses parsing exceptions.
def parse_date(when):
    try:
        return datetime.datetime.strptime(when, DATE_FORMAT)
    except:
        return None

# Current time with minute-level precision.
def this_minute():
    now_txt = datetime.datetime.now().strftime(DATE_FORMAT)
    return datetime.datetime.strptime(now_txt, DATE_FORMAT)

def get_posts_csv(url, timeout):
    with urllib.request.urlopen(url, None, timeout) as resp:
        charset = resp.headers.get_content_charset() or 'utf-8'
        csv_lines = resp.read().decode(charset).splitlines()
        csv_reader = csv.DictReader(csv_lines)
        rows = [ ]
        for row in csv_reader:
            rows.append(row)
        return rows

def read_config():
    with open("pldibot.yaml") as config_yaml:
        return yaml.safe_load(config_yaml)

def update_config(cfg, now):
    cfg['last_run'] = now.strftime(DATE_FORMAT)
    with open("pldibot.yaml", "w") as config_yaml:
        yaml.dump(cfg, config_yaml)

def main():
    if sys.version_info < (3,9):
        print("Must use Python 3.9+")
        sys.exit(1)

    cfg = read_config()
    now = this_minute()

    # Read the channel list from Slack
    chans = channel_manager.ChannelManager(token=cfg['oauth_token'])
    retry(5, "listing conversations", lambda: chans.list())

    # Read all posts from Google Sheets
    all_posts = retry(5, "reading Google Sheet", lambda: get_posts_csv(cfg['posts']['csv'], cfg['posts']['poll_timeout']))
    
    sent_posts = cfg['sent']
    pending_posts = [ ]

    for post in all_posts:
        if post in sent_posts:
            continue
        when = parse_date(post['When'])
        if when is None:
            pending_posts.append({
                'Message': f"Could not process the timestamp for {post['Message']}",
                'Channel': cfg["botadmin"]
            })
            continue
        if when != now:
            continue
        pending_posts.append(post)
    
    sent_posts.extend(pending_posts)
    # Write the config back with the current time, to avoid spamming.
    update_config(cfg, now)

    for post in pending_posts:
        try:
            chan = post["Channel"]
            message = post["Message"]
            retry(3, f"Posting message to {chan}: {message}", lambda: chans.post(chan, message))
        except:
            print(f"Failed to post to {chan}: {message}")
        

if __name__ == "__main__":
    main()
