from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Cadastro de Alunos
class Aluno(db.Model):
    __tablename__ = 'alunos'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    data_nascimento = db.Column(db.Date())
    sexo = db.Column(db.String(1))
    nome_responsavel = db.Column(db.String(100))
    celular_responsavel = db.Column(db.String(15))
    email = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    matriculas = db.relationship('Matricula', backref='aluno', lazy=True)

# Controle de Pagamento
class Pagamento(db.Model):
    __tablename__ = 'pagamentos'
    
    id = db.Column(db.Integer, primary_key=True)
    aluno_id = db.Column(db.Integer, db.ForeignKey('alunos.id'))
    plano_id = db.Column(db.Integer, db.ForeignKey('planos.id'))
    valor = db.Column(db.Float())
    data_pagamento = db.Column(db.DateTime())
    pago = db.Column(db.Boolean(), default=False)
    
    def calcular_comissao(self):
        return self.valor * 0.20  # Exemplo de cálculo

# Modalidades de Luta
class ModalidadeLuta(db.Model):
    __tablename__ = 'modalidades_lutas'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    descricao = db.Column(db.Text())
    
    # Relacionamento com professor
    professores = db.relationship('Professor', secondary='professor_modalidade')

# Professores
class Professor(db.Model):
    __tablename__ = 'professores'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    data_nascimento = db.Column(db.Date())
    sexo = db.Column(db.String(1))
    celular = db.Column(db.String(15))
    email = db.Column(db.String(100))
    
    # Relacionamentos
    turmas = db.relationship('Turma', backref='professor', lazy=True)
    modalidades = db.relationship('ModalidadeLuta', secondary='professor_modalidade')

# Turmas
class Turma(db.Model):
    __tablename__ = 'turmas'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    descricao = db.Column(db.Text())
    professor_id = db.Column(db.Integer, db.ForeignKey('professores.id'))
    
    # Relacionamentos
    horarios = db.relationship('Horario', backref='turma', lazy=True)

# Planos
class Plano(db.Model):
    __tablename__ = 'planos'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    descricao = db.Column(db.Text())
    valor = db.Column(db.Float())
    duracao = db.Column(db.Enum('mensal', 'trimestral', 'semestral', 'anual'))
    
# Matriculas
class Matricula(db.Model):
    __tablename__ = 'matriculas'
    
    id = db.Column(db.Integer, primary_key=True)
    aluno_id = db.Column(db.Integer, db.ForeignKey('alunos.id'))
    plano_id = db.Column(db.Integer, db.ForeignKey('planos.id'))
    turma_id = db.Column(db.Integer, db.ForeignKey('turmas.id'))
    data_matricula = db.Column(db.DateTime(), default=datetime.utcnow)

# Relacionamento entre Professor e Modalidade
class ProfessorModalidade(db.Model):
    __tablename__ = 'professor_modalidade'
    
    professor_id = db.Column(db.Integer, db.ForeignKey('professores.id'))
    modalidade_id = db.Column(db.Integer, db.ForeignKey('modalidades_lutas.id'))

# Horarios
class Horario(db.Model):
    __tablename__ = 'horarios'
    
    id = db.Column(db.Integer, primary_key=True)
    dia_semana = db.Column(db.String(10))
    hora_inicio = db.Column(db.Time())
    hora_fim = db.Column(db.Time())
    turma_id = db.Column(db.Integer, db.ForeignKey('turmas.id'))
    professor_id = db.Column(db.Integer, db.ForeignKey('professores.id'))

# Usuários e Permissões
class Usuario(db.Model):
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True)
    nome_completo = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    celular = db.Column(db.String(15))
    
    # Relacionamento com permissões
    permissions = db.relationship('Permiso', secondary='usuario_permisao')
