from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from functools import wraps
import json, os
from datetime import timedelta, datetime, timezone

from passlib.hash import pbkdf2_sha256 as sha256

auth_blueprint = Blueprint('auth',__name__, template_folder='templates', static_folder='static', static_url_path='/autenticacao/static')


SECRET_KEY = "Assinatura do cookie"

#Decorator para proteger as rotas
def proteger_rota(cargos_permitidos):
    def decorator_proteger_rota(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if session.get('cargo') in cargos_permitidos or session.get('cargo') == 'admin':
                return f(*args, **kwargs)
            else:
                return redirect(url_for('auth.chat_index'))
        return decorated_function
    return decorator_proteger_rota


@auth_blueprint.route('/')
def auth_project():
    return render_template('index.html')

#------------- Funções para a rota de cadastro -----------------

#Função para ler os dados do arquivo json
def ler_dados_json():
    if os.path.exists('autenticacao\static\json\cadastros.json'):
        with open('autenticacao\static\json\cadastros.json', 'r') as arquivo:
            dados = json.load(arquivo)
        return dados
    else:
        return {}

#Função para verificar se o usuário ou email já existe
def verificar_existencia_usuario_email(username, email):
    dados = ler_dados_json()
    for id_, cadastro in dados.items():
        if 'username' in cadastro and cadastro['username'] == username:
            return True
        if 'email' in cadastro and cadastro['email'] == email:
            return True
    return False

#Função para adicionar o usuário no arquivo json
def adicionar_usuario(username, email, senha, cargo):
    dados = ler_dados_json()
    novo_id = str(len(dados) + 1)
    dados[novo_id] = {
        'username': username,
        'email': email,
        'senha': senha,
        'cargo': cargo
    }

    with open('autenticacao\static\json\cadastros.json', 'w') as arquivo:
        json.dump(dados, arquivo)


@auth_blueprint.route('/cadastro', methods=['POST'])
def cadastro():
    dados = request.get_json()
    dados['cargo'] = 'user'
    username = dados['username']
    email = dados['email']
    cargo = dados['cargo']
    

    if verificar_existencia_usuario_email(username, email):
        resposta = jsonify({'success': False, 'message': 'Usuário ou email já cadastrado'})
        return resposta
    
    senha = sha256.hash(dados['senha'])
    adicionar_usuario(dados['username'], dados['email'], senha, cargo)


    return jsonify({'success': True, 'Dados': dados})


#------------- Funções para a rota de login -----------------

#Decorator de sessão
def make_session_permanent():
    session.permanent = False
    auth_blueprint.permanent_session_lifetime = timedelta(minutes=60)

    # Check if the session has expired
    if 'login_time' in session and \
            datetime.now(timezone.utc) - session['login_time'] > auth_blueprint.permanent_session_lifetime:
        session.clear()  # Clear the session data
        return redirect(url_for('auth_project'))

    # Update the last activity time
    session['last_activity'] = datetime.now(timezone.utc)

auth_blueprint.permanent_session_lifetime = timedelta(minutes=60)


def verificar_login(username, senha):
    with open('autenticacao\static\json\cadastros.json', 'r') as arquivo:
        dados = json.load(arquivo)
        for id_, cadastro in dados.items():
            if username == cadastro['username'] and sha256.verify(senha, cadastro['senha']):
                resposta = 'Usuário autenticado'
                dados = cadastro
                break
            else:
                resposta = 'Usuário ou senha incorretos'
    return resposta, cadastro


@auth_blueprint.route('/login', methods=['POST', 'GET'])
def login():
    dados = request.get_json()
    username = dados['username']
    senha = dados['senha']

    if verificar_login(username, senha)[0] == 'Usuário autenticado':
        session['username'] = username
        session['cargo'] = verificar_login(username, senha)[1]['cargo']
        print('Usuário autenticado')
        return jsonify({'success': True, 'message': 'Usuário autenticado'})
    else:
        print('Usuário ou senha incorretos')
        return jsonify({'success': False, 'message': 'Usuário ou senha incorretos'})


@auth_blueprint.route('/chat_index')
@proteger_rota(['user', 'admin'])
def chat_index():
    usuario_autenticado = session.get('username')
    if usuario_autenticado != None:
        return render_template('index_chat.html', usuario = usuario_autenticado)

@auth_blueprint.route('/chat')
@proteger_rota(['user', 'admin'])
def chat():
    usuario_autenticado = session.get('username')
    return render_template('chat.html', usuario = usuario_autenticado)

@auth_blueprint.route('/admin')
@proteger_rota(['admin'])
def painel_adm():
    usuario_autenticado = session.get('username')
    cargo = session.get('cargo')

    return render_template('painel.html', usuario = usuario_autenticado)


@auth_blueprint.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('cargo', None)
    return redirect(url_for('auth.auth_project'))
