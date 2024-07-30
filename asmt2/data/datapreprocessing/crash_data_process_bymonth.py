import pandas as pd
from dateutil import parser

df = pd.read_csv('cleaned_tas_crash_num.csv')

df['date_month'] = df[' crash_date'].apply(lambda x: parser.parse(x).strftime('%Y-%m'))

grouped = df.groupby([' location_description', 'date_month']).agg({'count': 'sum'}).reset_index()

grouped.rename(columns={'location_description': 'location'}, inplace=True)

grouped.to_csv('grouped_data.csv', index=False)

