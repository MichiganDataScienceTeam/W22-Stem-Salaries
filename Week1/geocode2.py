import time
import pandas as pd
import numpy as np
import geopy as geo
from geopy.geocoders import Nominatim
import plotly.io as pio
pio.renderers.default = 'iframe_connected'

salaries = pd.read_csv("stem_salaries_data.csv")
unique = pd.read_csv("unique_locations.csv")
lat = []
long = []
# for i in range(1, len(salaries["location"])):
for i in range(0, len(salaries["location"])):
    searching = True
    city = salaries["location"][i]
    temp = unique["name"]
    t_i = 0
    mid_i = 0
    r = False
    last_e = -1
    start_e = -1
    while searching:
        prev_i = mid_i
        if r == False:
            mid_i = mid_i + int(len(temp) / 2)
        elif r == True:
            mid_i = mid_i - int(len(temp) / 2)
        # print("city is " + city)
        if len(temp) == 2:
            if temp[start_e] == city:
                searching = False
                lat.append(unique["lat"][start_e])
                long.append(unique["long"][start_e])
            elif temp[last_e] == city:
                searching = False
                lat.append(unique["lat"][last_e])
                long.append(unique["long"][last_e])
        elif mid_i == 0:
            mid_i = prev_i
            searching = False
            lat.append(unique["lat"][mid_i])
            long.append(unique["long"][mid_i])
        elif len(temp) == 1:
            try:
                if temp[mid_i] == city:
                    searching = False
                    lat.append(unique["lat"][mid_i])
                    long.append(unique["long"][mid_i])
            except:
                try:
                    if temp[mid_i + 1] == city:
                        searching = False
                        lat.append(unique["lat"][mid_i + 1])
                        long.append(unique["long"][mid_i + 1])
                except:
                    if temp[mid_i - 1] == city:
                        searching = False
                        lat.append(unique["lat"][mid_i - 1])
                        long.append(unique["long"][mid_i - 1])

        elif temp[mid_i] == salaries["location"][i]:
            searching = False
            lat.append(unique["lat"][mid_i])
            long.append(unique["long"][mid_i])
        elif temp[mid_i] < salaries["location"][i]:
            r = False
            temp = unique["name"][mid_i:mid_i + round(len(temp)/2) + 1]
            start_e = mid_i
            last_e = mid_i + int(round(len(temp)/2)) - 1
            # n_temp = temp[mid_i:]
            # temp = []
            # temp = n_temp
        elif temp[mid_i] > salaries["location"][i]:
            r = True
            temp = []
            temp = unique["name"][mid_i - abs(prev_i - mid_i):mid_i]
            start_e = mid_i - abs(prev_i - mid_i)
            last_e = mid_i - 1
        t_i = t_i + 1
        if t_i > 10000:
            print("error! u cannot code LMAO")
            searching = False
            lat.append(float('NaN'))
            long.append(float('NaN'))
    print(str(i) + ": " + city + " is at " + str(float(lat[i])) + ", " + str(float(long[i])))
salaries["lat"] = lat
salaries["long"] = long
salaries.to_csv("salaries_geocoded.csv")
# for u_i in range(1, len(unique_locations)):
#     for i in range(1, salaries["location"]):
#         if salaries["location"][i] == unique_locations[u_i]:
#             salaries["lat"] = lat_u[u_i]
#             salaries["long"] = long_u[u_i]