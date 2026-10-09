# COMP 370 – Homework 5

## Data trimming (2024 only, one grep call)

```
tar -xzOf data/311_records.csv.tgz 311_Service_Requests_from_2010_to_Present_20250928.csv 2>/dev/null \
  | grep -E '^(Unique Key|[0-9]+,[0-9]{2}/[0-9]{2}/2024 )' > data/311_2024.csv
```

Keeps the header plus every row whose Created Date (column 2) is in 2024.

## Task 1

```
python borough_complaints.py -i data/311_2024.csv -s 2024-01-01 -e 2024-01-31 [-o out.csv]
```

## Task 3

See `complaint_analysis.ipynb` (notebook) and `complaint_type_analysis.md` (write-up).

## Task 4 – Bokeh dashboard

```
python dashboard/preprocess.py -i data/311_2024.csv -o data/monthly_response.csv
bokeh serve dashboard/dashboard.py --port 5006
```

`preprocess.py` computes monthly average response time (hours, created → closed) per
zipcode plus citywide, so the dashboard only loads a small file and updates instantly.

Data decisions (per FAQ): skip unclosed incidents, missing/invalid zipcodes, and negative
response times; assign each incident to the month it was closed; incidents closed in 2025
are excluded so the plot covers Jan–Dec 2024. Dropdowns list only NYC zipcodes (10xxx/11xxx).

Limitation: because months are by close date and the data starts Jan 1, early months can
only contain short-lived incidents, so averages naturally rise through the year.