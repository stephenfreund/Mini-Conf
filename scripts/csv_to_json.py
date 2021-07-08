# Python program to convert
# JSON file to CSV

import argparse
import csv
import json


def parse_arguments():
    parser = argparse.ArgumentParser(description="MiniConf Portal Command Line")
    parser.add_argument("input", default="data.csv", help="")

    parser.add_argument("out", default="data.json", help="")

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()

    # create a dictionary
    data = {}

    # Open a csv reader called DictReader
    with open(args.input, encoding="utf-8") as csvf:
        csvReader = csv.DictReader(csvf)

        # Convert each row into a dictionary
        # and add it to data
        data = [x for x in csvReader]

    # Open a json writer, and use the json.dumps()
    # function to dump data
    with open(args.out, "w", encoding="utf-8") as jsonf:
        jsonf.write(json.dumps(data, indent=4))
