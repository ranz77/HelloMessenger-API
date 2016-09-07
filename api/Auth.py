import json
import requests

from Secure import facebook_app_secret, facebook_app_id


def verify_auth_code(authcode, cursor):
    # Ping account kit
    url = 'https://graph.accountkit.com/v1.0/access_token?grant_type=authorization_code&code=' + authcode + '&access_token=AA|' + facebook_app_id + '|' + facebook_app_secret
    facebook_response = requests.get(url).text
    facebook_json = json.loads(facebook_response)
    print facebook_json
    access_token = facebook_json['access_token']
    user_id = facebook_json['id']

    # determine if account already exists
    sql_querry = 'SELECT userId FROM USER WHERE userId = ' + user_id
    print '*****' + sql_querry
    cursor.execute(sql_querry)

    # return json
    response = {
        'accountExists': cursor.fetchone() is not None,
        'accessToken': access_token
    }
    return json.dumps(response)
