import json, requests


def verify_auth_code(authcode, cursor):
    url = 'https://graph.accountkit.com/v1.0/access_token?grant_type=authorization_code&code=' + authcode + '&access_token=AA|' + 'id' + '|' + 'app_secret'
    response = requests.get(url).text
    print response
    return response
