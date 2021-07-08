#!/usr/bin/env python3

import csv
import io
import json
import time
import zlib

import requests
import yaml
import argparse
 
class Auth0:
    def __init__(self, auth0_domain, auth0_connection, client_id, client_secret):
        self.auth0_domain = auth0_domain
        self.auth0_connection = auth0_connection
        self.client_id = client_id
        self.client_secret = client_secret

        res = requests.post(
            auth0_domain + "/oauth/token",
            headers = { 'content-type': "application/json" },
            json = {
                "client_id": client_id,
                "client_secret": client_secret,
                "audience": auth0_domain + "/api/v2/",
                "grant_type":"client_credentials"
            })

        if res.status_code != 200:
            raise Exception(f"get oauth/token failed {res.status_code}")

        asJson = res.json()

        self.auth0_authorization = "Bearer " + asJson["access_token"]

    def addUser(self, email, name):
        defaultPass = "pldi2021!"
        res = requests.post(
            self.auth0_domain + "/api/v2/users",
            headers = {
                "authorization": self.auth0_authorization,
                "Content-Type": "application/json"
            },
            json = {
                "connection": "Username-Password-Authentication", 
                "email": email,
                "name": name,
                "password": defaultPass,
            }
        )
        print(res.json())
        if res.status_code != 201:
            raise Exception(f"users failed {res.status_code}")
        print(f"Created account for {email} with initial password '{defaultPass}'")

    def getUser(self, email):
        res = requests.get(
            self.auth0_domain + "/api/v2/users-by-email",
            headers = {
                "authorization": self.auth0_authorization,
                "Content-Type": "application/json"
            },
            params = {
                "email": email.lower(),
            }
        )
        if res.status_code != 200:
            raise Exception(f"users-by-email failed {res.status_code}")

        return res.json()

    def getLog(self, filter):
        res = requests.get(
            self.auth0_domain + "/api/v2/logs",
            headers = {
                "authorization": self.auth0_authorization,
                "Content-Type": "application/json"
            },
            params = {
                "q": filter,
            }
        )
        if res.status_code != 200:
            raise Exception(f"log failed {res.status_code}")

        return res.json()


    def userList(self):
        res = requests.post(
            self.auth0_domain + "/api/v2/jobs/users-exports",
            headers={"authorization": self.auth0_authorization},
            data={"connection_id": self.auth0_connection},
        )
        if res.status_code != 200:
            raise Exception(f"users-exports failed {res.status_code}")

        jobId = res.json()["id"]

        while True:
            res = requests.get(
                self.auth0_domain + "/api/v2/jobs/" + jobId,
                headers={"authorization": self.auth0_authorization},
            )
            if res.status_code != 200:
                raise Exception(f"jobs failed {res.status_code}")

            asJson = res.json()
            if asJson["status"] != "pending":
                break
            timeLeft = asJson.get("time_left_seconds", 2)
            time.sleep(timeLeft)

        location = res.json()["location"]

        res = requests.get(location, headers={"accept-encoding": "gzip"})
        text = zlib.decompress(res.content, 16 + zlib.MAX_WBITS).decode("utf-8")

        with io.StringIO(text) as csvf:
            csvReader = csv.DictReader(csvf)
            return sorted([x for x in csvReader], key=lambda x : x["email"])

