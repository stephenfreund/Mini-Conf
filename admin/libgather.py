#!/usr/bin/env python3

import json

import requests

# https://www.notion.so/EXTERNAL-Gather-http-API-3bbf6c59325f40aca7ef5ce14c677444#af100c0dc3a84ea6869cb779d58ff7b7


class Gather:
    def __init__(self, gather_api_key, gather_space_id):
        self.gather_api_key = gather_api_key
        self.gather_space_id = gather_space_id

    def createMap(self, name, sourceSpace=None, map=None):
        if sourceSpace == None:
            extra = {"map": map}
        else:
            extra = {"sourceSpace": sourceSpace}

        res = requests.post(
            "https://gather.town/api/createMap",
            json={
                "apiKey": self.gather_api_key,
                "spaceId": self.gather_space_id,
                "name": name,
            }
            | extra,
        )

        if res.status_code != 200:
            raise Exception(f"getMap failed {res.status_code}")

        return res.json()

    def getMap(self, mapId):
        res = requests.get(
            "https://gather.town/api/getMap",
            params={
                "apiKey": self.gather_api_key,
                "spaceId": self.gather_space_id,
                "mapId": mapId,
            },
        )
        if res.status_code != 200:
            raise Exception(f"getMap failed {res.status_code}")

        return res.json()

    def setMap(self, mapId, mapContent):
        res = requests.post(
            "https://gather.town/api/setMap",
            json={
                "apiKey": self.gather_api_key,
                "spaceId": self.gather_space_id,
                "mapId": mapId,
                "mapContent": mapContent,
            },
        )
        if res.status_code != 200:
            raise Exception(f"getMap failed {res.status_code}")

    def getGatherEmailDictionary(self):
        res = requests.get(
            "https://gather.town/api/getEmailGuestlist",
            headers={"Content-Type": "application/json"},
            params={
                "apiKey": self.gather_api_key,
                "spaceId": self.gather_space_id,
            },
        )
        if res.status_code != 200:
            raise Exception(f"getEmailGuestlist failed {res.status_code}")

        result = res.json()
        if isinstance(result, list):
            return { }
        else: 
            return result

    def setGatherEmailDictionary(self, users, mustCreate):
        res = requests.post(
            "https://gather.town/api/setEmailGuestlist",
            headers={"Content-Type": "application/json"},
            json={
                "overwrite": mustCreate,
                "apiKey": self.gather_api_key,
                "spaceId": self.gather_space_id,
                "guestlist": users,
            },
        )
        if res.status_code != 200:
            raise Exception(f"setEmailGuestlist failed {res.status_code}")

        return res.json()
        # print(json.dumps(res.json(), indent=4, sort_keys=True))

    # just use the javascript -- too tired to figure out the right
    # params to post...
    #
    # def uploadImage(self, fileName):
    #     with open(fileName, mode='rb') as file: # b is important -> binary
    #         fileContent = file.read()

    #     res = requests.post(
    #         "https://gather.town/api/uploadImage",
    #         headers={"Content-Type": "application/json"},
    #         json={
    #             "spaceId": self.gather_space_id,
    #             "bytes": fileContent
    #         },
    #     )
    #     if res.status_code != 200:
    #         raise Exception(f"uploadImage failed {res.status_code}")
    #     return res.data()


