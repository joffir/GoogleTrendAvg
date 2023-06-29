import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Use the 'Agg' backend, avoids multithreading issues with matplotlib
import matplotlib.pyplot as plt
from datetime import datetime
from pytrends.request import TrendReq

def generate_chart(keyword_in):
    current_year = datetime.now().year # Current year so the code can be reused in the future

    # PYTRENDS
    pytrends = TrendReq(hl='en-US', tz=360)
    keyword = keyword_in
    timeframe = 'today 5-y'
    pytrends.build_payload([keyword], timeframe=timeframe)
    trends_data = pytrends.interest_over_time()
    trends_data = trends_data.reset_index()
    trends_data.to_csv('trends.csv', index=False)

    # Read the CSV file into a DataFrame
    df = pd.read_csv('trends.csv')

    df['date'] = pd.to_datetime(df['date'])
    df['WeekNumber'] = df['date'].apply(lambda x: datetime.strftime(x, "%U"))

    filtered_df = df[df['date'].dt.year < current_year]
    average_df = filtered_df.groupby('WeekNumber')[keyword].mean().reset_index()
    year_current_df = df[df['date'].dt.year == current_year]
    max_week_current = year_current_df['WeekNumber'].max()

    plt.figure(figsize=(10, 6))  # Set the figure size
    plt.plot(average_df['WeekNumber'], average_df[keyword], label='Average Past 4 Years')
    plt.plot(year_current_df['WeekNumber'], year_current_df[keyword], label=current_year)
    plt.xlabel('WeekNumber')
    plt.ylabel(keyword)
    plt.title('Google Trends: '+ keyword)
    plt.xlim(0, 52) # Set the x-axis limit based on the maximum WeekNumber for 2023 max_week_current
    plt.legend()
    plt.savefig('static/chart.png')  # Save the chart as an image file
    plt.close()

    # ANOTHER CHART
    yearsub_1_current_df = df[df['date'].dt.year == (current_year - 1)]
    yearsub_2_current_df = df[df['date'].dt.year == (current_year - 2)]
    yearsub_3_current_df = df[df['date'].dt.year == (current_year - 3)]
    yearsub_4_current_df = df[df['date'].dt.year == (current_year - 4)]

    plt.figure(figsize=(10, 6))  # Set the figure size

    plt.plot(average_df['WeekNumber'], average_df[keyword], label='Average Past 4 Years', linewidth=2.5, linestyle='solid')
    plt.plot(year_current_df['WeekNumber'], year_current_df[keyword], label=current_year, linewidth=2.5, linestyle='solid')
    plt.plot(yearsub_1_current_df['WeekNumber'], yearsub_1_current_df[keyword], label=(current_year-1), linewidth=1.0, linestyle='dashed')
    plt.plot(yearsub_2_current_df['WeekNumber'], yearsub_2_current_df[keyword], label=(current_year-2), linewidth=1.0, linestyle='dashed')
    plt.plot(yearsub_3_current_df['WeekNumber'], yearsub_3_current_df[keyword], label=(current_year-3), linewidth=1.0, linestyle='dashed')
    plt.plot(yearsub_4_current_df['WeekNumber'], yearsub_4_current_df[keyword], label=(current_year-4), linewidth=1.0, linestyle='dashed')

    plt.xlabel('WeekNumber')
    plt.ylabel(keyword)
    plt.title('Google Trends: '+ keyword)
    plt.xlim(0, 52) # Set the x-axis limit based on the maximum WeekNumber for 2023
    plt.legend()
    plt.savefig('static/chart2.png')  # Save the chart as an image file
    plt.close()

# FOR TEST:
#generate_chart('ac repair')