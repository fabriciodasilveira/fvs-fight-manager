from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from models import db
from models.models import *
from routes.autenticacao import auth_bp
from routes.usuarios import usuarios_bp
from routes.alunos import alunos_bp
from routes.professores import professores_bp
from routes.modalidades import modalidades_bp
from routes.planos import planos_bp
from routes.matriculas import matriculas_bp
from routes.contas import contas_bp 


app = Flask(__name__)
app.config['SECRET_KEY'] = 'fabricio123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///academia.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

migrate = Migrate(app, db)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
csrf = CSRFProtect(app)


# Registrando Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(usuarios_bp)
app.register_blueprint(alunos_bp)
app.register_blueprint(professores_bp)
app.register_blueprint(modalidades_bp)
app.register_blueprint(planos_bp)
app.register_blueprint(matriculas_bp)
app.register_blueprint(contas_bp)  # <- Adicionado

# # Decorator para verificar permissões
# def requer_permissao(codigo_permissao):
#     def decorator(f):
#         @wraps(f)
#         def decorated_function(*args, **kwargs):
#             if not current_user.tem_permissao(codigo_permissao):
#                 flash('Você não tem permissão para acessar esta área. Procure o Administrador para solicitar !', 'error')
#                 return redirect(url_for('index'))
#             return f(*args, **kwargs)
#         return decorated_function
#     return decorator

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

# Rota Principal
@app.route('/')
@login_required
def index():
    return render_template('index.html')

# # Rotas para Usuários
# @app.route('/usuarios/editar/<int:id>', methods=['GET', 'POST'])
# @login_required
# @requer_permissao('admin')
# def editar_usuario(id):
#     usuario = Usuario.query.get_or_404(id)
#     if request.method == 'POST':
#         usuario.username = request.form['username']
#         usuario.nome_completo = request.form['nome_completo']
#         usuario.email = request.form['email']
        
#         # Atualiza as permissões
#         permissoes_selecionadas = request.form.getlist('permissoes')
#         permissoes = Permissao.query.filter(Permissao.codigo.in_(permissoes_selecionadas)).all()
#         usuario.permissoes = permissoes
        
#         db.session.commit()
#         flash('Usuário atualizado com sucesso!', 'success')
#         return redirect(url_for('listar_usuarios'))
    
#     permissoes = Permissao.query.all()
#     return render_template('usuarios/novo.html', usuario=usuario, permissoes=permissoes)

# @app.route('/usuarios/excluir/<int:id>', methods=['POST'])
# @login_required
# @requer_permissao('admin')
# def excluir_usuario(id):
#     usuario = Usuario.query.get_or_404(id)
#     if usuario.tipo == 'admin':
#         flash('Não é possível excluir um usuário admin.', 'error')
#     else:
#         db.session.delete(usuario)
#         db.session.commit()
#         flash('Usuário excluído com sucesso!', 'success')
#     return redirect(url_for('listar_usuarios'))

# # Rotas de Autenticação
# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         user = Usuario.query.filter_by(username=username).first()
        
#         if user and check_password_hash(user.password, password):
#             login_user(user)
#             flash('Login realizado com sucesso!')
#             return redirect(url_for('index'))
#         else:
#             flash('Usuário ou senha inválidos.')
    
#     return render_template('login.html')

# @app.route('/logout')
# @login_required
# def logout():
#     logout_user()
#     flash('Logout realizado com sucesso!')
#     return redirect(url_for('login'))



# # Rotas para Usuários
# @app.route('/usuarios')
# @login_required
# @requer_permissao('admin')
# def listar_usuarios():
#     usuarios = Usuario.query.all()
#     return render_template('usuarios/listar.html', usuarios=usuarios)

# @app.route('/usuarios/novo', methods=['GET', 'POST'])
# @login_required
# @requer_permissao('admin')
# def novo_usuario():
#     if request.method == 'POST':
#         permissoes_selecionadas = request.form.getlist('permissoes')
        
