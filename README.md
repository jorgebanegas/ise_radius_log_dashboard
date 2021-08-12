# GVE_DevNet_app_template
prototype web app that displays the users that have authenticated to the ISE network and are grouped by Active Directory membership 

## Contacts
* Jorge Banegas

## Solution Components
* flask
* python
* HTML
* Javascript
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
        ![/static/images/giturl.png](/static/images/giturl.png)

4. Access the folder **GVE_DevNet_app_template**
    ```python
    cd GVE_DevNet_app_template
    ```

5.	Install dependencies
    ```python
    pip install -r requirements.txt
    ```
### LICENSE

Provided under Cisco Sample Code License, for details see [LICENSE](LICENSE.md)

### CODE_OF_CONDUCT

Our code of conduct is available [here](CODE_OF_CONDUCT.md)

### CONTRIBUTING

See our contributing guidelines [here](CONTRIBUTING.md)

#### DISCLAIMER:
<b>Please note:</b> This script is meant for demo purposes only. All tools/ scripts in this repo are released for use "AS IS" without any warranties of any kind, including, but not limited to their installation, use, or performance. Any use of these scripts and tools is at your own risk. There is no guarantee that they have been through thorough testing in a comparable environment and we are not responsible for any damage or data loss incurred with their use.
You are responsible for reviewing and testing any scripts you run thoroughly before use in any non-testing environment.
