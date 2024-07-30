import pandas as pd
import numpy as np


def haversine(lon1, lat1, lon2, lat2):
    lon1, lat1, lon2, lat2 = map(np.radians, [lon1, lat1, lon2, lat2])
    
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    
    # Haversine
    a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
    c = 2 * np.arcsin(np.sqrt(a))
    
    r = 6371
    return c * r

stations = []
with open("station_tas.txt", "r") as file:
    for line in file:
        parts = line.strip().split()
        latitude = float(parts[-2])
        longitude = float(parts[-1])
        station_name = '_'.join(parts[2:-2])
        stations.append((station_name, latitude, longitude))

crash_data = pd.read_csv("test_cleaned_tas_crash_num_with_coords.csv")

def find_nearest_station(lat, lon):
    distances = [haversine(lon, lat, s_lon, s_lat) for _, s_lat, s_lon in stations]
    nearest_station_index = np.argmin(distances)
    return stations[nearest_station_index][0]

crash_data['nearest_station'] = crash_data.apply(lambda row: find_nearest_station(row['average_latitude'], row['average_longitude']), axis=1)

crash_data['location_description'] = crash_data['nearest_station']

crash_data.to_csv("crash_data_with_nearest_stations.csv", index=False)
