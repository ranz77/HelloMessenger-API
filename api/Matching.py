from api import Users
from api import Utils
from api import pending_requests
import json


def has_not_been_matched(user_id_one, user_id_two, cursor):
    sql_querry = "SELECT first_user_id from PREVIOUS_MATCHES WHERE first_user_id = '{0}' AND user_id_two = '{1}'"\
        .format(user_id_one, user_id_two)
    cursor.execute(sql_querry)
    return cursor.fetchone() is None


def finish_request(request, user_id, cursor):
    # Get user ids ready
    user_id_one = request['id']
    user_id_two = user_id

    # Record that these users have been matched before
    sql_querry = "INSERT INTO PREVIOUS_MATCHES values ('{0}', '{1}')".format(user_id_one, user_id_two)
    cursor.execute(sql_querry)
    sql_querry = "INSERT INTO PREVIOUS_MATCHES values ('{0}', '{1}')".format(user_id_two, user_id_one)
    cursor.execute(sql_querry)

    # Make new conversations
    conversation_id = user_id_one + "---" + user_id_two
    sql_querry = "INSERT INTO CONVERSATIONS values ('{0}', '{1}', '{2}', 0)".format(conversation_id, user_id_one, user_id_two)
    cursor.execute(sql_querry)
    sql_querry = "INSERT INTO CONVERSATIONS values ('{0}', '{1}', '{2}', 0)".format(conversation_id, user_id_two, user_id_one)
    cursor.execute(sql_querry)

    # Complete request data
    request["status"] = "matched"
    request["matchedUserId"] = user_id
    request["matchedUserInfo"] = Users.get_user_for_id(user_id, cursor)

    current_user_request = {
        "id": user_id,
        "status": "matched",
        "matchedUserId": request["id"],
        "matchedUserInfo": Users.get_user_for_id(request["id"], cursor)
    }
    pending_requests.append(current_user_request)


def new_request(data, cursor):
    user_id = Utils.get_id_for_access_token(data['accessToken'])
    for request in pending_requests:
        if user_id != request['id'] and request['status'] == 'pending' and has_not_been_matched(user_id, request[id], cursor):
            finish_request(request, user_id, cursor)
            return json.dump({
                "success": True
            })
    pending_requests.append({
        "id": user_id,
        "status": "pending"
    })
    return json.dump({
        "success": True
    })


def get_update_on_request(token, cursor):
    user_id = Utils.get_id_for_access_token(token)
    for request in pending_requests:
        if user_id is request['id']:
            request_copy = request.copy()
            del request_copy['id']
            return json.dump(request_copy)
    return json.dump({
        "status": "nonactive"
    })


def end_request(token, cursor):
    user_id = Utils.get_id_for_access_token(token)
    for request in pending_requests:
        if user_id is request['id']:
            pending_requests.remove(request)
            return json.dump({
                "success": True
            })
