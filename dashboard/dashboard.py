import os
import pandas as pd
from bokeh.core.properties import value
from bokeh.io import curdoc
from bokeh.layouts import column
from bokeh.models import ColumnDataSource, Select
from bokeh.plotting import figure

HERE = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(HERE, "..", "data", "monthly_response.csv")
MONTHS = list(range(1, 13))
MONTH_NAMES = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
               "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

# Load the small precomputed file ONCE at startup (this is what keeps updates fast)
df = pd.read_csv(DATA_PATH, dtype={"zipcode": str})
table = df.pivot(index="month", columns="zipcode", values="avg_hours").reindex(MONTHS)

# Real NYC zipcodes start with 10 or 11 -> drop junk like 00000
zipcodes = sorted(z for z in table.columns if z.startswith(("10", "11")))


def series(zipcode):
    """The 12 monthly averages for one zipcode (or 'ALL'), in Bokeh's format."""
    return dict(month=MONTHS, hours=table[zipcode].tolist())


start1, start2 = zipcodes[0], zipcodes[1]
all_source = ColumnDataSource(series("ALL"))
source1 = ColumnDataSource(series(start1))
source2 = ColumnDataSource(series(start2))

select1 = Select(title="Zipcode 1", value=start1, options=zipcodes)
select2 = Select(title="Zipcode 2", value=start2, options=zipcodes)

p = figure(title="Monthly average 311 response time, 2024 (created to closed)",
           x_axis_label="Month (2024, by month closed)",
           y_axis_label="Average response time (hours)",
           width=900, height=450)
p.line("month", "hours", source=all_source, legend_label="All NYC",
       line_width=2, color="gray", line_dash="dashed")
p.line("month", "hours", source=source1, legend_label=f"Zipcode 1: {start1}",
       line_width=2, color="#1f77b4")
p.line("month", "hours", source=source2, legend_label=f"Zipcode 2: {start2}",
       line_width=2, color="#d62728")
p.xaxis.ticker = MONTHS
p.xaxis.major_label_overrides = dict(zip(MONTHS, MONTH_NAMES))
p.legend.location = "top_left"


def update(attr, old, new):
    """Runs whenever either dropdown changes: swap in the new zipcode's data."""
    source1.data = series(select1.value)
    source2.data = series(select2.value)
    p.legend.items[1].label = value(f"Zipcode 1: {select1.value}")
    p.legend.items[2].label = value(f"Zipcode 2: {select2.value}")


select1.on_change("value", update)
select2.on_change("value", update)

curdoc().add_root(column(select1, select2, p))