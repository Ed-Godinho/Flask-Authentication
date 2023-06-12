from flask import Flask, Blueprint
from autenticacao.auth_project import auth_blueprint

app = Flask(__name__)

app.register_blueprint(auth_blueprint)

if __name__ == '__main__':
    app.run(host='192.168.1.147', port=5000, debug=True)