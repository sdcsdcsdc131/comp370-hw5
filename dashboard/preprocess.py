import argparse
import csv
from datetime import datetime

DATE_FORMAT = "%m/%d/%Y %I:%M:%S %p"   # e.g. 01/31/2024 02:30:00 PM


def main():
    parser = argparse.ArgumentParser(
        description="Precompute monthly average 311 response time (hours) per zipcode, plus citywide (ALL)."
    )
    parser.add_argument("-i", "--input", required=True, help="trimmed 2024 311 CSV")
    parser.add_argument("-o", "--output", required=True, help="output CSV of monthly averages")
    args = parser.parse_args()

    sums = {}    # (zipcode, month) -> total hours
    counts = {}  # (zipcode, month) -> number of incidents

    with open(args.input, newline="") as f:
        reader = csv.reader(f)
        header = next(reader)
        created_col = header.index("Created Date")
        closed_col = header.index("Closed Date")
        zip_col = header.index("Incident Zip")

        for row in reader:
            if len(row) <= zip_col:
                continue
            closed_text = row[closed_col]
            zipcode = row[zip_col].strip()[:5]
            # skip: not closed yet, or no valid 5-digit zipcode
            if not closed_text or len(zipcode) != 5 or not zipcode.isdigit():
                continue
            try:
                created = datetime.strptime(row[created_col], DATE_FORMAT)
                closed = datetime.strptime(closed_text, DATE_FORMAT)
            except ValueError:
                continue

            hours = (closed - created).total_seconds() / 3600
            if hours < 0:              # closed before opened -> bad data (FAQ 1)
                continue
            if closed.year != 2024:    # keep the plot to Jan-Dec 2024
                continue

            # add this incident to its zipcode AND to the citywide "ALL" total
            for key in ((zipcode, closed.month), ("ALL", closed.month)):
                sums[key] = sums.get(key, 0.0) + hours
                counts[key] = counts.get(key, 0) + 1

    with open(args.output, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["zipcode", "month", "avg_hours", "n"])
        for key in sorted(sums):
            zipcode, month = key
            writer.writerow([zipcode, month, round(sums[key] / counts[key], 3), counts[key]])


if __name__ == "__main__":
    main()