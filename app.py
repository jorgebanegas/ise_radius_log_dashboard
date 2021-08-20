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

# Import Section
from flask import Flask, render_template, request, url_for, redirect,jsonify
from collections import defaultdict
import datetime
import requests
import json
from dotenv import load_dotenv
import os
from collections import Counter
from pymongo import MongoClient
import config

# load all environment variables
load_dotenv()


# Global variables
app = Flask(__name__)

client = MongoClient()
db = client['logs']
collection = db['radius_logs']

def unique(list1):
    temp = []
    # insert the list to the set
    list_set = set(list1)

    # convert the set to the list
    unique_list = (list(list_set))

    for x in unique_list:
        temp.append(x)

    return temp

@app.route('/ise',methods=['GET', 'POST'])
def ise():
        if request.method == 'POST':
            temp = []
            list_of_dates = []
            payload = {"count":[0,0],"student_data":[],"faculty_data":[],"data":[]}
            start = request.form.get("start")
            end = request.form.get("end")
            print(start)
            print(end)

            start = datetime.datetime.strptime(start, "%Y-%m-%d").strftime("%Y-%d-%m")
            end = datetime.datetime.strptime(end, "%Y-%m-%d").strftime("%Y-%d-%m")
            
            if start == end:
                myquery = { "date": str(start) }
                mydoc = collection.find(myquery)
            else:
                myquery = {'date':{'$gte':start,'$lte':end}}
                mydoc = collection.find(myquery)

            for entry in mydoc:
                temp.append(entry)

            print(temp)
            
            temp.sort(key = lambda x:x['time'])
            for i in temp:
                list_of_dates.append(i["date"])

            unique_dates = unique(list_of_dates)
            counter = list(Counter(list_of_dates).items())

            for i in temp:
                time = i["time"]
                temp2 = {}
                temp2["time"] = i['time']
                temp2["user"] = i['username']
                temp2["date"] = i['date']
           
                if config.faculty_sid in str(i['adgroup']):
                    temp2["ad"] = "Faculty"
                    payload["count"][1] += 1
                    date = datetime.datetime.strptime(i['date'], "%Y-%d-%m").strftime("%Y-%m-%d")
                    payload["faculty_data"].append(date)
                    payload['data'].append(temp2)


                if config.student_sid in str(i['adgroup']):
                    temp2["ad"] = "Student"
                    payload["count"][0] += 1
                    date = datetime.datetime.strptime(i['date'], "%Y-%d-%m").strftime("%Y-%m-%d")
                    payload["student_data"].append(date)
                    payload['data'].append(temp2)

                if config.faculty_sid in str(i['adgroup']) and config.student_sid in str(i['adgroup']):
                    temp2["ad"] = "Faculty/Student"
           
            payload["student_data"] = list(Counter(payload["student_data"]).items())
            payload["faculty_data"] = list(Counter(payload["faculty_data"]).items())
            list_students = []
            list_faculty = []

            for entry in payload["student_data"]:
                temp = {}
                temp['x'] = entry[0]
                temp['y'] = entry[1]
                list_students.append(temp)
            
            for entry in payload["faculty_data"]:
                temp = {}
                temp['x'] = entry[0]
                temp['y'] = entry[1]
                list_faculty.append(temp)

            payload["student_data"] = list_students
            payload["faculty_data"] = list_faculty

            #return as json to jquery request, which is then manipulated to show existing ssid schedules
            return  jsonify(payload)
        else:
            today = datetime.datetime.today()
            day = today.strftime("%m/%d/%Y")
            previous = datetime.datetime.today() - datetime.timedelta(days=2)
            previous_day = previous.strftime("%m/%d/%Y")
            date_range = str(day) + " - " + str(previous_day)
            return render_template('ise.html',date_range=date_range)

if __name__ == "__main__":
    app.run(host='127.0.0.1', debug=True)
    
