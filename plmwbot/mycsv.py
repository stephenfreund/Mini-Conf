import csv

# Read CSV file, turn into a list of dictionaries. Assumes a header a present.
def read_csv(filename: str) -> list:
    with open(filename, newline='') as f:
        reader = csv.DictReader(f)
        rows = [ ]
        for row in reader:
            rows.append(row)
        return rows

# Writes a list of dictionaries to a header. Uses the keys of the first
# dictionary as the header row. Assumes that all dictionaries have the
# same keys.
def write_csv(filename: str, rows: dict):
    with open(filename, 'w', newline='') as f:
        fieldnames = list(rows[0].keys())
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for row in rows:
            w.writerow(row)

