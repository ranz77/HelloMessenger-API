import json, requests


def verify_auth_code(authcode, cursor):
    # Ping account kit
    url = 'https://graph.accountkit.com/v1.0/access_token?grant_type=authorization_code&code=' + authcode + '&access_token=AA|' + 'id' + '|' + 'app_secret'
    facebook_response = requests.get(url).text
    facebook_json = json.loads(facebook_response)
    access_token = facebook_json['access_token']
    user_id = facebook_json['id']

    # determine if account already exists
    cursor.execute('SELECT userId FROM User WHERE userId = ' + user_id)

    # return json
    response = {
        'accountExists': cursor.fetchone() is None,
        'accessToken': access_token
    }
    return response
