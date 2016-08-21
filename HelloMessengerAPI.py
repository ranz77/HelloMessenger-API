#!/usr/bin/python
from django.core.serializers import python
from flask import Flask
import Auth, DatabaseTest, MySQLdb
import GeneralDatabase
import Secure

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


@app.route('/auth/accessToken/<authcode>', methods=['GET'])
def auth_access_token(authcode):
    return Auth.verify_auth_code(authcode, get_database_cursor());


@app.route('/user', methods=['POST', 'PUT', 'DELETE'])
def users():
    # TODO
    return


@app.route('/user/<id>', methods=['GET'])
def user(id):
    # TODO
    return


@app.route('/conversations/list', methods=['GET'])
def conversations_list():
    # TODO
    return


@app.route('/conversations/request', methods=['POST', 'GET', 'DELETE'])
def conversations_request():
    # TODO
    return


@app.route('/conversations/mesages/<id>', methods=['POST', 'GET'])
def conversations_messages(id):
    # TODO
    return


@app.route('/conversations/leave/<id>', methods=['DELETE'])
def conversations_messages(id):
    # TODO
    return


@app.route('/conversations/friend_request/<id>', methods=['POST'])
def conversations_friend_request(id):
    # TODO
    return


if __name__ == '__main__':
    app.run(host='0.0.0.0')
