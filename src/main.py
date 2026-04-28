import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date

st.title("US Labor Statistics Dashboard")
nonFarmersWorkers = pd.read_csv("./data/Nonfarm Workers.csv")
unEmployment = pd.read_csv("../src/data/Unemployment Data.csv")
unEmployment = unEmployment.replace("-", pd.NA)
unEmployment['month'] = unEmployment['period'].str.replace('[A-Za-z]', '', regex=True).astype(int)

unemploymentXNonFarmers = pd.merge(
            unEmployment [['year', 'period', 'Us Unemployment']],
            nonFarmersWorkers,
            on=["year", "period"],
            how="outer"
)


current_year = date.today().year
current_month = date.today().month
current_day = date.today().day


labelMap = {
    "Us Unemployment": "United States",
    "Afam Unemployment": "African American",
    "Hispanic Unemployment": "Hispanic",
    "Asian Unemployment": "Asian",
    "White Unemployment": "White",
    "Men Unemployment": "Men",
    "Women Unemployment": "Women",
    "Nebraska Unemployment": "Nebraska"
}

reverse_map = {v: k for k, v in labelMap.items()}

for col in labelMap.keys():
    unEmployment[col] = pd.to_numeric(unEmployment[col])

unEmployment["date"] = pd.to_datetime(
    unEmployment["year"].astype(str) + unEmployment["month"].astype(str).str.zfill(2),
    format="%Y%m"
)

currentTitle = f"Unemployment as of: {current_year}-{current_month}-{current_day}"

unEmployment = unEmployment.sort_values("date")

filtered = unEmployment[
    (unEmployment["year"] == current_year) &
    (unEmployment["month"] == current_month)
].dropna()

if not filtered.empty:
    latest = filtered.iloc[0]
else:
    latest = unEmployment.sort_values(["year", "month"]).dropna().iloc[-1]

### Unemployment DashBoard
nonFarmWorkers = nonFarmersWorkers.sort_values(["year", "month"]).dropna().iloc[-1]

container = st.container()


container.subheader(currentTitle)
col1, col2, col3, col4, col5 = container.columns(5)
col1.metric("US", f"{latest['Us Unemployment']}%")
col2.metric("US Women", f"{latest['Women Unemployment']}%")
col3.metric("US Men", f"{latest['Men Unemployment']}%")
col4.metric("Nebraska", f"{latest['Nebraska Unemployment']}%")
col5.metric("Non Farmers Workers", f"{nonFarmWorkers['value']}")


container2 = st.container()
container2.subheader("Unemployment Trends Over Time")
col1, col2= container2.columns([5, 1], vertical_alignment="bottom")
with col2:
    st.write("Filters")
    selected_labels = []
    for label in labelMap.values():
        if st.checkbox(label, value=(label in ["Men", "Women"])):
            selected_labels.append(label)
    selected_columns = [reverse_map[label] for label in selected_labels]

with col1:
    fig = px.line(
        unEmployment,
        x="date",
        y=selected_columns,
        labels={
            "value": "Unemployment Rate (%)",
            "variable": "Demographic Group"
        }
    )

    # Rename legend entries
    fig.for_each_trace(
        lambda t: t.update(name=labelMap.get(t.name, t.name))
    )

    fig.update_layout(
        legend_title_text="Demographic Group"
    )
    st.plotly_chart(fig)

st.subheader("United States VS Nebraska Unemployment")
fig2 = px.line(
    unEmployment,
    x="date",
    y=["Us Unemployment", "Nebraska Unemployment"],
    labels={
        "value": "Unemployment Rate (%)",
        "variable": "Location"
    }
)

fig2.for_each_trace(
    lambda t: t.update(name=labelMap.get(t.name, t.name))
)

fig2.update_layout(
    legend_title_text="Location"
)

st.plotly_chart(fig2)

### Unemployment over Non-Farmer Workers DashBoard

