import requests
import json
import matplotlib.pyplot as plt
from datetime import datetime

# URL of the NOAA JSON data
url = "https://www.ncei.noaa.gov/access/monitoring/us-weekly/wkly.json"

# Send a GET request to retrieve the JSON data
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the JSON data
    data = json.loads(response.text)

    # Extract the temperature data
    temperature_data = data["data"]

    # Prepare a list to store the dates
    dates = []

    # Prepare a dictionary to store the average temperatures for each region
    region_temperatures = {}

    # Regions to include in the chart
    regions_to_include = [
        "ne",
        "enc",
        "c",
        "se",
        "wnc",
        "s",
        "sw",
        "nw",
        "w",
        "nat"
    ]

    # Iterate over the temperature data
    for date, temperatures in temperature_data.items():
        # Extract the date
        dates.append(date)

        # Iterate over each region's temperature
        for region, temp in temperatures.items():
            if region in regions_to_include:
                if region not in region_temperatures:
                    region_temperatures[region] = []
                region_temperatures[region].append(float(temp))

    # Plot the data for each region
    for region, temps in region_temperatures.items():
        # Calculate the number of weeks passed in the current year
        current_date = datetime.now()
        year_to_date_weeks = (current_date - datetime(current_date.year, 1, 1)).days // 7 + 1

        # Limit the data to the year-to-date period
        year_to_date_temps = temps[:year_to_date_weeks]

        # Generate x-axis values for the weeks
        x_values = list(range(1, len(year_to_date_temps) + 1))

        # Plot the data
        plt.plot(x_values, year_to_date_temps)

        plt.xlabel("Week")
        plt.ylabel("Average Temperature (deg F)")
        plt.title(f"Year-to-Date Temperature - {region}")

        # Show or save the chart as desired
        plt.show()

else:
    print("Failed to retrieve the data. Error:", response.status_code)
