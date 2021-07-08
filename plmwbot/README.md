# The PLMW Bot

## Overview

Adds people to the plmw channel. Based on the pldibot.

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

   - users:read
   - users:read.email

5. Click *Install to Workspace*.

6. Save the *User OAuth Token*, which you will need later.

7. Create a world-readable Google Sheet with the columns *When*, *Channel*, and
   *Message* and get the URL to the CSV for the sheet.

8. Create a file in this directory called `plmwbot.yaml` with the following
   contents:

   ```
   oauth_token:  <User OAuth Token from the previous step>
   plmw_emails: plmw_emails.csv
   ```


## Running

Run `./plmwbot.py`.