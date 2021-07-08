# Python program to convert
# JSON file to CSV

import argparse
import csv
import json


def parse_arguments():
    parser = argparse.ArgumentParser(description="MiniConf Portal Command Line")
    parser.add_argument("input", default="data.json", help="paper file")

    parser.add_argument("out", default="data.csv", help="embeddings file to shrink")

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()

    # Opening JSON file and loading the data
    # into the variable data
    with open(args.input) as json_file:
        data = json.load(json_file)

    # now we will open a file for writing
    data_file = open(args.out, "w")

    # create the csv writer object
    csv_writer = csv.writer(data_file)

    # Counter variable used for writing
    # headers to the CSV file
    count = 0

    for emp in data:
        if count == 0:

            # Writing headers of CSV file
            header = emp.keys()
            csv_writer.writerow(header)
            count += 1

        # Writing data of CSV file
        csv_writer.writerow(emp.values())

    data_file.close()
