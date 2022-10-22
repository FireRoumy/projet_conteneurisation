from datetime import datetime
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS, ASYNCHRONOUS

token = "'bmDLXMwdrf95qc8mMhoTm-nZLcDnYNge-j7vRWgicWHFAC5Rz4dGfhWEr6_B8hFATArCyvtJ3JQespdURJ8Psg=='"
org = "grandlyon"
bucket = "grandlyon-data"

class InfluxClient:
    def __init__(self,token,org,bucket): 
        self._org=org 
        self._bucket = bucket
        self._client = InfluxDBClient(url="http://localhost:8086", token=token)

    def write_data(self,data,write_option=SYNCHRONOUS):
        write_api = self._client.write_api(write_option)
        write_api.write(self._bucket, self._org , data,write_precision='s')

IC = InfluxClient(token,org,bucket)

# Data Write Method 1
IC.write_data(["testTKT,tagtest=tagtest2 Open=62.79,High=63.84,Low=62.13"])