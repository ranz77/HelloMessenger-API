#!/usr/bin/python
from flask import Flask, request
import DatabaseTest
import GeneralDatabase
import MySQLdb
import Secure

from api import Auth, Users, Conversations, Messages, Matching

app = Flask(__name__)
db = MySQLdb.connect(Secure.host, Secure.user, Secure.password, Secure.database, autocommit=1)


def get_database_cursor():
    cursor = db.cursor()
    return cursor


@app.route('/testdatabase')
def test():
    return DatabaseTest.test_database(get_database_cursor())


@app.route('/testadd')
def testAdd():
    return DatabaseTest.test_add(get_database_cursor())


@app.route('/testget')
def testGet():
    return DatabaseTest.test_get(get_database_cursor())


@app.route('/reset')
def reset():
    return GeneralDatabase.reset_database(get_database_cursor())


@app.route('/auth/access_token/<authcode>', methods=['GET'])
def auth_access_token(authcode):
    if request.method == 'GET':
        return Auth.verify_auth_code(authcode, get_database_cursor())
    else:
        return '404 not found'


@app.route('/user', methods=['POST', 'GET', 'PUT', 'DELETE'])
def users():
    data = request.get_json()
    if request.method == 'POST':
        return Users.create_new_user(data, get_database_cursor())
    elif request.method == 'GET':
        return Users.get_my_user(data, get_database_cursor())
    elif request.method == 'PUT':
        return Users.update_user(data, get_database_cursor())
    elif request.method == 'DELETE':
        return Users.delete_user(data, get_database_cursor())
    else:
        return "404 not found"


@app.route('/user/<id>', methods=['GET'])
def user(id):
    data = request.get_json()
    if request.method == 'GET':
        return Users.get_user_json_for_id(id, get_database_cursor())
    else:
        return "404 not found"


@app.route('/conversations/list', methods=['GET'])
def conversations_list():
    data = request.get_json()
    if request.method == 'GET':
        return Conversations.list_conversations(data, get_database_cursor())
    else:
        return "404 not found"


@app.route('/conversations/request', methods=['POST', 'GET', 'DELETE'])
def conversations_request():
    data = request.get_json()
    if request.method == 'POST':
        return Matching.new_request(data, get_database_cursor())
    elif request.method == 'GET':
        return Matching.get_update_on_request(data, get_database_cursor())
    elif request.method == 'DELETE':
        return Matching.end_request(data, get_database_cursor())
    else:
        return "404 not found"


@app.route('/conversations/top_messages/<id>', methods=['GET'])
def conversations_messages_top(id):
    data = request.get_json()
    if request.method == 'GET':
        return Messages.get_conversation_messages(id, data, get_database_cursor())
    else:
        return '404 not found'


@app.route('/conversations/bottom_messages/<id>', methods=['POST', 'GET'])
def conversations_messages_bottem(id):
    data = request.get_json()
    if request.method == 'POST':
        return Messages.post_new_conversation_message(id, data, get_database_cursor())
    elif request.method == 'GET':
        return Messages.get_conversation_messages(id, data, get_database_cursor())
    else:
        return '404 not found'


@app.route('/conversations/leave/<id>', methods=['DELETE'])
def conversations_messages(id):
    data = request.get_json()
    if request.method == 'DELETE':
        return Conversations.leave_conversation(id, data, get_database_cursor())
    else:
        return '404 not found'


@app.route('/conversations/friend_request/<id>', methods=['POST'])
def conversations_friend_request(id):
    data = request.get_json()
    if request.method == 'POST':
        return Conversations.send_friend_request(id, data, get_database_cursor())
    else:
        return '404 not found'


if __name__ == '__main__':
    app.run(host='0.0.0.0')
