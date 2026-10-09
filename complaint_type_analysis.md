# Task 3 – Complaint Type Analysis

## Method
I ran `borough_complaints.py` from a Jupyter notebook on the 2024 data for two
periods: Jan 1–Feb 29, 2024 and Jun 1–Jul 31, 2024 (60 vs. 61 days, so the
periods are directly comparable). I summed counts across boroughs to find the
most abundant complaint type in Jan–Feb, then compared that type across periods.

## Most abundant complaint type (Jan–Feb 2024): HEAT/HOT WATER

## Findings
- HEAT/HOT WATER was the #1 complaint in Jan–Feb, narrowly ahead of Illegal
  Parking (79,916).
- In Jun–Jul it dropped by ~92% and fell to #25. The summer top complaints were
  Illegal Parking, Noise – Residential, and Noise – Street/Sidewalk.
- The drop is seasonal: heat complaints are driven by cold weather, when
  landlords are required to provide heat. The complaints that remain in summer
  are likely hot-water issues, which can happen year-round.
- The Bronx had the most heat complaints in both periods (~37% of the
  Jan–Feb total), suggesting heating problems are concentrated there rather than
  spread evenly across the city.