#         novo_usuario = Usuario(
#             username=request.form['username'],
#             password=generate_password_hash(request.form['password']),
#             tipo='usuario',
#             nome_completo=request.form['nome_completo'],
#             email=request.form['email']
#         )
        
#         permissoes = Permissao.query.filter(Permissao.codigo.in_(permissoes_selecionadas)).all()
#         novo_usuario.permissoes = permissoes
        
#         db.session.add(novo_usuario)
#         db.session.commit()
#         flash('Usuário cadastrado com sucesso!')
#         return redirect(url_for('listar_usuarios'))
    
#     permissoes = Permissao.query.all()
#     return render_template('usuarios/novo.html', permissoes=permissoes)

# # Rotas para Alunos
# @app.route('/alunos')
# @login_required
# @requer_permissao('alunos')
# def listar_alunos():
#     alunos = Aluno.query.all()
#     return render_template('alunos/listar.html', alunos=alunos)

# @app.route('/alunos/novo', methods=['GET', 'POST'])
# @login_required
# @requer_permissao('alunos')
# def novo_aluno():
#     if request.method == 'POST':
#         aluno = Aluno(
#             nome=request.form['nome'],
#             cpf=request.form['cpf'],
#             data_nascimento=datetime.strptime(request.form['data_nascimento'], '%Y-%m-%d'),
#             telefone=request.form['telefone'],
#             email=request.form['email']
#         )
#         db.session.add(aluno)
#         db.session.commit()
#         flash('Aluno cadastrado com sucesso!', 'success')
#         return redirect(url_for('listar_alunos'))
#     return render_template('alunos/novo.html')

# @app.route('/alunos/editar/<int:id>', methods=['GET'])
# @login_required
# @requer_permissao('alunos')
# def editar_aluno(id):
#     aluno = Aluno.query.get_or_404(id)
#     return render_template('alunos/novo.html', aluno=aluno)

# @app.route('/alunos/atualizar/<int:id>', methods=['POST'])
# @login_required
# @requer_permissao('alunos')
# def atualizar_aluno(id):
#     aluno = Aluno.query.get_or_404(id)
#     aluno.nome = request.form['nome']
#     aluno.cpf = request.form['cpf']
#     aluno.data_nascimento = datetime.strptime(request.form['data_nascimento'], '%Y-%m-%d')
#     aluno.telefone = request.form['telefone']
#     aluno.email = request.form['email']
#     db.session.commit()
#     flash('Aluno atualizado com sucesso!', 'success')
#     return redirect(url_for('listar_alunos'))

# @app.route('/alunos/excluir/<int:id>', methods=['POST'])
# @login_required
# @requer_permissao('alunos')
# def excluir_aluno(id):
#     aluno = Aluno.query.get_or_404(id)
#     db.session.delete(aluno)
#     db.session.commit()
#     flash('Aluno excluído com sucesso!', 'success')
#     return redirect(url_for('listar_alunos'))

# # Rotas para Professores
# @app.route('/professores')
# @login_required
# @requer_permissao('professores')
# def listar_professores():
#     professores = Professor.query.all()
#     return render_template('professores/listar.html', professores=professores)

# @app.route('/professores/novo', methods=['GET', 'POST'])
# @login_required
# @requer_permissao('professores')
# def novo_professor():
#     modalidades = Modalidade.query.all()
#     if request.method == 'POST':
#         professor = Professor(
#             nome=request.form['nome'],
#             cpf=request.form['cpf'],
#             especialidade=request.form['especialidade'],
#             telefone=request.form['telefone'],
#             email=request.form['email']
#         )
#         db.session.add(professor)
#         db.session.commit()
#         flash('Professor cadastrado com sucesso!', 'success')
#         return redirect(url_for('listar_professores'))
#     return render_template('professores/novo.html', modalidades=modalidades)

# @app.route('/professores/editar/<int:id>', methods=['GET'])
# @login_required
# @requer_permissao('professores')
# def editar_professor(id):
#     professor = Professor.query.get_or_404(id)
#     return render_template('professores/novo.html', professor=professor)

