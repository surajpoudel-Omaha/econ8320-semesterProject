# Sidebar filter
selected_series = st.sidebar.multiselect(
    "Select Variables",
    df['series_name'].unique(),
    default=["Unemployment Rate"]
)

filtered_df = df[df['series_name'].isin(selected_series)]

# Latest values
latest = df.sort_values("date").groupby("series_name").tail(1)

st.subheader("Latest Metrics")

col1, col2, col3 = st.columns(3)

try:
    col1.metric("US Unemployment", 
        round(latest[latest['series_name']=="Unemployment Rate"]['value'].values[0],2))
    col2.metric("Nebraska Unemployment", 
        round(latest[latest['series_name']=="Nebraska Unemployment"]['value'].values[0],2))
    col3.metric("Nonfarm Workers", 
        round(latest[latest['series_name']=="Nonfarm Workers"]['value'].values[0],2))
except:
    st.write("Metrics loading...")

# Line chart
st.subheader("Trend Over Time")

fig = px.line(
    filtered_df,
    x="date",
    y="value",
    color="series_name"
)

st.plotly_chart(fig)

# Omaha comparison
st.subheader("Omaha Earnings vs Hours")

omaha_df = df[df['series_name'].isin(["Omaha Earnings", "Omaha Hours"])]

fig2 = px.line(
    omaha_df,
    x="date",
    y="value",
    color="series_name"
)

st.plotly_chart(fig2)