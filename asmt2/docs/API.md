# CCC assignment2 API document

## Endpoints

### Endpoint 1: [weatherinsert]

- **URL**: `/weatherinsert/{index_name}`
- **Method**: `POST`
- **URL Params**
  - **Required**:
    - `index_name=[string]`
- **Data Params**
  - `[{"location": "BUSHY PARK (BUSHY PARK ESTATES)", "rain": "0.0", 
                                             "maxTemp": 18.1, "minTemp": 8.3, "day": "30", "month": "09",
                                               "year": "2018"}]`
- **Success Response**:
  - **Code**: `200`
  - **Content**: `{insertData: data_detail}`
- **Error Response**:
  - **Code**: `400`
  - **Content**: `{ "error": ErrorMessage }`
- **Notes**:
  - Weather insert only accept weatherstats & weathertest as index name

### Endpoint 2: [advanceeq]

- **URL**: `/advanceeq/indexname/{index}/date/{date}/location/{location}`
- **Method**: `GET`
- **URL Params**
  - **Required**:
    - `index=[string]`: The name of the index to be queried.
    - `date=[string]`: The date of the data to be queried. It can be `false` (i.e. not specify any date for the selected data) or a specific date string (e.g., "2021-01-01   or 2020").
    - `location=[string]`: The location of the data to be queried. It can be `false`(i.e. not specify any location for the selected data) or a specific location string (e.g., "Melbourne").
- **Data Params**
  - None (since this is a GET request)
- **Success Response**:
  - **Code**: `200`
  - **Content**: `{ "data": { /* Response data details here */ } }`
- **Error Response**:
  - **Code**: `200`
  - **Content**: `{ "error": "ErrorMessage" }`
- **Notes**:
  - Ensure that the index name and other parameters are valid and correctly formatted.
  - This endpoint retrieves data based on the specified parameters.

### Endpoint 3: [esquery]

- **URL**: `/esq/indexname/{index}`
- **Method**: `GET`
- **URL Params**
  - **Required**:
    - `index=[string]`: The name of the index to be queried.
- **Data Params**
  - None (since this is a GET request)
- **Success Response**:
  - **Code**: `200`
  - **Content**: `{ /* Response data details here */ }`
- **Error Response**:
  - **Code**: `200`
  - **Content**: `{ "error": "ErrorMessage" }`
- **Notes**:
  - Ensure that the index name is valid and correctly formatted.
  - This endpoint retrieves data based on the specified parameters.

### Endpoint 4: [weatherq]

- **URL**: `/weather/year/{year}/month/{month}/day/{day}/location/{location}/weatherstat/{weather}/bymonth/{bymonth}/index/{index}`
- **Method**: `GET`
- **URL Params**
  - **Required**:
    - `index=[string]`: The name of the index to be queried.
    - `year=[integer]`: The year of the data to be queried. It can be `false`(i.e. not specify any year for the selected data) or a specific year integer (e.g., 2020).
    - `month=[integer]`: The month of the data to be queried. It can be `false`(i.e. not specify any month for the selected data) or a specific year integer (e.g., 10).
    - `day=[integer]`: The day of the data to be queried. It can be `false`(i.e. not specify any day for the selected data) or a specific day integer (e.g., 16).
    - `location=[string]`: The location of the data to be queried. It can be `false`(i.e. not specify any location for the selected data) or a specific location string (e.g., "Melbourne").
    - `weather=[string]`: The state of weather to be queried. It should be a specific weather state string (e.g., "rain" or "maxTemp" or "minTemp").
    - `bymonth=[string]`: Whether the data to be queried is required to be grouped by each month. It should be `false` or `true`.
- **Data Params**
  - None (since this is a GET request)
- **Success Response**:
  - **Code**: `200`
  - **Content**: `{ /* Response data details here */ }`
- **Error Response**:
  - **Code**: `200`
  - **Content**: `{ "error": "ErrorMessage" }`
- **Notes**:
  - Ensure that the index name and other parameters are valid and correctly formatted.
  - This endpoint retrieves data based on the specified parameters.

