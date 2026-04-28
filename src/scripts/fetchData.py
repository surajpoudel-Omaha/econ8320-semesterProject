import requests
import json
import pandas as pd
from datetime import date

API_KEY = "94b1aa81d7e54ee2bcc0a66f6a817923"

current_year = date.today().year
startYear = current_year - 10 

series_ids = [
    "LNU04000000",  # Unemployment Rate
    "LNS14000006",  # Black
    "LNS14000009",  # Hispanic
    "LNS14032183", # Asian
    "LNS14000003",  # White
    "LNS14000001",  # Men
    "LASST310000000000003", # Nebraska
    "CES0000000001", # Nonfarm
    "SMU31365400500000011", # Earnings Omaha
    "SMU31365400500000002", # Hours Omaha
    "CXUTOTALEXPLB0101M", # Expenditures
    "LNS14000002" #women
]

headers = {'Content-type': 'application/json'}

data = json.dumps({
    "seriesid": series_ids,
    "startyear": startYear,
    "endyear": current_year,
    "registrationkey":API_KEY
})

response = requests.post(
    'https://api.bls.gov/publicAPI/v2/timeseries/data/',
    data=data,
    headers=headers
)

series_map = {
    "LNU04000000": "Us Unemployment",
    "LNS14000006": "Afam Unemployment",
    "LNS14000009": "Hispanic Unemployment",
    "LNS14032183": "Asian Unemployment",
    "LNS14000003": "White Unemployment",
    "LNS14000001": "Men Unemployment",
    "LASST310000000000003": "Nebraska Unemployment",
    "CES0000000001": "Nonfarm Workers",
    "LNS14000002" : "Women Unemployment",
    "SMU31365400500000011": "Omaha Weekly Earnings",
    "SMU31365400500000002": "Omaha Weekly Hours",
    "CXUTOTALEXPLB0101M": "Expenditures"
    
}

json_data = response.json()

unemploymentData = []

for series in json_data['Results']['series']:
    series_id = series['seriesID']
    series_name = series_map.get(series_id, series_id)
    rows = []

    for item in series['data']:
        if item['period'] != 'M13':
            rows.append({
                "year": item['year'],
                "period": item['period'],
                "value": item['value']
            })

    df = pd.DataFrame(rows)
    
    if "Unemployment" in series_name:
        df = df.rename(columns={"value": series_name})
        unemploymentData.append(df)
    else:
        df['month'] = df['period'].str.extract(r'(\d+)').astype(int)
        filename = f"src/data/{series_name}.csv"
        df.to_csv(filename, index=False)
        print(f"Saved separate file: {filename}")

if unemploymentData:
    unemployment_df = unemploymentData[0]

    for df in unemploymentData[1:]:
        unemployment_df = pd.merge(
            unemployment_df,
            df,
            on=["year", "period"],
            how="outer"
        )
    unemployment_df = unemployment_df.sort_values(["year", "period"])
    unemployment_df.to_csv("src/data/Unemployment Data.csv", index=False)

print("Data collected successfully!")