# @app.route('/professores/atualizar/<int:id>', methods=['POST'])
# @login_required
# @requer_permissao('professores')
# def atualizar_professor(id):
#     professor = Professor.query.get_or_404(id)
#     professor.nome = request.form['nome']
#     professor.cpf = request.form['cpf']
#     professor.especialidade = request.form['especialidade']
#     professor.telefone = request.form['telefone']
#     professor.email = request.form['email']
#     db.session.commit()
#     flash('Professor atualizado com sucesso!', 'success')
#     return redirect(url_for('listar_professores'))

# @app.route('/professores/excluir/<int:id>', methods=['POST'])
# @login_required
# @requer_permissao('professores')
# def excluir_professor(id):
#     professor = Professor.query.get_or_404(id)
#     db.session.delete(professor)
#     db.session.commit()
#     flash('Professor excluído com sucesso!', 'success')
#     return redirect(url_for('listar_professores'))

# # Rotas para Modalidades
# @app.route('/modalidades')
# @login_required
# @requer_permissao('modalidades')
# def listar_modalidades():
#     modalidades = Modalidade.query.all()
#     return render_template('modalidades/listar.html', modalidades=modalidades)

# @app.route('/modalidades/nova', methods=['GET', 'POST'])
# @login_required
# @requer_permissao('modalidades')
# def nova_modalidade():
#     if request.method == 'POST':
#         modalidade = Modalidade(
#             nome=request.form['nome'],
#         )
#         db.session.add(modalidade)
#         db.session.commit()
#         flash('Modalidade cadastrada com sucesso!', 'success')
#         return redirect(url_for('listar_modalidades'))
#     return render_template('modalidades/nova.html')

# @app.route('/modalidades/editar/<int:id>', methods=['GET'])
# @login_required
# @requer_permissao('modalidades')
# def editar_modalidade(id):
#     modalidade = Modalidade.query.get_or_404(id)
#     return render_template('modalidades/nova.html', modalidade=modalidade)

# @app.route('/modalidades/atualizar/<int:id>', methods=['POST'])
# @login_required
# @requer_permissao('modalidades')
# def atualizar_modalidade(id):
#     modalidade = Modalidade.query.get_or_404(id)
#     modalidade.nome = request.form['nome']
#     modalidade.descricao = request.form['descricao']
#     modalidade.valor_mensal = float(request.form['valor_mensal'])
#     db.session.commit()
#     flash('Modalidade atualizada com sucesso!', 'success')
#     return redirect(url_for('listar_modalidades'))

# @app.route('/modalidades/excluir/<int:id>', methods=['POST'])
# @login_required
# @requer_permissao('modalidades')
# def excluir_modalidade(id):
#     modalidade = Modalidade.query.get_or_404(id)
#     db.session.delete(modalidade)
#     db.session.commit()
#     flash('Modalidade excluída com sucesso!', 'success')
#     return redirect(url_for('listar_modalidades'))

# # Rotas para Mensalidades
# @app.route('/mensalidades')
# @login_required
# @requer_permissao('mensalidades')
# def listar_mensalidades():
#     mensalidades = Mensalidade.query.all()
#     return render_template('mensalidades/listar.html', mensalidades=mensalidades)

# @app.route('/mensalidades/nova', methods=['GET', 'POST'])
# @login_required
# @requer_permissao('mensalidades')
# def nova_mensalidade():
#     if request.method == 'POST':
#         mensalidade = Mensalidade(
#             aluno_id=request.form['aluno_id'],
#             valor=float(request.form['valor']),
#             mes_referencia=datetime.strptime(request.form['mes_referencia'] + '-01', '%Y-%m-%d'),
#             status='pendente'
#         )
#         db.session.add(mensalidade)
#         db.session.commit()
#         flash('Mensalidade cadastrada com sucesso!', 'success')
#         return redirect(url_for('listar_mensalidades'))
#     alunos = Aluno.query.all()
#     return render_template('mensalidades/nova.html', alunos=alunos)

