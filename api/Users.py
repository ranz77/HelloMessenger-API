import json
import datetime
from api import Utils


def create_new_user(data, cursor):
    # get data input
    user_data = data['userInfo']
    user_id = Utils.get_id_for_access_token(data['accessToken'])

    # Add user to SQL database
    sql_querry = "INSERT INTO User values ('{0}', {1}, {2}, {3}, '{4}', '{5}', '{6}')"\
        .format(user_id, user_data['name'], user_data['birthDay'], user_data['birthMonth'],
                user_data['birthYear'], user_data['location'], user_data['picture'], user_data['bio'])
    cursor.execute(sql_querry)

    # Return json
    response = {
        'success': True
    }
    return json.dumps(response)


def update_user(data, cursor):
    # get data input
    user_data = data['userInfo']
    user_id = Utils.get_id_for_access_token(data['accessToken'])

    # Update user in SQL database
    sql_querry = '''UPDATE table
                    SET name='{0}', location='{1}', picture='{2}', bio='{3}'
                    WHERE userId = '{4}' '''\
        .format(user_data['name'], user_data['location'], user_data['picture'], user_data['bio'], user_id)
    cursor.execute(sql_querry)

    # Return json
    response = {
        'success': True
    }
    return json.dumps(response)


def delete_user(data, cursor):
    user_id = Utils.get_id_for_access_token(data['accessToken'])

    # Remove user from SQL database
    sql_querry = '''
    DELETE FROM User
    WHERE userId = '{0}'
    '''.format(user_id)
    cursor.execute(sql_querry)

    # Return json
    response = {
        'success': True
    }
    return json.dumps(response)


def get_my_user(data, cursor):
    user_id = Utils.get_id_for_access_token(data['accessToken'])
    return get_user_for_id(user_id, data, cursor)


def get_user_for_id(user_id, data, cursor):
    # Remove user from SQL database
    sql_querry = '''
        SELECT name, birthDay, birthMonth, birthYear, location, picture, bio
        FROM User
        WHERE userId = '{0}'
        '''.format(user_id)
    cursor.execute(sql_querry)

    # Return json
    for (name, birthDay, birthMonth, birthYear, location, picture, bio) in cursor:
        now = datetime.datetime.now()
        if now.month > birthMonth:
            age = now.year - birthYear - 1
        elif now.month < birthMonth:
            age = now.year - birthYear
        elif now.day > birthDay:
            age = now.year - birthYear - 1
        else:
            age = now.year - birthYear
        return {
            'name': name,
            'age': age,
            'location': location,
            'picture': picture,
            'bio': bio
        }
    