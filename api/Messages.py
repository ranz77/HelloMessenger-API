import json

from api import Utils


def get_conversation_messages(conversation_id, upper_bound_index, lower_bound_index, cursor):
    # Get SQL info
    cursor.execute("SELECT index, type, data, sender, timestamp FROM MESSAGES WHERE conversation_id ="
                   + conversation_id + " AND index >= " + lower_bound_index + " AND index <= " + upper_bound_index
                   + " ORDER BY index DESC")

    # Assemble returned json dictionary
    array = []
    for (index, type, data, sender, timestamp) in cursor:
        array.append({
            'index': index,
            'type': type,
            'data': data,
            'sender': sender,
            'timestamp': timestamp
        })

    # Update message read
    cursor.execute("SELECT TOP 1 index FROM MESSAGES WHERE conversation_id ="
                   + conversation_id + " AND index >= " + lower_bound_index + " AND index <= " + upper_bound_index
                   + " ORDER BY index DESC")
    my_data = cursor.fetchone
    if my_data is not None and my_data >= lower_bound_index <= upper_bound_index:
        cursor.execute("UPDATE MESSAGES SET seen_by_reciever = 1 WHERE conversation_id = " + conversation_id)

    return json.dump({
        'messages': array
    })


def get_conversation_messages_at_bottom(conversation_id, data, cursor):
    # Determine bounds
    lower_bound_index = data['lowerBoundIndex'] + 1
    upper_bound_index = lower_bound_index + 99

    return get_conversation_messages(conversation_id, upper_bound_index, lower_bound_index, cursor)


def get_conversation_messages_at_top(conversation_id, data, cursor):
    # Determine bounds
    upper_bound_index = data['upperBoundIndex'] - 1
    lower_bound_index = upper_bound_index - 99

    return get_conversation_messages(conversation_id, upper_bound_index, lower_bound_index, cursor)


def post_new_conversation_message(conversation_id, data, cursor):
    # Prep
    user_id = Utils.get_id_for_access_token(data['accessToken'])
    cursor.execute(
        "SELECT TOP 1 index FROM MESSAGES WHERE conversation_id = " + conversation_id + ' ORDER BY index DESC')
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
    type = data['type']
    dataa = data['data']
    seen_by_reciever = 0

    # Send to sql database
    cursor.execute("INSERT INTO MESSAGES VALUES ('{0}', '{1}', {2}, '{3}', '{4}', '{5}', {6}, '{7}')").format(
        message_id, conversation_id, index, type, dataa, sender, timestamp, seen_by_reciever
    )
    return json.dump({
        'success': True
    })
