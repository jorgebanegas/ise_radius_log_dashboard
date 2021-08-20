from base64 import b64encode
import requests
import json
import config
import pprint

#Build the Headers for the API Calls to ISE
def build_headers():
    authencode = config.api_user+":"+config.api_password
    authencode = authencode.encode("ascii")
    userAndPass = b64encode(authencode).decode("ascii")
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": "Basic %s" % userAndPass
        }
    return headers

def get_active_directories():
    headers = build_headers()
    url = "https://" + config.hostname + ":9060/ers/config/activedirectory"

   
    response_raw = requests.request("GET", url,data="{}", headers=headers, verify=False)
    response = json.loads(response_raw.text.encode("utf8"))
    results = response["SearchResult"]["resources"]

    return results

def get_ad_groups(ad_id,username):

    headers = build_headers()

    url ="https://" + config.hostname + ":9060/ers/config/activedirectory/" + ad_id + "/getUserGroups"

    payload = {
            "OperationAdditionalData": {
                "additionalData":[{
                    "name":"username",
                    "value":username
                }]
            }
    }

    response = requests.request("PUT", url, data=json.dumps(payload), headers=headers, verify=False)
    response = json.loads(response.text.encode("utf8"))
    pprint.pprint(response)
    try:
        results = response["ERSActiveDirectoryGroups"]["groups"]
    except:
        print("Username: ",username, " cannot be found")
        return None
    return results