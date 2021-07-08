#!/usr/bin/env python3

# High-level Plan:
# 1. Get the current list of Slack users (using Slack API)
# 2. Read the file of expected users
# 3. Figure out who needs to be added to the PLMW channel. A little irritating
#    to deal with the ID / email mapping.
import sys
import yaml
import mycsv
from slack_sdk import WebClient

def read_config():
    with open("plmwbot.yaml") as config_yaml:
        return yaml.safe_load(config_yaml)

def get_all_slack_users(slack):
    users_list =  slack.users_list()
    if users_list['response_metadata']['next_cursor'] != '':
        print("Need to implement pagination now!")
        exit(1)
    members = users_list['members']
    return { user['profile']['email']: user['id'] for user in members if 'email' in user['profile'] }

def read_plmw_emails(filename):
    users_csv = mycsv.read_csv(filename)
    return [ user['email'] for user in users_csv ]

def get_plmw_channel_id(slack):
    all_chans = slack.conversations_list(exclude_archived=True, types="public_channel,private_channel", limit=500)
    for chan in all_chans.data['channels']:
        if chan['name'] == "plmw":
            return chan['id']
    print("No #plmw channel (or the bot user is not a member)")
    sys.exit(1)

def get_plmw_channel_members(slack, plmw_channel_id):
    members = slack.conversations_members(channel=plmw_channel_id, limit=500)
    return set(members['members'])

def main():
    cfg = read_config()
    slack = WebClient(token=cfg['oauth_token'])
    plmw_channel_id = get_plmw_channel_id(slack)
    # set(id): Slack IDs for all members of #plmw
    plmw_channel_members = get_plmw_channel_members(slack, plmw_channel_id)
    # dict(email, id): All users on Slack
    all_slack_users = get_all_slack_users(slack)
    # set(email): People who should be on #plmw
    plmw_emails = set(read_plmw_emails(cfg['plmw_emails']))
    # set(id): Slack IDs of people who should be on #plmw
    may_add_to_plmw = { all_slack_users[email] for email in plmw_emails if email in all_slack_users }
    # set(id): Slack IDs of people who are not on #plmw, but should be
    will_add_to_plmw = may_add_to_plmw - plmw_channel_members
    
    # Sanity check
    if len(will_add_to_plmw) > 0:
        print("Email addresses of people we are going to add:")
        all_slack_users_inv = {v: k for k, v in all_slack_users.items()}
        for id in will_add_to_plmw:
            print(all_slack_users_inv[id])
    else:
        print("Nobody to add")
        return
    
    if len(sys.argv) == 2 and sys.argv[1] == "side-effect":
        slack.conversations_invite(channel=plmw_channel_id,users=','.join(will_add_to_plmw))
    else:
        print("Use ./plmwbot.py side-effect to actually add these people")
        return

if __name__ == "__main__":
    main()
