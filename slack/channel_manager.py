# TODO(arjun): Still working on this. It is overengineered.
import os
import mycsv
from pathlib import Path
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

class ChannelManager(object):

    def __init__(self, token=Path('SLACK_OAUTH_TOKEN').read_text()):
        self.token = token
        self.client = WebClient(token=self.token)
        self.channels = [ ]

    # Sets the internal channels field
    def list(self):
        resp = self.client.conversations_list(exclude_archived=True, types="public_channel,private_channel", limit=500)
        assert resp.data['ok']
        self.channels = []
        for channel in resp.data['channels']:
            self.channels.append({
                'ID': channel['id'],
                'Channel Name': channel['name'],
                'Purpose': channel['purpose']['value']
            })
    
    def exists(self, name):
        for channel in self.channels:
            if channel['Channel Name'] == name:
                return True
        return False

    def get_id(self, name):
        for channel in self.channels:
            if channel['Channel Name'] == name:
                return channel['ID']
        return False
    
    def get_purpose(self, name):
        for channel in self.channels:
            if channel['Channel Name'] == name:
                return channel['Purpose']
        return False


    def create(self, name, is_private):
        print(f'Creating channel {name} ...')
        resp = self.client.conversations_create(name=name, is_private=is_private)
        return resp
    
    def set_purpose(self, name, purpose):
        chan_id = self.get_id(name)
        # TODO(arjun): Hack. The name that comes back has HTML entities for
        # special characters. God help us all.
        if self.get_purpose(name) != "":
            return
        print(f'Setting purpose for {name} ...')
        self.client.conversations_setPurpose(channel=chan_id, purpose=purpose)

    def post(self, name, message):
        channel_id = self.get_id(name)
        if not channel_id:
            return False

        try:
            resp = self.client.chat_postMessage(channel=channel_id, text=message)
            if resp.data['ok']:
                return True
            else:
                print(f"Response was {resp.data}")
                return False    
        except SlackApiError as e:
            if e.response["error"] != "not_in_channel":
                raise e
            self.client.conversations_join(channel=channel_id)
            self.client.chat_postMessage(channel=channel_id, text=message)
            return True

def create_channels(channels_csv):
    channels = mycsv.read_csv(channels_csv)
    channel_manager = ChannelManager()
    channel_manager.list()
    for chan in channels:
        name = chan["Channel Name"]
        if not channel_manager.exists(name):
            channel_manager.create(name, is_private=False)
        if chan["Purpose"] != "":
            channel_manager.set_purpose(name, chan["Purpose"])
        
