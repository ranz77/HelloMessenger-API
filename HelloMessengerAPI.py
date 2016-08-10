from flask import Flask

import Auth

app = Flask(__name__)


@app.route('/auth/<authcode>')
def hello_world(authcode):
    return Auth.verifyAuthCode(authcode);


if __name__ == '__main__':
    app.run()