# @app.route('/mensalidades/editar/<int:id>', methods=['GET'])
# @login_required
# @requer_permissao('mensalidades')
# def editar_mensalidade(id):
#     mensalidade = Mensalidade.query.get_or_404(id)
#     alunos = Aluno.query.all()
#     return render_template('mensalidades/nova.html', mensalidade=mensalidade, alunos=alunos)

# @app.route('/mensalidades/atualizar/<int:id>', methods=['POST'])
# @login_required
# @requer_permissao('mensalidades')
# def atualizar_mensalidade(id):
#     mensalidade = Mensalidade.query.get_or_404(id)
#     mensalidade.aluno_id = request.form['aluno_id']
#     mensalidade.valor = float(request.form['valor'])
#     mensalidade.mes_referencia = datetime.strptime(request.form['mes_referencia'] + '-01', '%Y-%m-%d')
#     mensalidade.status = request.form['status']
#     db.session.commit()
#     flash('Mensalidade atualizada com sucesso!', 'success')
#     return redirect(url_for('listar_mensalidades'))

# @app.route('/mensalidades/excluir/<int:id>', methods=['POST'])
# @login_required
# @requer_permissao('mensalidades')
# def excluir_mensalidade(id):
#     mensalidade = Mensalidade.query.get_or_404(id)
#     db.session.delete(mensalidade)
#     db.session.commit()
#     flash('Mensalidade excluída com sucesso!', 'success')
#     return redirect(url_for('listar_mensalidades'))

# # Rotas para Contas a Pagar
# @app.route('/contas')
# @login_required
# @requer_permissao('contas')
# def listar_contas():
#     contas = ContaPagar.query.all()
#     return render_template('contas/listar.html', contas=contas)

# @app.route('/contas/nova', methods=['GET', 'POST'])
# @login_required
# @requer_permissao('contas')
# def nova_conta():
#     if request.method == 'POST':
#         conta = ContaPagar(
#             descricao=request.form['descricao'],
#             valor=float(request.form['valor']),
#             data_vencimento=datetime.strptime(request.form['data_vencimento'], '%Y-%m-%d'),
#             status='pendente'
#         )
#         db.session.add(conta)
#         db.session.commit()
#         flash('Conta cadastrada com sucesso!', 'success')
#         return redirect(url_for('listar_contas'))
#     return render_template('contas/nova.html')

# @app.route('/contas/editar/<int:id>', methods=['GET'])
# @login_required
# @requer_permissao('contas')
# def editar_conta(id):
#     conta = ContaPagar.query.get_or_404(id)
#     return render_template('contas/nova.html', conta=conta)

# @app.route('/contas/atualizar/<int:id>', methods=['POST'])
# @login_required
# @requer_permissao('contas')
# def atualizar_conta(id):
#     conta = ContaPagar.query.get_or_404(id)
#     conta.descricao = request.form['descricao']
#     conta.valor = float(request.form['valor'])
#     conta.data_vencimento = datetime.strptime(request.form['data_vencimento'], '%Y-%m-%d')
#     conta.status = request.form['status']
#     db.session.commit()
#     flash('Conta atualizada com sucesso!', 'success')
#     return redirect(url_for('listar_contas'))

# @app.route('/contas/excluir/<int:id>', methods=['POST'])
# @login_required
# @requer_permissao('contas')
# def excluir_conta(id):
#     conta = ContaPagar.query.get_or_404(id)
#     db.session.delete(conta)
#     db.session.commit()
#     flash('Conta excluída com sucesso!', 'success')
#     return redirect(url_for('listar_contas'))

# # Rotas para Planos
# @app.route('/planos')
# @login_required
# @requer_permissao('admin')
# def listar_planos():
#     planos = Plano.query.all()
#     return render_template('planos/listar.html', planos=planos)

