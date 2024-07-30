import unittest
import requests
import json
import time
    
class HTTPSession: 
    def __init__(self, protocol, host, port):
        self.session = requests.Session()
        self.base_url = f'{protocol}://{host}:{port}'

    def get(self, path):
        response = self.session.get(f'{self.base_url}{path}')
        return response
    
    def post(self, path, data):
        response = self.session.post(f'{self.base_url}{path}', json=data)
        return response
    
    def put(self, path, data):
        response = self.session.put(f'{self.base_url}{path}', json=data)
        return response
    
    def delete(self, path):
        response = self.session.delete(f'{self.base_url}{path}')
        return response

class TestHTTPSession(unittest.TestCase):
    def setUp(self):
        self.assertEqual(test_request.delete("/wipetestdatabase").status_code, 200)
        time.sleep(1)

    def test_insert(self):
        # test correct action
        self.assertEqual(test_request.post("/weatherinsert/weathertest", 
                                           data=[{"location": "BUSHY PARK (BUSHY PARK ESTATES)", "date":"30/09/2018", "rain": "0.0", 
                                             "maxTemp": 18.1, "minTemp": 8.3, "day": "30", "month": "09",
                                               "year": "2018"}]).status_code, 200)
        # test incorrect index name
        self.assertEqual(test_request.post("/weatherinsert/weathertest1",  
                                           data=[{"location": "BUSHY PARK (BUSHY PARK ESTATES)", "date":"30/09/2018", "rain": "0.0", 
                                             "maxTemp": 18.1, "minTemp": 8.3, "day": "30", "month": "09",
                                               "year": "2018"}]).status_code, 400)

        # test invalid input data format
        self.assertEqual(test_request.post("/weatherinsert/weathertest",{}).status_code, 500)

        r = test_request.post("/weatherinsert/weathertest",[{}])
        self.assertEqual( "error" in r.text, True)
    



        self.assertEqual(test_request.post("/weatherinsert/weathertest", 
                                           data=[{"location": "BUSHY PARK (BUSHY PARK ESTATES)", "date":"30/09/2018", "rain": "0.0", 
                                            "minTemp": 8.3, "day": "30", "month": "09",
                                               "year": "2018"}]).status_code, 200)


    def test_fetch(self):
        self.assertEqual(test_request.get("/ftpfetchweather").status_code, 404)
        self.assertEqual(test_request.get("/ftpfetchweather/location").status_code, 404)

        r = test_request.get("/ftpfetchweather/notexistlocation/notexiststation/date")
        self.assertEqual( "500" in r.text, True)
        self.assertEqual( "Error" in r.text, True)

        self.assertEqual(test_request.get("/ftpfetchweather/qld/warwick/202404").status_code, 200)
        r = test_request.get("/ftpfetchweather/qld/warwick/202404")
        self.assertEqual(r.status_code, 200)
        data = r.json()
        self.assertEqual(data["data"][0]["location"], "WARWICK")
        self.assertEqual(data["data"][0]["date"], "01/04/2024")

        r = test_request.get("/fetchgold")
        self.assertEqual(r.status_code, 200)
        self.assertEqual("error" in r.text, False)

        r = test_request.get("/fetchaud")
        self.assertEqual(r.status_code, 200)
        self.assertEqual("error" in r.text, False)

        r = test_request.get("/fetchbtc")
        self.assertEqual(r.status_code, 200)
        self.assertEqual("error" in r.text, False)
        #check aud/btc

    def test_harvest(self):

        self.assertEqual(test_request.get("/ftpcallstation/errorindex").status_code, 404)
        self.assertEqual(test_request.get("/ftpcallstation/crash/").status_code, 404)

        self.assertEqual(test_request.get("/ftpcallstation/crash/201704-201705").status_code, 404)

        r = test_request.get("/ftpcallstation/crashstation/201704-201705/errorindex")

        self.assertEqual( "500" in r.text, True)
        self.assertEqual( "Error" in r.text, True)
        
        r = test_request.get("/ftpcallstation/crashstation/209904-209905/weathertest")
        self.assertEqual( "500" in r.text, True)
        self.assertEqual( "Error" in r.text, True)

        r = test_request.get("/ftpcallstation/errorstation/201704-201705/weathertest")
        self.assertEqual( "500" in r.text, True)
        self.assertEqual( "Error" in r.text, True)

        # r = test_request.get("/ftpcallstation/pollen/201804-201804/weathertest")
        # self.assertEqual(r.status_code, 200)
        # r = test_request.get("/esq/indexname/weathertest")
        # self.assertEqual(r.status_code, 200)
        # self.assertNotEqual(len(r.json()["hits"]), 0)



    def test_query_stationList(self):

        self.assertEqual(test_request.get("/qstation").status_code, 404)

        r = test_request.get("/qstation/pollenstation")
        r = r.json()
        self.assertEqual(r["hits"][0]["_source"]["stationname"], "brisbane")

        r = test_request.get("/qstation/errorindex")
        r = r.json()
        self.assertEqual(len(r["hits"]), 0)



    def test_query_weather(self):
        self.assertEqual(test_request.get("/weatherq").status_code, 404)
        self.assertEqual(test_request.get("/weatherq/year").status_code, 404)
        self.assertEqual(test_request.get("/weatherq/year/wrongdate").status_code, 404)


        r = test_request.get("/weather/year/2018/month/9/day/15/location/brisbane/weatherstat/rain/bymonth/true/index/weatherstats")
        self.assertEqual(r.status_code, 200)
        r = r.json()
        self.assertEqual(r["groupby"]["buckets"][0]["key"]["year"], 2018)

        r = test_request.get("/weather/year/2018/month/9/day/15/location/brisbane/weatherstat/rain/bymonth/false/index/weatherstats")
        self.assertEqual(r.status_code, 200)
        r = r.json()
        self.assertEqual(r["hits"][0]["fields"]["year"][0], 2018)

        r = test_request.get("/weather/year/2050/month/9/day/15/location/brisbane/weatherstat/maxTemp/bymonth/true/index/weatherstats")
        self.assertEqual(r.status_code, 200)
        r = r.json()
        self.assertEqual(len(r["groupby"]["buckets"]),0)
        r = test_request.get("/weather/year/2018/month/9/day/15/location/brisbane/weatherstat/maxTemp/bymonth/true/index/weatherstats")    
        
        r = test_request.get("/weather/year/2050/month/9/day/15/location/test/weatherstat/maxTemp/bymonth/false/index/weatherstats")
        self.assertEqual(r.status_code, 200)
        r = r.json()
        self.assertEqual(len(r["hits"]),0)

        r = test_request.get("/weather/year/2018/month/9/day/15/location/brisbane/weatherstat/maxTemp/bymonth/true/index/weatherstats")   

    def test_getAll_query(self):
        
        self.assertEqual(test_request.get("/esq").status_code, 404)
        
        r = test_request.get("/esq/indexname/crash")
        self.assertEqual(r.status_code, 200)
        r = r.json()
        self.assertNotEqual(len(r["hits"]), 0)

        r = test_request.get("/esq/indexname/errorindex")
        self.assertEqual( "500" in r.text, True)
        self.assertEqual( "Error" in r.text, True)

        r = test_request.get("/qprice/audrate")
        self.assertEqual(r.status_code, 200)
        r = r.json()
        self.assertNotEqual(len(r["hits"]), 0)

        

    def test_advanceeq_query(self):
            
            self.assertEqual(test_request.get("/advanceeq").status_code, 404)

            r = test_request.get("/advanceeq/indexname/pollen/date/2018/location/brisbane")
            self.assertEqual(r.status_code, 200)
            r = r.json()
            self.assertEqual(r["hits"][0]["_source"]["location"], "BRISBANE")
            self.assertEqual(r["hits"][0]["_index"], "pollen")

            r = test_request.get("/advanceeq/indexname/pollen/date/2018/location/errorlocation")
            self.assertEqual(r.status_code, 200)
            r = r.json()
            self.assertEqual(len(r["hits"]), 0)

            r = test_request.get("/advanceeq/indexname/pollen/date/2099/location/brisbane")
            self.assertEqual(r.status_code, 200)
            r = r.json()
            self.assertEqual(len(r["hits"]), 0)

            r = test_request.get("/advanceeq/indexname/errorindex/date/2018/location/brisbane")
            self.assertEqual(r.status_code, 200)
            r = r.json()
            self.assertEqual(len(r["hits"]), 0)

    def test_analysis(self):
        self.assertEqual(test_request.get("/canalysis").status_code, 404)
        self.assertEqual(test_request.get("/canalysis/year").status_code, 404)

        r = test_request.get("/canalysis/year/2018/crash/mount_read/weather/MOUNT%20READ")
        self.assertEqual(r.status_code, 200)
        r = r.json()
        self.assertNotEqual(len(r), 0)

        r = test_request.get("/canalysis/year/2018/crash/mount_read/weather/errorlocation")
        self.assertEqual(r.status_code, 200)
        r = r.json()
        self.assertEqual(r["error"], "'date'")
        
        
        r = test_request.get("/canalysis/year/2077/crash/mount_read/weather/MOUNT%20READ")
        self.assertEqual(r.status_code, 200)
        r = r.json()
        self.assertEqual(r["error"], "'date'")



        self.assertEqual(test_request.get("/panalysis").status_code, 404)
        self.assertEqual(test_request.get("/panalysis/year").status_code, 404)

        r = test_request.get("/panalysis/year/2018/pollen/brisbane/weather/BRISBANE")
        self.assertEqual(r.status_code, 200)
        r = r.json()
        self.assertNotEqual(len(r), 0)
        self.assertEqual( "BRISBANE" in r, True)


        self.assertEqual(test_request.get("/ganalysis").status_code, 404)
        self.assertEqual(test_request.get("/ganalysis/fill").status_code, 404)


        r = test_request.get("/ganalysis/fill/false/startdate/2077-09-13/enddate/2077-10-20")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.text == "\"[]\"", True)

        r = test_request.get("/ganalysis/fill/true/startdate/2077-09-13/enddate/2077-10-20")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.text == "\"[]\"", True)


        r = test_request.get("/ganalysis/fill/true/startdate/2016-09-13/enddate/2016-10-20")
        self.assertEqual(r.status_code, 200)
        self.assertEqual("BitcoinPrice" in r.text, True)

        r = test_request.get("/ganalysis/fill/false/startdate/2016-09-13/enddate/2016-10-20")
        self.assertEqual(r.status_code, 200)
        self.assertEqual("BitcoinPrice" in r.text, True)

        r = test_request.get("/ganalysis/fill/test/startdate/2016-09-13/enddate/2016-10-20")
        self.assertEqual(r.status_code, 200)
        self.assertEqual("BitcoinPrice" in r.text, True)


        r = test_request.get("/ganalysis/fill/false/startdate/2016-09-13/enddate/test")
        self.assertEqual(r.status_code, 200)
        self.assertEqual("error" in r.text, True)



        r = test_request.get("/ianalysis")
        self.assertEqual(r.status_code, 200)
        self.assertEqual("MeanWeekly" in r.text, True)


    # def test_analysis(self):
if __name__ == '__main__':
    test_request = HTTPSession('http', 'localhost', 9090)
    unittest.main()