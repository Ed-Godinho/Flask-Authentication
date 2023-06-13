from flask import Blueprint, render_template, request, jsonify
import json, os

from passlib.hash import pbkdf2_sha256 as sha256

auth_blueprint = Blueprint('auth',__name__, template_folder='templates', static_folder='static', static_url_path='/autenticacao/static')

@auth_blueprint.route('/')
def auth_project():
    return render_template('index.html')


def ler_dados_json():
    if os.path.exists('autenticacao\static\json\cadastros.json'):
        with open('autenticacao\static\json\cadastros.json', 'r') as arquivo:
            dados = json.load(arquivo)
        return dados
    else:
        return {}


def verificar_existencia_usuario_email(username, email):
    dados = ler_dados_json()
    for id_, cadastro in dados.items():
        if 'username' in cadastro and cadastro['username'] == username:
            return True
        if 'email' in cadastro and cadastro['email'] == email:
            return True
    return False


def adicionar_usuario(username, email, senha):
    dados = ler_dados_json()
    novo_id = str(len(dados) + 1)
    dados[novo_id] = {
        'username': username,
        'email': email,
        'senha': senha
    }
    with open('autenticacao\static\json\cadastros.json', 'w') as arquivo:
        json.dump(dados, arquivo)



@auth_blueprint.route('/cadastro', methods=['POST'])
def cadastro():
    dados = request.get_json()
    username = dados['username']
    email = dados['email']

    if verificar_existencia_usuario_email(username, email):
        resposta = jsonify({'success': False, 'message': 'Usuário ou email já cadastrado'})
        return resposta
    
    senha = sha256.hash(dados['senha'])
    adicionar_usuario(dados['username'], dados['email'], senha)


    return jsonify({'success': True, 'Dados': dados})
