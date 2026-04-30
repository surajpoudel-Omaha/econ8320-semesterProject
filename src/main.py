import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date
import os

baseDir = os.path.dirname(os.path.abspath(__file__))

current_year = date.today().year
current_month = date.today().month
current_day = date.today().day

nonFarmWorkersDir = os.path.join(baseDir,"data", "Nonfarm Workers.csv")
expendituresDir = os.path.join(baseDir,"data", "Expenditures.csv")
unemploymentDir = os.path.join(baseDir,"data", "Unemployment Data.csv")
weeklEarningDir = os.path.join(baseDir,"data", "Omaha Weekly Earnings.csv")
weeklHoursDir = os.path.join(baseDir,"data", "Omaha Weekly Hours.csv")

nonFarmersWorkers = pd.read_csv(nonFarmWorkersDir)
unEmployment = pd.read_csv(unemploymentDir)
expenditures = pd.read_csv(expendituresDir)
weeklyEarnings = pd.read_csv(weeklEarningDir)
weeklyHours = pd.read_csv(weeklHoursDir)

unEmployment = unEmployment.replace("-", pd.NA)
unEmployment['month'] = unEmployment['period'].str.replace('[A-Za-z]', '', regex=True).astype(int)

with st.sidebar:
    view = st.selectbox(
        "Select a Dashboard",
        ["Unemployment DashBoard", "Workers Dashboard", "Datasets"]
    )

if view == "Unemployment DashBoard":
    st.title("US Labor Statistics Dashboard")

   


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
                "variable": "Demographic Group",
                "date" : "Date"
            }
        )

        # Used OpenAI. (2026). ChatGPT (GPT-5.3-mini) [Large language model]. https://chat.openai.com
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
            "variable": "Location",
            "date" : "Date"
        }
    )
    # Used OpenAI. (2026). ChatGPT (GPT-5.3-mini) [Large language model]. https://chat.openai.com
    fig2.for_each_trace(
        lambda t: t.update(name=labelMap.get(t.name, t.name))
    )

    fig2.update_layout(
        legend_title_text="Location"
    )

    st.plotly_chart(fig2)
if view == "Workers Dashboard":
# Workers DashBoard
    currentTitle = f"Workers Information as of: {current_year}-{current_month}-{current_day}"
    nonFarmWorkers = nonFarmersWorkers.sort_values(["year", "month"]).dropna().iloc[-1]
    expendituresCurrent = expenditures.sort_values(["year", "month"]).dropna().iloc[-1]
    weeklyEarningsCurrent = weeklyEarnings.sort_values(["year", "month"]).dropna().iloc[-1]
    weeklyHoursCurrent = weeklyHours.sort_values(["year", "month"]).dropna().iloc[-1]
    
    st.title("Workers Dashboard")
    container3 = st.container()
    container3.subheader(currentTitle)
    col1, col2, col3, col4= container3.columns(4)
    col1.metric("US Non Farmers Workers", f"{nonFarmWorkers['value']}")
    col2.metric("US Avg Expenses", f"{expendituresCurrent['value']}")
    col3.metric("Omaha Avg Weekly Income", f"{weeklyEarningsCurrent['value']}")
    col4.metric("Omaha Avg Weekly Hours", f"{weeklyHoursCurrent['value']}")

    nonFarmersWorkers["date"] = pd.to_datetime(
        nonFarmersWorkers["year"].astype(str) + nonFarmersWorkers["month"].astype(str).str.zfill(2),
        format="%Y%m"
    )
    st.subheader("Non Farmers Workers In US Over Year")
    fig3 = px.line(
        nonFarmersWorkers,
        x="date",
        y= "value",
        labels={
            "value": "Non Farmers Workers",
            "date" : "Date"
        }
    )
    st.plotly_chart(fig3)
    
    weeklyEarnings["value"] = pd.to_numeric(weeklyEarnings["value"])
    weeklyEarnings.rename(columns={"value": "earnings"}, inplace=True)
    
    
    expenditures["value"] = pd.to_numeric(expenditures["value"])
    expenditures.rename(columns={"value": "expenditures"}, inplace=True)
    
    
    yearlyEarnings = (
        weeklyEarnings
        .groupby("year")["earnings"]
        .mean()
        .reset_index()
        )
        
    
    
    comparisionData = pd.merge(
    yearlyEarnings,
    expenditures,
    on="year",
    how="inner")
    
    comparisionData['earnings'] = comparisionData['earnings'] * 52
    st.subheader("US Average Expense VS Omaha Average Yearly Income")
    fig4 = px.bar(
        comparisionData, 
        x="year",
        y= ["earnings", "expenditures"],
        barmode="group",
        labels={
            "value": "Amount",
            "variable": "",
            "earnings" : "Income",
        })
    st.plotly_chart(fig4)
    
    
    
    weeklyHours.rename(columns={"value": "hours"}, inplace=True)
    weeklyHours["hours"] = pd.to_numeric(weeklyHours["hours"])
    
    heatData = weeklyHours.pivot_table(
    index="year",
    columns="month",
    values="hours",)
    
    st.subheader("Average Weekly Hours Worked In Omaha")
    fig5 = px.imshow(heatData,labels=dict(y="Year", x="Month"), color_continuous_scale="hot")
    
    st.plotly_chart(fig5)
    
    weeklyHours = weeklyHours.drop(columns=["month"])
    weeklyHouXWeeklyEar = pd.merge(
        weeklyHours,
        weeklyEarnings,
        on=["year","period"],
        how="inner"    
    )
       
    
    
if view == "Datasets":
    st.title("Datasets")
    st.markdown('Data Source: <a href="https://www.bls.gov/developers/home.htm"> U.S. Bureau of Labor Statistics  <a>',
    unsafe_allow_html=True)
    unemploymentContainer = st.container()
    unemploymentContainer.subheader("Unemployment Dataset")
    unemploymentContainer.write(unEmployment)
    unemploymentContainer.subheader("Non FarmWorkers Dataset")
    unemploymentContainer.write(nonFarmersWorkers)
    unemploymentContainer.subheader("Expenditures Dataset")
    unemploymentContainer.write(expenditures)
    unemploymentContainer.subheader("Omaha Weekly Earnings Datasets")
    unemploymentContainer.write(weeklyEarnings)
    unemploymentContainer.subheader("Omaha Weekly Hours Datasets")
    unemploymentContainer.write(weeklyHours)
        
