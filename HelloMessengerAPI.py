#!/usr/bin/python
from django.core.serializers import python
from flask import Flask
import Auth, DatabaseTest, MySQLdb
import GeneralDatabase
import Secure

app = Flask(__name__)
db = MySQLdb.connect(Secure.host, Secure.database, Secure.password, Secure.user)

def getDatabaseCursor():
    cursor = db.cursor()
    return cursor

@app.route('/testdatabase')
def test():
    return DatabaseTest.test_database(getDatabaseCursor())

@app.route('/testadd')
def testAdd():
    return DatabaseTest.test_add(getDatabaseCursor())

@app.route('/testget')
def testGet():
    return DatabaseTest.test_get(getDatabaseCursor())

@app.route('/auth/<authcode>')
def hello_world(authcode):
    return Auth.verify_auth_code(authcode, getDatabaseCursor());

@app.route('/reset')
def reset():
    return GeneralDatabase.reset_database(getDatabaseCursor())

if __name__ == '__main__':
    app.run(host='0.0.0.0')