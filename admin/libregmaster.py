#!/usr/bin/env python3

import json
import requests

class RegMaster:
    def __init__(self, password, endpoint):
        self.password = password
        self.endpoint = endpoint

    def validate(self, emailAddress):
        res = requests.post(
            self.endpoint,
            params={
                "action": "validate",
                "email" : emailAddress,
                "password": self.password
            }
        )

        if res.status_code != 200:
            raise Exception(f"validate failed {res.status_code}")

        if res.text.startswith('{"error":'):
            return res.text
        else:
            return None
        # print(res.text)
        # 
        # return res.json()

    def listFromResult(self, row):
        cols = row.split(",")
        email = cols[-2]
        name = " ".join(cols[:-2])
        return { "email" : email, "name" : name }

    def bodyToJSON(self, body):
        return map(lambda x: self.listFromResult(x), [row for row in body.split("\n") if row != ""])
        # return sorted(map(lambda x: self.listFromResult(x), [row for row in body.split("\n") if row != ""]), key=lambda x: x["email"])

    def allRegistered(self):
        res = requests.post(
            self.endpoint,
            params={
                "action": "listpaid",
                "password": self.password
            }
        )

        if res.status_code != 200:
            raise Exception(f"validate failed {res.status_code}")

        return self.bodyToJSON(res.text)

    def allRegisteredWithUnpaid(self):
        res = requests.post(
            self.endpoint,
            params={
                "action": "listall",
                "password": self.password
            }
        )

        if res.status_code != 200:
            raise Exception(f"validate failed {res.status_code}")

        return self.bodyToJSON(res.text)
