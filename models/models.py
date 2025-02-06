
from flask_migrate import Migrate
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from models import db
from datetime import datetime


# Modelos
class Usuario(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    tipo = db.Column(db.String(20), nullable=False)  # 'admin', 'usuario'
    nome_completo = db.Column(db.String(100))
    email = db.Column(db.String(120))
    ativo = db.Column(db.Boolean, default=True)
    permissoes = db.relationship('Permissao', secondary='usuario_permissao', lazy='subquery',
        backref=db.backref('usuarios', lazy=True))

    def tem_permissao(self, codigo_permissao):
        if self.tipo == 'admin':  # Admin tem todas as permissões
            return True
        return any(p.codigo == codigo_permissao for p in self.permissoes)

class Permissao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    codigo = db.Column(db.String(50), unique=True, nullable=False)

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


class Pagamento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    matricula_id = db.Column(db.Integer, db.ForeignKey('matricula.id'), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    mes_referencia = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), default='pendente')  # 'pendente', 'pago'
    data_pagamento = db.Column(db.Date)

# Modelo de Modalidade
class Modalidade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    planos = db.relationship('Plano', backref='modalidade', lazy=True)
    
#  Modelo de Plano
class Plano(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text)
    valor_mensal = db.Column(db.Float, nullable=False)
    ativo = db.Column(db.Boolean, default=True)  # Indica se o plano está ativo
    modalidade_id = db.Column(db.Integer, db.ForeignKey('modalidade.id'), nullable=False)



class Aluno(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    cpf = db.Column(db.String(11), unique=True, nullable=False)
    data_nascimento = db.Column(db.Date, nullable=False)
    telefone = db.Column(db.String(20))
    ativo = db.Column(db.Boolean, default=True)
    email = db.Column(db.String(120))
    matriculas = db.relationship('Matricula', backref='aluno', lazy=True)
    
    
    
# Correção da definição de 'aluno_plano'
# aluno_plano = db.Table('aluno_plano',
#     db.Column('aluno_id', db.Integer, db.ForeignKey('aluno.id'), primary_key=True),
#     db.Column('plano_id', db.Integer, db.ForeignKey('plano.id'), primary_key=True),
#     db.Column('data_matricula', db.DateTime, default=datetime.utcnow),
#     db.Column('status', db.String(20), default='ativo')  # Status da matrícula (ativo/trancado)
# )


usuario_permissao = db.Table('usuario_permissao',
    db.Column('usuario_id', db.Integer, db.ForeignKey('usuario.id'), primary_key=True),
    db.Column('permissao_id', db.Integer, db.ForeignKey('permissao.id'), primary_key=True)
)

class Turma(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    
    # Relação com Modalidade
    modalidades = db.relationship('Modalidade', secondary='turma_modalidade', backref='turmas')
    

# Tabela de Associação entre Turmas e Modalidades
turma_modalidade = db.Table('turma_modalidade',
    db.Column('turma_id', db.Integer, db.ForeignKey('turma.id'), primary_key=True),
    db.Column('modalidade_id', db.Integer, db.ForeignKey('modalidade.id'), primary_key=True)
)


class Matricula(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    aluno_id = db.Column(db.Integer, db.ForeignKey('aluno.id'), nullable=False)
    plano_id = db.Column(db.Integer, db.ForeignKey('plano.id'), nullable=False)
    status = db.Column(db.String(20), default='ativo')  # 'ativo', 'trancado', 'cancelado'
    data_matricula = db.Column(db.DateTime, default=datetime.utcnow)
    data_vencimento = db.Column(db.Date)  # Define a data da próxima cobrança