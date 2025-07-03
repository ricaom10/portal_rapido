from flask import Flask, render_template, request, redirect, url_for, flash, make_response, session
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user
from users import get_user, create_user

app = Flask(__name__)
app.secret_key = 'chave_super_secreta'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class Usuario(UserMixin):
    def __init__(self, nome):
        self.id = nome

@login_manager.user_loader
def load_user(nome):
    if get_user(nome):
        return Usuario(nome)
    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        senha = request.form['senha']
        create_user(nome, senha)
        flash('Cadastro realizado com sucesso!')
        return redirect(url_for('login'))
    return render_template('cadastro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nome = request.form['nome']
        senha = request.form['senha']
        if get_user(nome) == senha:
            user = Usuario(nome)
            login_user(user)
            session['nome'] = nome
            resp = make_response(redirect(url_for('painel')))
            resp.set_cookie('nome', nome, max_age=120)
            return resp
        else:
            flash('Nome ou senha inválidos')
    return render_template('login.html')

@app.route('/painel')
@login_required
def painel():
    nome_cookie = request.cookies.get('nome', 'Visitante')
    return render_template('painel.html', nome=nome_cookie)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
