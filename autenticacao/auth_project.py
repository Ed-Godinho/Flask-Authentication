from flask import Blueprint, render_template

auth_blueprint = Blueprint('auth',__name__, template_folder='templates', static_folder='static', static_url_path='/autenticacao/static')

@auth_blueprint.route('/')
def auth_project():
    return render_template('index.html')

