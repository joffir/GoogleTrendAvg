import requests
import json
import matplotlib.pyplot as plt
from datetime import datetime
import pandas as pd

def generate_noaa():
    # URL of the NOAA JSON data
    url = "https://www.ncei.noaa.gov/access/monitoring/us-weekly/wkly.json"

    # Send a GET request to retrieve the JSON data
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON data
        data = json.loads(response.text)
        temperature_data = data["data"]
        dates = []
        region_temperatures = {}

        # Regions to include in the chart
        regions_to_include = [
            "nat",
            "ne",
            "enc",
            "c",
            "se",
            "wnc",
            "s",
            "sw",
            "nw",
            "w"
        ]

        # Iterate over the temperature data
        for date, temperatures in temperature_data.items():
            # Extract the date
            date = datetime.strptime(date, "%Y%m%d")
            dates.append(date)

            # Iterate over each region's temperature
            for region, temp in temperatures.items():
                if region in regions_to_include:
                    if region not in region_temperatures:
                        region_temperatures[region] = []
                    region_temperatures[region].append(float(temp))

        zipped = list(zip(dates, region_temperatures["ne"], region_temperatures["enc"], region_temperatures["c"], region_temperatures["se"],
                        region_temperatures["wnc"], region_temperatures["s"], region_temperatures["sw"], region_temperatures["nw"],
                        region_temperatures["w"], region_temperatures["nat"]))
        df = pd.DataFrame(zipped, columns=["date","ne","enc","c","se","wnc","s","sw","nw","w","nat"])
        df['WeekNumber'] = df['date'].apply(lambda x: datetime.strftime(x, "%U"))

        current_year = datetime.now().year
        filtered_df = df[(df['date'].dt.year < current_year) & (df['date'].dt.year > (current_year - 10))]
        average_df = filtered_df.groupby('WeekNumber').mean().reset_index()
        year_current_df = df[df['date'].dt.year == current_year]
        max_week_current = year_current_df['WeekNumber'].max()

        # PLOT
        charts = ['map.png']
        for region in regions_to_include:
            plt.figure(figsize=(10, 6))  # Set the figure size
            plt.plot(average_df['WeekNumber'], average_df[region], label='Average Past 10 Years')
            plt.plot(year_current_df['WeekNumber'], year_current_df[region], label=current_year)

            plt.xlabel('WeekNumber')
            plt.ylabel(region)
            plt.title(f"Year-to-Date Temperature - {region}")

            plt.xlim(1, 52) # Set the x-axis limit based on the maximum WeekNumber for 2023
            plt.ylim(0,100)

            plt.legend()
            plt.savefig(f'static/{region}-chart.png')  # Save the chart as an image file
            plt.close()
            charts.append(f'{region}-chart.png')
            print(charts)

        return charts
    
    else:
        print("Failed to retrieve the data. Error:", response.status_code)