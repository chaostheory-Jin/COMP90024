import pandas as pd
crash_data = pd.read_csv("dsg_tasmania_crash_stats_2010_2020-7167587354022124293.csv")
city_list = crash_data[' location_description']

last_elements = []

for location in city_list:
    parts = location.split(',')
    last_element = parts[-1].strip()
    if " City" in last_element:
        last_element = last_element.replace(" City", "")
    last_elements.append(last_element)
    # processed_elements.append(cleaned_element)
crash_data[' location_description'] = last_elements

crash_data = crash_data[crash_data[' location_description'] != 'Not available']
crash_data = crash_data[crash_data[' location_description'] != 'Off road at Glamorgan-Spring Bay']
crash_data = crash_data[crash_data[' location_description'] != 'Break O\'Day']
# crash_data = crash_data[crash_data[' location_description'] != 'Not available']
# city_list = crash_data[' location_description']
# crash_data.to_csv("cleaned_tas_crash.csv")
# print(set(city_list))
crash_counts = crash_data.groupby([' crash_date', ' location_description']).size().reset_index(name='count')

crash_counts.to_csv("cleaned_tas_crash_num.csv")
# print(crash_counts)