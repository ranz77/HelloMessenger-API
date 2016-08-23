import json
import requests


def get_id_for_access_token(access_token):
    url = 'https://graph.accountkit.com/v1.0/me/?access_token=' + access_token
    response = requests.get(url).text
    response_json = json.loads(response)
    return response_json['id']