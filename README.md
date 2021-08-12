# GVE_DevNet_ISE_RADIUS_LOG_DASHBOARD
prototype web app that displays the users that have authenticated to the ISE network and are grouped by Active Directory membership 

## Contacts
* Jorge Banegas

## Solution Components
* flask
* python
* Mongo DB
* Cisco ISE
* Active Directory integration with ISE
* Google Chrome Browser
* local user credentials for ISE instance

## Installation

In the CLI:
1.	Choose a folder, then create and activate a virtual environment for the project
    ```python
    #WINDOWS:
    py -3 -m venv [add name of virtual environment here] 
    source [add name of virtual environment here]/Scripts/activate
    #MAC:
    python3 -m venv [add name of virtual environment here] 
    source [add name of virtual environment here]/bin/activate
    ```

2. Access the created virtual enviroment folder
    ```python
    cd [add name of virtual environment here] 
    ```

3.	Clone this Github repository into the virtual environment folder.
    ```python
    git clone [add github link here]
    ```
    For Github link: 
        In Github, click on the **Clone or download** button in the upper part of the page > click the **copy icon**

4. Access the root folder of the project
5. Open up Google Chrome, and vist the login page for ISE while having the inspect tool open in the Network tab
    ![/static/images/ise_login.png](/images/ise_login.png)
7. Expand the LoginAction.do 
8. Copy the source text of the Request Header and paste it in between """ """ in line 61 in  the populate.py file
    ![/static/images/payload.png](/images/ui_auth.png)
10. Copy the source text of the Form Data and paste it in between the quotes on the line payload = create_json("""""") in  the populate.py file
     ![/static/images/ui_auth.png](/images/payload.png)
12. Vist the Operations tab -> Live logs while have the inspect tool open in the  Network tab
13. Expand authLiveLog 
14. Copy the source text of the Request Header and paste it in between """ """ in line 61 in  the populate.py file
    ![/static/images/ui_auth.png](/images/live_log_payload.png)
16. Open up the config.py file and enter ISE environment info and the two AD groups to track
 ```python
    hostname =""
    username = ""
    password = ""
    student_group = ""
    faculty_group = ""
  ```
14.	Install dependencies
    ```python
    pip install -r requirements.txt
    ```
 15. You can chance the ip address if needed 
 
   ![/images/ip.png](/images/ip.png)
    
 18. Now you can launch the web application
```python
    python app.py
  ```
### Screenshots

![/images/screenshot.png](/images/screenshot.png)

### LICENSE

Provided under Cisco Sample Code License, for details see [LICENSE](LICENSE.md)

### CODE_OF_CONDUCT

Our code of conduct is available [here](CODE_OF_CONDUCT.md)

### CONTRIBUTING

See our contributing guidelines [here](CONTRIBUTING.md)

#### DISCLAIMER:
<b>Please note:</b> This script is meant for demo purposes only. All tools/ scripts in this repo are released for use "AS IS" without any warranties of any kind, including, but not limited to their installation, use, or performance. Any use of these scripts and tools is at your own risk. There is no guarantee that they have been through thorough testing in a comparable environment and we are not responsible for any damage or data loss incurred with their use.
You are responsible for reviewing and testing any scripts you run thoroughly before use in any non-testing environment.
