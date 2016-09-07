from api import Users
from api import Utils
import json


def list_conversations(access_token, cursor):
    user_id = Utils.get_id_for_access_token(access_token)
    cursor.execute("SELECT second_user_id, conversation_id FROM CONVERSATIONS WHERE first_user_id = " + user_id)
    array = []
    list_of_conversations = list(cursor)
    for (other_user_id, conversation_id) in list_of_conversations:
        cursor.execute("SELECT TOP 1 type, data, seen_by_reciever, sender FROM MESSAGES WHERE conversation_id = " + conversation_id)
        for (type, data, seen_by_reciever, sender) in cursor:
            if type == 'media':
                new_message = "Sent a picture."
            else:
                new_message = data
            array.append({
                'userInfo': Users.get_user_for_id(other_user_id, cursor),
                'lastMessage': new_message,
                'newMessage': seen_by_reciever,
                'conversationId': conversation_id
            })
    return json.dumps({'conversations':array})


def leave_conversation(conversation_id, data, cursor):
    user_id = Utils.get_id_for_access_token(data['accessToken'])
    cursor.execute("DELETE FROM CONVERSATIONS WHERE first_user_id = " + user_id + " AND second_user_id = " + conversation_id)
    return json.dump({
        'success': True
    })


def send_friend_request(conversation_id, data, cursor):
    # Prep
    user_id = Utils.get_id_for_access_token(data['accessToken'])
    cursor.execute("SELECT perm FROM MESSAGES WHERE conversation_id = " + conversation_id + "AND type = " + "friend")
    is_accepter = cursor.fetchone() is not None
    cursor.execute(
        "SELECT TOP 1 index FROM MESSAGES WHERE conversation_id = " + conversation_id)
    content = cursor.fetchone()

    # Determine params
    sender = user_id
    conversation_id = conversation_id
    if content is None:
        index = 0
    else:
        index = content + 1
    message_id = conversation_id + '---' + index
    timestamp = Utils.current_milli_time()
    type = "friend"
    if is_accepter:
        data = "accept"
    else:
        data = "send"
    seen_by_reciever = 0

    # Send to sql database
    cursor.execute("INSERT INTO MESSAGES VALUES ('{0}', '{1}', {2}, '{3}', '{4}', '{5}', {6}, '{7}')").format(
        message_id, conversation_id, index, type, data, sender, timestamp, seen_by_reciever
    )
    return json.dump({
        'success': True
    })
