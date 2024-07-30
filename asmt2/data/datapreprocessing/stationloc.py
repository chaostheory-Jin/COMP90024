import csv
import re

# Input text data
data = """095003  TAS 95    BUSHY PARK (BUSHY PARK ESTATES)          18740101..      -42.7097 146.8983  
096003  TAS 96    BUTLERS GORGE                            19410101..      -42.2753 146.2758  
094212  TAS 94    CAMPANIA (KINCORA)                       20000406..      -42.6867 147.4258  
094198  TAS 94    CAPE BRUNY (CAPE BRUNY)                  19970516..      -43.4886 147.1444  
091331  TAS 91    CAPE GRIM                                20101216..      -40.6764 144.6922  
097000  TAS 97    CAPE SORELL                              18990101..      -42.1986 145.17    
091375  TAS 91    CRESSY (BRUMBYS CREEK)                   20220929..      -41.7114 147.082   
094255  TAS 94    DENNES POINT                             20120926..      -43.0639 147.3567  
091126  TAS 91    DEVONPORT AIRPORT                        19620601..      -41.1701 146.4289  
094254  TAS 94    DUNALLEY (STROUD POINT)                  20120307..      -42.9017 147.7894  
092163  TAS 92    FINGAL (FLEMING ST)                      20220721..      -41.643  147.98    
099005  TAS 99    FLINDERS ISLAND AIRPORT                  19420101..      -40.0911 148.0024  
092114  TAS 92    FRIENDLY BEACHES                         19970220..      -41.9953 148.2794  
094220  TAS 94    GROVE (RESEARCH STATION)                 20040611..      -42.9844 147.0756  
094191  TAS 97    HARTZ MOUNTAIN (KEOGHS PIMPLE)           19940101..      -43.2006 146.7683  
094029  TAS 94    HOBART (ELLERSLIE ROAD)                  18820101..      -42.8897 147.3278  
094250  TAS 94    HOBART AIRPORT                           20170605..      -42.8333 147.5119  
098017  TAS 98    KING ISLAND AIRPORT                      19620101..      -39.8804 143.8857  
094087  TAS 94    KUNANYI (MOUNT WELLINGTON PINNACLE)      19610101..      -42.895  147.2358  
092045  TAS 92    LARAPUNA (EDDYSTONE POINT)               19080101..      -40.9928 148.3467  
091237  TAS 91    LAUNCESTON (TI TREE BEND)                19800507..      -41.4194 147.1219  
091311  TAS 91    LAUNCESTON AIRPORT                       20040614..      -41.5476 147.2156  
096033  TAS 96    LIAWENEE                                 20010109..      -41.8997 146.6694  
091293  TAS 91    LOW HEAD                                 19971106..      -41.0547 146.7874  
097080  TAS 97    LOW ROCKY POINT                          19920316..      -42.9831 145.5025  
091259  TAS 91    LUNCHEON HILL (FORESTRY)                 19890101..      -41.1492 145.1517  
094041  TAS 94    MAATSUYKER ISLAND LIGHTHOUSE             18911001..      -43.6578 146.2711  
092124  TAS 92    MARIA ISLAND (POINT LESUEUR)             20040527..      -42.6621 148.0179  
097085  TAS 97    MOUNT READ                               19960910..      -41.8444 145.5417  
095048  TAS 95    OUSE FIRE STATION                        19731009..      -42.4842 146.7106  
097083  TAS 97    SCOTTS PEAK DAM                          19920101..      -43.0425 146.2722  
091219  TAS 91    SCOTTSDALE (WEST MINSTONE ROAD)          19710303..      -41.1708 147.4883  
091291  TAS 91    SHEFFIELD SCHOOL FARM                    19961213..      -41.389  146.3173  
091292  TAS 91    SMITHTON AERODROME                       19961114..      -40.8347 145.0847  
092120  TAS 92    ST HELENS AERODROME                      20010110..      -41.3381 148.2792  
097072  TAS 97    STRAHAN AERODROME                        19760101..      -42.155  145.2908  
092123  TAS 92    SWAN ISLAND                              20011022..      -40.7292 148.125   
094155  TAS 94    TASMAN ISLAND                            19770101..      -43.2397 148.0025  
094195  TAS 94    TUNNACK FIRE STATION                     19970813..      -42.4543 147.4612  
097024  TAS 97    WARRA                                    20040928..      -43.0609 146.704   
091107  TAS 91    WYNYARD AIRPORT                          19470101..      -40.9964 145.7311"""

# Regular expression pattern to match the relevant columns
pattern = re.compile(r'(\d{6})\s+TAS\s+\d{2}\s+([A-Z ()]+?)\s+\d{8}\.\.\s+(-\d+\.\d+)\s+(\d+\.\d+)')

# Open a CSV file to write the extracted data
with open('location_data.csv', 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['Location', 'Latitude', 'Longitude'])

    # Iterate through each line and extract the relevant data using the regex pattern
    for line in data.split('\n'):
        match = pattern.search(line)
        if match:
            location = match.group(2).strip()
            latitude = match.group(3)
            longitude = match.group(4)
            csvwriter.writerow([location, latitude, longitude])

print('CSV file created successfully.')