# @app.route('/planos/novo', methods=['GET', 'POST'])
# @login_required
# @requer_permissao('admin')
# def novo_plano():
#     modalidades = Modalidade.query.all()
#     if request.method == 'POST':
#         modalidades = Modalidade.query.all()
#         plano = Plano(
#             nome=request.form['nome'],
#             descricao=request.form['descricao'],
#             valor_mensal=float(request.form['valor_mensal']),
#             modalidade_id = request.form['modalidade_id']
#         )
#         db.session.add(plano)
#         db.session.commit()
#         flash('Plano cadastrado com sucesso!', 'success')
#         return redirect(url_for('listar_planos'))
#     return render_template('planos/novo.html', modalidades=modalidades)

# @app.route('/planos/editar/<int:id>', methods=['GET', 'POST'])
# @login_required
# @requer_permissao('admin')
# def editar_plano(id):
#     plano = Plano.query.get_or_404(id)
#     modalidades = Modalidade.query.all()
#     if request.method == 'POST':
#         plano.nome = request.form['nome']
#         plano.descricao = request.form['descricao']
#         plano.valor_mensal = float(request.form['valor_mensal'])
#         db.session.commit()
#         flash('Plano atualizado com sucesso!', 'success')
#         return redirect(url_for('listar_planos'))
#     return render_template('planos/novo.html', plano=plano, modalidades=modalidades)

# @app.route('/planos/excluir/<int:id>', methods=['POST'])
# @login_required
# @requer_permissao('admin')
# def excluir_plano(id):
#     plano = Plano.query.get_or_404(id)
#     db.session.delete(plano)
#     db.session.commit()
#     flash('Plano excluído com sucesso!', 'success')
#     return redirect(url_for('listar_planos'))

# @app.route('/matricular', methods=['GET', 'POST'])
# @login_required
# @requer_permissao('admin')
# def matricular():
#     alunos = Aluno.query.all()  # Lista todos os alunos
#     planos = Plano.query.filter_by(ativo=True).all()  # Lista apenas planos ativos

#     if request.method == 'POST':
#         aluno_id = request.form['aluno_id']
#         plano_id = request.form['plano_id']

#         aluno = Aluno.query.get_or_404(aluno_id)
#         plano = Plano.query.get_or_404(plano_id)

#         # Verifica se o aluno já está matriculado no plano
#         if plano in aluno.planos:
#             flash('O aluno já está matriculado neste plano.', 'error')
#         else:
#             # Adiciona o plano ao aluno
#             aluno.planos.append(plano)
#             db.session.commit()
#             flash('Aluno matriculado no plano com sucesso!', 'success')
#         return redirect(url_for('listar_matriculas'))

#     return render_template('alunos/matricular.html', alunos=alunos, planos=planos)

# @app.route('/alunos/matriculas', methods=['GET'])
# @login_required
# @requer_permissao('admin')
# def listar_matriculas():
#     # Obtém todos os alunos com suas matrículas (planos associados)
#     alunos_com_matriculas = (
#         db.session.query(Aluno, aluno_plano.c.status, aluno_plano.c.data_matricula, Plano)
#         .join(aluno_plano, Aluno.id == aluno_plano.c.aluno_id)
#         .join(Plano, aluno_plano.c.plano_id == Plano.id)
#         .all()
#     )

#     # Organiza os dados para o template
#     alunos_organizados = {}
#     for aluno, status, data_matricula, plano in alunos_com_matriculas:
#         if aluno.id not in alunos_organizados:
#             alunos_organizados[aluno.id] = {
#                 'aluno': aluno,
#                 'matriculas': []
#             }
#         alunos_organizados[aluno.id]['matriculas'].append({
#             'plano_id': plano.id,  # Adiciona o ID do plano
#             'plano_nome': plano.nome,
#             'status': status,
#             'data_matricula': data_matricula.strftime('%d/%m/%Y')  # Formata a data
#         })

#     return render_template('alunos/listar_matriculas.html', alunos=alunos_organizados.values())