### Endpoint 5: [fetchaud]
- **URL**: `/fetchaud`
- **Method**: `GET`
- **URL Params**: None (No URL parameters are required)
- **Data Params**: None (since this is a GET request)
- **Success Response**:
  - **Code**: `200`
  - **Content**: `{ /* Response data details here */ }`
- **Error Response**:
  - **Code**: `200`
  - **Content**: `{ "error": "ErrorMessage" }`
- **Notes**:
  - fetch dyanmic aud data from external everyday and insert to elasicsearch.

### Endpoint 6: [fetchbtc]
- **URL**: `/fetchbtc`
- **Method**: `GET`
- **URL Params**: None (No URL parameters are required)
- **Data Params**: None (since this is a GET request)
- **Success Response**:
  - **Code**: `200`
  - **Content**: `{ /* Response data details here */ }`
- **Error Response**:
  - **Code**: `200`
  - **Content**: `{ "error": "ErrorMessage" }`
- **Notes**:
  - fetch dyanmic btc data from external everyday and insert to elasicsearch.

### Endpoint 7: [fetchgold]
- **URL**: `/fetchgold`
- **Method**: `GET`
- **URL Params**: None (No URL parameters are required)
- **Data Params**: None (since this is a GET request)
- **Success Response**:
  - **Code**: `200`
  - **Content**: `{ /* Response data details here */ }`
- **Error Response**:
  - **Code**: `200`
  - **Content**: `{ "error": "ErrorMessage" }`
- **Notes**:
  - fetch dyanmic gold data from external everyday and insert to elasicsearch..

### Endpoint 8: [ftpcallstation]
- **URL**: `/ftpcallstation/{index}/{daterange}/{insertindex}`
- **Method**: `GET`
- **URL Params**:
  - **Required**:
    - `index=[string]`: The name of the index to be queried.
    - `daterange=[string]`: The date range for the query. eg '201209-202301'
    - `insertindex=[string]`: The index where the data will be inserted.
- **Data Params**: None (since this is a GET request)
- **Success Response**:
  - **Code**: `200`
  - **Content**: `{ /* Response data details here */ }`
- **Error Response**:
  - **Code**: `200`
  - **Content**: `{ "error": "ErrorMessage" }`
- **Notes**:
  - Ensure that the index name, date range, and insert index are valid and correctly formatted.
  - This endpoint retrieves and processes data based on the specified parameters.  

### Endpoint 9: [ftpfetchweather]
- **URL**: `/ftpfetchweather/{state}/{station}/{date}`
- **Method**: `GET`
- **URL Params**:
  - **Required**:
    - `state=[string]`: The state where the weather station is located.
    - `station=[string]`: The specific weather station to fetch data from.
    - `date=[string]`: The date for which the weather data is to be fetched. eg'201204'
- **Data Params**: None (since this is a GET request)
- **Success Response**:
  - **Code**: `200`
  - **Content**: `{ /* Response data details here */ }`
- **Error Response**:
  - **Code**: `200`
  - **Content**: `{ "error": "ErrorMessage" }`
- **Notes**:
  - Ensure that the state, station, and date are valid and correctly formatted.
  - This endpoint retrieves weather data based on the specified parameters.

### Endpoint 10: [qprice]
- **URL**: `/qprice/{index}`
- **Method**: `GET`
- **URL Params**:
  - **Required**:
    - `index=[string]`: The name of the index to be queried. [audrate, goldprice, btcprice]
- **Data Params**: None (since this is a GET request)
- **Success Response**:
  - **Code**: `200`
  - **Content**: `{ /* Response data details here */ }`
- **Error Response**:
  - **Code**: `200`
  - **Content**: `{ "error": "ErrorMessage" }`
- **Notes**:
  - Ensure that the index name is valid and correctly formatted.
  - This endpoint retrieves price data based on the specified index.


### Endpoint 11: [qstation]
- **URL**: `/qstation/{index}`
- **Method**: `GET`
- **URL Params**:
  - **Required**:
    - `index=[string]`: The name of the index to be queried. [pollenstaion, crashstation]
- **Data Params**: None (since this is a GET request)
- **Success Response**:
  - **Code**: `200`
  - **Content**: `{ /* Response data details here */ }`
