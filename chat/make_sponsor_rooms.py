import argparse
import csv
import json

import yaml
from requests import sessions
from rocketchat_API.rocketchat import RocketChat


def parse_arguments():
    parser = argparse.ArgumentParser(description="MiniConf Portal Command Line")
    parser.add_argument("--config", default="config.yml", help="Configuration yaml")
    parser.add_argument(
        "--sponsors", default="../sitedata/sponsors.yml", help="Papers YML"
    )
    parser.add_argument("--test", action="store_true")
    return parser.parse_args()


def read_data(fname):
    _name, typ = fname.split("/")[-1].split(".")
    if typ == "json":
        res = json.load(open(fname))
    elif typ in {"csv", "tsv"}:
        res = list(csv.DictReader(open(fname)))
    elif typ == "yml":
        res = yaml.load(open(fname).read(), Loader=yaml.SafeLoader)
    else:
        raise ValueError("file not supported: " + fname)
    return res


if __name__ == "__main__":
    args = parse_arguments()

    config = yaml.load(open(args.config))
    sponsors = read_data(args.sponsors)

    with sessions.Session() as session:
        rocket = RocketChat(
            config["username"],
            config["password"],
            server_url=config["server"],
            session=session,
        )

        for sponsor in sponsors:
            if sponsor.get("channel") != None:
                channel_name = sponsor["channel"]
                if not args.test:
                    created = rocket.channels_create(channel_name).json()
                    print(channel_name, created)
                    channel_id = rocket.channels_info(channel=channel_name).json()[
                        "channel"
                    ]["_id"]

                # Change to topic of papers.
                topic = sponsor["name"]
                if not args.test:
                    rocket.channels_set_topic(channel_id, topic).json()

                print("Creating " + channel_name + " topic " + topic)
