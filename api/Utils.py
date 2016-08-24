import json
import requests
import time


def get_id_for_access_token(access_token):
    url = 'https://graph.accountkit.com/v1.0/me/?access_token=' + access_token
    response = requests.get(url).text
    response_json = json.loads(response)
    return response_json['id']


def current_milli_time():
    return int(round(time.time() * 1000))
