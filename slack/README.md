# The PLDI Bot

## Overview

The *pldibot* is a Slack bot that makes announcements during the conference.
To use the bot, create a Google Sheet with three columns and these headers:

1. *When* the announcement should be made (date and time),
2. The *Channel* where the announcement should be made, and
3. The *Message* of the announcement.

The pldibot is designed to run as a Cron job every minute. On every run, it
polls for a new set of announcements and posts those announcements to Slack.

## Prerequisites

You will need the Slack SDK for Python:

```
pip3 install slack_sdk
```

## Install the app

1. Visit https://api.slack.com/

2. Choose a name for the app, e.g., "pldibot", and associate it with the
   right workspace.

3. Select *OAuth & Permissions* on the right-hand side.

4. Scroll down to *User Token Scopes* in the *Scopes* section. The bot requires
   these scopes:

   - channels:read
   - channels:write
   - chat:write
   - groups:read
   - groups:write

5. Click *Install to Workspace*.

6. Save the *User OAuth Token*, which you will need later.

7. Create a world-readable Google Sheet with the columns *When*, *Channel*, and
   *Message* and get the URL to the CSV for the sheet.

8. Create a file in this directory called `pldibot.yaml` with the following
   contents:

   ```
   botadmin: botadmin
   oauth_token: <User OAuth Token from the previous step>
   posts:
   csv: <Google Sheet CSV URL>
   poll_timeout: 10

## Running

Run `./pldibot.py`. You will need to run it every minute, e.g., using Cron.
Note that pldibot will overwrite `pldibot.yaml` on each run. It uses the file
to track the announcements it has already sent, to avoid creating duplicates.