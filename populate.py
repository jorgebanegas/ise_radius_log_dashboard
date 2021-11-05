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
import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
import ad

client = MongoClient()
db = client['logs']
collection = db['radius_logs']


def get_radius_logs():

    url = "https://" + config.hostname + ":8910/pxgrid/mnt/sd/getSessions"
    time_5mins = datetime.datetime.now() - datetime.timedelta(minutes=5)

    data= {"startTimestamp": time_5mins.isoformat()}
    headers = {
    'Accept-Language': 'application/json',
    'Content-Type': 'application/json',
    }

    response = requests.request("POST", url, headers=headers,  data=json.dumps(data),auth = HTTPBasicAuth(config.pxgrid_user, config.pxgrid_secret))

    return response.json()


def collect():
    client = MongoClient()
    db = client['logs']
    collection = db['radius_logs']

    temp = []
    today = datetime.datetime.today()
    day = today.strftime("%Y-%d-%m")
    day = str(day).split(" ")[0]
    radius_logs = get_radius_logs()
    myquery = { "date": str(day) }
    mydoc = collection.find(myquery)

    for x in mydoc:
        temp.append(x.get("username"))
    
    pprint.pprint(radius_logs)
    
    for radius_log in radius_logs['sessions']:
        try:
            date = radius_log["timestamp"].split('T')[0]
            date = datetime.datetime.strptime(date, "%Y-%m-%d").strftime("%Y-%d-%m")
           
            time = radius_log["timestamp"].split('T')[1]
            time = time.split('-')[0]
            time = datetime.datetime.strptime(time,'%H:%M:%S').strftime('%I:%M %p')
        except Exception as e: 
            print("Error: " + e)
            print("Error parsing start time : ",str(radius_log))
            continue
        if radius_log["state"] == "STARTED" and radius_log["userName"] not in temp:
            ads = ad.get_active_directories()
            #pprint.pprint(ads)
            ads = ads[0]
            groups = ad.get_ad_groups(ads["id"],radius_log["userName"])
            if groups == None:
                continue
            data  = {"username":radius_log["userName"],"adgroup":groups,"date":date,"time":time}
            collection.insert_one(data)
            print("Username : ",radius_log["username"]," AD Group : ",str(groups)," Date : ",date)


scheduler = BlockingScheduler()
scheduler.add_job(collect, 'interval', minutes=1)
scheduler.start()
