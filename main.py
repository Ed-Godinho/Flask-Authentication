from flask import Flask, Blueprint
from autenticacao.auth_project import auth_blueprint
from flask_socketio import SocketIO, emit, send

app = Flask(__name__)


SECRET_KEY = "Assinatura do cookie"
app.secret_key = SECRET_KEY

app.register_blueprint(auth_blueprint)

if __name__ == '__main__':
    app.run(host='192.168.1.147', port=5000, debug=True)