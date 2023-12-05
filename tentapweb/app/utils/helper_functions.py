from flask import current_app

import requests

def getApiDetails(endpoint=""):
    API_KEY = current_app.config['TP_API_KEY'] 
    API_URL = current_app.config['TP_API'] + endpoint
    return API_URL, API_KEY

def fetchStartPageContent(section):
    API_LINK = current_app.config['TP_API'] + "startpage"
    API_KEY = current_app.config['TP_API_KEY']

    response = requests.get(API_LINK + "/" + section, headers={
        'X-API-Key': API_KEY
    })

    if response.status_code == 200:
        data = response.json()  # Parse the response JSON
        return data["content"]

    return ""