- **Error Response**:
  - **Code**: `200`
  - **Content**: `{ "error": "ErrorMessage" }`
- **Notes**:
  - Ensure that the index name is valid and correctly formatted.
  - This endpoint retrieves station data based on the specified index.

### Endpoint 12: [ftpcallstationperday]
- **URL**: `/ftpcallstationperday`
- **Method**: `GET`
- **URL Params**: None (No URL parameters are required)
- **Data Params**: None (since this is a GET request)
- **Success Response**:
  - **Code**: `200`
  - **Content**: `{ /* Response data details here */ }`
- **Error Response**:
  - **Code**: `200`
  - **Content**: `{ "error": "ErrorMessage" }`
- **Notes**:
  - fetch dyanmic data from ftp server everyday.

### Endpoint 13: [canalysis]

- **URL**: `/canalysis/year/{year}/crash/{locationc}/weather/{locationw}`
- **Method**: `GET`
- **URL Params**
  - **Required**:
    - `year=[integer]`: The year of the data to be selected and analysed. It should be a specific year integer (e.g., 2020).
    - `locationc=[string]`: The location of crash data to be selected and analysed. It should be a specific location string (e.g., "Melbourne").
    - `locationw=[string]`: The state of weather data to be selected and analysed. It should be a specific location string (e.g., "Melbourne").
- **Data Params**
  - None (since this is a GET request)
- **Success Response**:
  - **Code**: `200`
  - **Content**: `{ /* Response data details here */ }`
- **Error Response**:
  - **Code**: `200`
  - **Content**: `{ "error": "ErrorMessage" }`
- **Notes**:
  - Ensure that the parameters are valid and correctly formatted.
  - This endpoint retrieves data based on the specified parameters.

### Endpoint 14: [panalysis]

- **URL**: `/panalysis/year/{year}/pollen/{locationp}/weather/{locationw}`
- **Method**: `GET`
- **URL Params**
  - **Required**:
    - `year=[integer]`: The year of the data to be selected and analysed. It should be a specific year integer (e.g., 2020).
    - `locationp=[string]`: The location of pollen data to be selected and analysed. It should be a specific location string (e.g., "Melbourne").
    - `locationw=[string]`: The state of weather data to be selected and analysed. It should be a specific location string (e.g., "Melbourne").
- **Data Params**
  - None (since this is a GET request)
- **Success Response**:
  - **Code**: `200`
  - **Content**: `{ /* Response data details here */ }`
- **Error Response**:
  - **Code**: `200`
  - **Content**: `{ "error": "ErrorMessage" }`
- **Notes**:
  - Ensure that the parameters are valid and correctly formatted.
  - This endpoint retrieves data based on the specified parameters.

### Endpoint 15: [ganalysis]

- **URL**: `/ganalysis/fill/{fill}/startdate/{start}/enddate/{end}`
- **Method**: `GET`
- **URL Params**
  - **Required**:
    - `fill=[integer]`: Whether the missing value will be filled in automatically. It should be `false` or `true`.
    - `start=[string]`: The start date of the required data (e.g., "2016-09-13").
    - `end=[string]`: The end date of the required data (e.g., "2016-10-20")..
- **Data Params**
  - None (since this is a GET request)
- **Success Response**:
  - **Code**: `200`
  - **Content**: `{ /* Response data details here */ }`
- **Error Response**:
  - **Code**: `200`
  - **Content**: `{ "error": "ErrorMessage" }`
- **Notes**:
  - Ensure that the parameters are valid and correctly formatted.
  - This endpoint retrieves data based on the specified parameters.

### Endpoint 16: [ianalysis]
- **URL**: `/ianalysis`
- **Method**: `GET`
- **URL Params**: None (No URL parameters are required)
- **Data Params**: None (since this is a GET request)
- **Success Response**:
  - **Code**: `200`
  - **Content**: `{ /* Response data details here */ }`
- **Error Response**:
  - **Code**: `200`
  - **Content**: `{ "error": "ErrorMessage" }`
- **Notes**:
  - this function retrieves the data of income after analyses.