# @app.route('/alunos/alterar_status_matricula/<int:aluno_id>/<int:plano_id>', methods=['POST'])
# @login_required
# @requer_permissao('admin')
# def alterar_status_matricula(aluno_id, plano_id):
#     # Obtém a matrícula do aluno no plano especificado
#     matricula = db.session.query(aluno_plano).filter_by(aluno_id=aluno_id, plano_id=plano_id).first()

#     if matricula:
#         # Alterna o status entre 'ativo' e 'trancado'
#         novo_status = 'trancado' if matricula.status == 'ativo' else 'ativo'
        
#         # Atualiza o status da matrícula
#         db.session.execute(
#             aluno_plano.update()
#             .where(aluno_plano.c.aluno_id == aluno_id)
#             .where(aluno_plano.c.plano_id == plano_id)
#             .values(status=novo_status)
#         )
#         db.session.commit()

#         flash(f'Status da matrícula alterado para "{novo_status}" com sucesso!', 'success')
#     else:
#         flash('Matrícula não encontrada.', 'error')

#     return redirect(url_for('listar_matriculas'))


# @app.route('/relatorios/mensalidades')
# def relatorio_mensalidades():
    mensalidades = (
        db.session.query(Mensalidade, Aluno, Plano)
        .join(Aluno)
        .join(Matricula, Matricula.aluno_id == Aluno.id)
        .join(Plano, Matricula.plano_id == Plano.id)
        .filter(Aluno.ativo == True, Mensalidade.status == 'pendente')
        .order_by(Plano.nome, Mensalidade.status)
        .all()
    )
    
    
    return render_template('relatorios/mensalidades.html', mensalidades=mensalidades)

# @app.route('/confirmar_recebimento/<int:mensalidade_id>', methods=['POST'])
# @login_required
# @requer_permissao('confirmar_recebimento')
# def confirmar_recebimento(mensalidade_id):
    mensalidade = Mensalidade.query.get_or_404(mensalidade_id)
    mensalidade.status = 'pago'
    mensalidade.data_pagamento = datetime.now()
    db.session.commit()
    return redirect(url_for('relatorio_mensalidades'))

# @app.route('/abonar_pagamento/<int:mensalidade_id>', methods=['POST'])
# @login_required
# @requer_permissao('abonar_pagamento')
# def abonar_pagamento(mensalidade_id):
    mensalidade = Mensalidade.query.get_or_404(mensalidade_id)
    mensalidade.status = 'abonado'
    mensalidade.data_pagamento = datetime.now()
    db.session.commit()
    return redirect(url_for('relatorio_mensalidades'))


# Funções de Inicialização
def criar_permissoes():
    permissoes = [
        {'nome': 'Cadastro de Alunos', 'codigo': 'alunos'},
        {'nome': 'Cadastro de Professores', 'codigo': 'professores'},
        {'nome': 'Modalidades', 'codigo': 'modalidades'},
        {'nome': 'Mensalidades', 'codigo': 'mensalidades'},
        {'nome': 'Contas a Pagar', 'codigo': 'contas'},
    ]
    
    for p in permissoes:
        permissao = Permissao.query.filter_by(codigo=p['codigo']).first()
        if not permissao:
            permissao = Permissao(nome=p['nome'], codigo=p['codigo'])
            db.session.add(permissao)
    db.session.commit()


def criar_usuario_admin():
    with app.app_context():
        # Cria as permissões primeiro
        criar_permissoes()
        
        # Verifica se já existe algum usuário admin
        admin = Usuario.query.filter_by(tipo='admin').first()
        if not admin:
            # Cria um usuário admin com senha padrão
            senha_hash = generate_password_hash('admin123')
            admin = Usuario(
                username='admin',
                password=senha_hash,
                tipo='admin',
                nome_completo='Administrador',
                email='admin@academia.com'
            )
            db.session.add(admin)
            db.session.commit()
            print('Usuário admin criado com sucesso!')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        criar_usuario_admin()
    app.run(debug=True, port=5000)