import requests
from requests.auth import HTTPBasicAuth
import config
import json
import pprint
import datetime

def getSessions():
    url = "https://" + config.hostname + ":8910/pxgrid/mnt/sd/getSessions"

    time_5mins = datetime.datetime.now() - datetime.timedelta(minutes=5)

    data= {"startTimestamp": time_5mins.isoformat()}
    headers = {
    'Accept-Language': 'application/json',
    'Content-Type': 'application/json',
    }

    response = requests.request("POST", url, headers=headers,  data=json.dumps(data),auth = HTTPBasicAuth(config.pxgrid_user, config.pxgrid_secret))

    return response.json()

response = getSessions()
pprint.pprint(response)



