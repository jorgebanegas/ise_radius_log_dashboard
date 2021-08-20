""" Copyright (c) 2021 Cisco and/or its affiliates.
This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at
           https://developer.cisco.com/docs/licenses
All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied. 
"""

import requests
import json
import config

from requests.sessions import session
import pprint
from requests.auth import HTTPBasicAuth
from pymongo import MongoClient
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
import ad

client = MongoClient()
db = client['logs']
collection = db['radius_logs']

try:
    requests.packages.urllib3.disable_warnings()
except:
    pass

def create_json(browser_headers):
    headers = browser_headers.split("\n")
    headers_dict = {}

    for header in headers:
        header = header.partition(":")
        key = header[0]

        value = header[2]

        headers_dict[key] = value.strip()

    return headers_dict




class ISE:
    def __init__(self, host, username, password):
        self.host = host
        self.__BASE_URL = "https://{host}:9060/ers/".format(host=host)
        self.__username = username
        self.__password = password
        self.__headers = {'Accept': 'application/json'}
        self.__session = self.ui_auth(username,password)

    def ui_auth(self, username, password):
        headers = create_json("""""")


        payload = create_json("""""")
        login_url = "https://%s/admin/LoginAction.do" % self.host
        request = requests.session()
        response = request.post(url=login_url, data=payload, verify=False, headers=headers)
        print(request.cookies.get_dict())

        return request

    def get_radius_logs(self):
        
        headers = create_json("""""")
        
        headers['Cookie'] = "APPSESSIONID={appsessionid}".format(appsessionid=self.__session.cookies.get_dict()['APPSESSIONID'])


        pprint.pprint(headers)
        
        url = "https://%s/admin/rs/uiapi/mnt/livesession"%(self.host)
        response = self.__session.get(url, auth=HTTPBasicAuth(self.__username, self.__password),headers=headers,verify=False)
        self.__session.close()
        if response.status_code == 200:
            return json.loads(response.content)
        else:
            print(response.status_code)
            raise Exception


def collect():
    client = MongoClient()
    db = client['logs']
    collection = db['radius_logs']

    temp = []
    today = datetime.today()
    day = today.strftime("%Y-%d-%m")
    day = str(day).split(" ")[0]
    ise = ISE(config.hostname, config.username,config.password)
    radius_logs = ise.get_radius_logs()
    myquery = { "date": str(day) }
    mydoc = collection.find(myquery)

    for x in mydoc:
        temp.append(x.get("username"))
    
    pprint.pprint(radius_logs)
    
    for radius_log in radius_logs:
        try:
            datetime_time = datetime.fromtimestamp(radius_log["session_start_time"]/1000)
            date = str(datetime_time).split(" ")[0]
            time = str(datetime_time).split(" ")[1]
        except Exception as e: 
            print("Error: " + e)
            print("Error parsing start time : ",str(radius_log))
            continue
        if radius_log["username"] not in temp:
            ads = ad.get_active_directories()
            #pprint.pprint(ads)
            ads = ads[0]
            groups = ad.get_ad_groups(ads["id"],radius_log["username"])
            if groups == None:
                continue
            data  = {"username":radius_log["username"],"adgroup":groups,"date":date,"time":time}
            collection.insert_one(data)
            print("Username : ",radius_log["username"]," AD Group : ",str(groups)," Date : ",date)


scheduler = BlockingScheduler()
scheduler.add_job(collect, 'interval', minutes=1)
scheduler.start()