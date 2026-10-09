import argparse
import csv
import sys
from datetime import datetime

ARG_DATE_FORMAT = "%Y-%m-%d"    # how the user types dates, e.g. 2024-01-31
FILE_DATE_FORMAT = "%m/%d/%Y"   # how dates start in the CSV, e.g. 01/31/2024


def count_complaints(input_path, start, end):
    """Return a dict mapping (complaint type, borough) -> count."""
    counts = {}
    with open(input_path, newline="") as f:
        reader = csv.reader(f)
        header = next(reader)                      # first line = column names
        date_col = header.index("Created Date")    # find columns by name, not number
        type_col = header.index("Complaint Type")
        borough_col = header.index("Borough")

        for row in reader:                         # one row at a time = low memory
            if len(row) <= borough_col:            # skip broken/short rows
                continue
            try:
                # only the first 10 characters (the date) matter for a date range
                created = datetime.strptime(row[date_col][:10], FILE_DATE_FORMAT)
            except ValueError:
                continue                           # skip rows with an unreadable date
            if start <= created <= end:
                key = (row[type_col], row[borough_col])
                counts[key] = counts.get(key, 0) + 1
    return counts


def write_counts(counts, out):
    """Write the counts as CSV to an open file (or the screen)."""
    writer = csv.writer(out)
    writer.writerow(["complaint type", "borough", "count"])
    for (complaint_type, borough), n in sorted(counts.items()):
        writer.writerow([complaint_type, borough, n])


def main():
    parser = argparse.ArgumentParser(
        description="Count each complaint type per borough for a given creation date range."
    )
    parser.add_argument("-i", "--input", required=True,
                        help="path to the input 311 CSV file")
    parser.add_argument("-s", "--start", required=True,
                        help="start date (YYYY-MM-DD), inclusive")
    parser.add_argument("-e", "--end", required=True,
                        help="end date (YYYY-MM-DD), inclusive")
    parser.add_argument("-o", "--output",
                        help="output CSV file (prints to the screen if omitted)")
    args = parser.parse_args()

    try:
        start = datetime.strptime(args.start, ARG_DATE_FORMAT)
        end = datetime.strptime(args.end, ARG_DATE_FORMAT)
    except ValueError:
        parser.error("dates must be in YYYY-MM-DD format")
    if start > end:
        parser.error("start date must be on or before end date")

    counts = count_complaints(args.input, start, end)

    if args.output:
        with open(args.output, "w", newline="") as f:
            write_counts(counts, f)
    else:
        write_counts(counts, sys.stdout)


if __name__ == "__main__":
    main()