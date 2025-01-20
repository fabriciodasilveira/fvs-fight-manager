# requirements.txt
flask==2.0.1
flask-sqlalchemy==2.5.1
flask-login==0.5.0
python-dotenv==0.19.0
werkzeug==2.0.1

# app.py
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sua_chave_secreta_aqui'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///academia.db'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Modelos
class Usuario(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    tipo = db.Column(db.String(20), nullable=False)  # 'admin', 'professor', 'aluno'

class Aluno(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    cpf = db.Column(db.String(11), unique=True, nullable=False)
    data_nascimento = db.Column(db.Date, nullable=False)
    telefone = db.Column(db.String(20))
    email = db.Column(db.String(120))
    modalidades = db.relationship('Modalidade', secondary='aluno_modalidade')

class Professor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    cpf = db.Column(db.String(11), unique=True, nullable=False)
    especialidade = db.Column(db.String(50), nullable=False)
    telefone = db.Column(db.String(20))
    email = db.Column(db.String(120))

class ContaPagar(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.String(200), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    data_vencimento = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), default='pendente')  # 'pendente', 'pago'

class Mensalidade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    aluno_id = db.Column(db.Integer, db.ForeignKey('aluno.id'), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    mes_referencia = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), default='pendente')  # 'pendente', 'pago'
    data_pagamento = db.Column(db.Date)

class Modalidade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    descricao = db.Column(db.Text)
    valor_mensal = db.Column(db.Float, nullable=False)

# Tabela de associação entre alunos e modalidades
aluno_modalidade = db.Table('aluno_modalidade',
    db.Column('aluno_id', db.Integer, db.ForeignKey('aluno.id'), primary_key=True),
    db.Column('modalidade_id', db.Integer, db.ForeignKey('modalidade.id'), primary_key=True)
)

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

# Rotas
@app.route('/')
@login_required
def index():
    return render_template('index.html')

# Rotas para Alunos
@app.route('/alunos')
@login_required
def listar_alunos():
    alunos = Aluno.query.all()
    return render_template('alunos/listar.html', alunos=alunos)

@app.route('/alunos/novo', methods=['GET', 'POST'])
@login_required
def novo_aluno():
    if request.method == 'POST':
        aluno = Aluno(
            nome=request.form['nome'],
            cpf=request.form['cpf'],
            data_nascimento=datetime.strptime(request.form['data_nascimento'], '%Y-%m-%d'),
            telefone=request.form['telefone'],
            email=request.form['email']
        )
        db.session.add(aluno)
        db.session.commit()
        flash('Aluno cadastrado com sucesso!')
        return redirect(url_for('listar_alunos'))
    return render_template('alunos/novo.html')

# Rotas para Professores
@app.route('/professores')
@login_required
def listar_professores():
    professores = Professor.query.all()
    return render_template('professores/listar.html', professores=professores)

@app.route('/professores/novo', methods=['GET', 'POST'])
@login_required
def novo_professor():
    if request.method == 'POST':
        professor = Professor(
            nome=request.form['nome'],
            cpf=request.form['cpf'],
            especialidade=request.form['especialidade'],
            telefone=request.form['telefone'],
            email=request.form['email']
        )
        db.session.add(professor)
        db.session.commit()
        flash('Professor cadastrado com sucesso!')
        return redirect(url_for('listar_professores'))
    return render_template('professores/novo.html')

# Rotas para Contas a Pagar
@app.route('/contas')
@login_required
def listar_contas():
    contas = ContaPagar.query.all()
    return render_template('contas/listar.html', contas=contas)

@app.route('/contas/nova', methods=['GET', 'POST'])
@login_required
def nova_conta():
    if request.method == 'POST':
        conta = ContaPagar(
            descricao=request.form['descricao'],
            valor=float(request.form['valor']),
            data_vencimento=datetime.strptime(request.form['data_vencimento'], '%Y-%m-%d')
        )
        db.session.add(conta)
        db.session.commit()
        flash('Conta cadastrada com sucesso!')
        return redirect(url_for('listar_contas'))
    return render_template('contas/nova.html')

# Rotas para Mensalidades
@app.route('/mensalidades')
@login_required
def listar_mensalidades():
    mensalidades = Mensalidade.query.all()
    return render_template('mensalidades/listar.html', mensalidades=mensalidades)

@app.route('/mensalidades/nova', methods=['GET', 'POST'])
@login_required
def nova_mensalidade():
    if request.method == 'POST':
        mensalidade = Mensalidade(
            aluno_id=request.form['aluno_id'],
            valor=float(request.form['valor']),
            mes_referencia=datetime.strptime(request.form['mes_referencia'], '%Y-%m')
        )
        db.session.add(mensalidade)
        db.session.commit()
        flash('Mensalidade cadastrada com sucesso!')
        return redirect(url_for('listar_mensalidades'))
    alunos = Aluno.query.all()
    return render_template('mensalidades/nova.html', alunos=alunos)

# Rotas para Modalidades
@app.route('/modalidades')
@login_required
def listar_modalidades():
    modalidades = Modalidade.query.all()
    return render_template('modalidades/listar.html', modalidades=modalidades)

@app.route('/modalidades/nova', methods=['GET', 'POST'])
@login_required
def nova_modalidade():
    if request.method == 'POST':
        modalidade = Modalidade(
            nome=request.form['nome'],
            descricao=request.form['descricao'],
            valor_mensal=float(request.form['valor_mensal'])
        )
        db.session.add(modalidade)
        db.session.commit()
        flash('Modalidade cadastrada com sucesso!')
        return redirect(url_for('listar_modalidades'))
    return render_template('modalidades/nova.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5050)