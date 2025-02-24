from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from models.models import db, Aluno
from datetime import datetime

alunos_bp = Blueprint('alunos', __name__, url_prefix='/alunos')

@alunos_bp.route('/')
@login_required
def listar_alunos():
    alunos = Aluno.query.all()
    return render_template('alunos/listar.html', alunos=alunos)

@alunos_bp.route('/novo', methods=['GET', 'POST'])
@login_required
def novo_aluno():
    if request.method == 'POST':
        aluno = Aluno(
            nome=request.form['nome'],
            cpf=request.form['cpf'],
            data_nascimento=datetime.strptime(request.form['data_nascimento'], '%Y-%m-%d'),
            telefone=request.form['telefone'],
            email=request.form['email'],
            endereco=request.form['endereco'],
            responsavel= request.form['responsavel'],
            contato_emergencia= request.form['contato_emergencia']
        )
        db.session.add(aluno)
        db.session.commit()
        flash('Aluno cadastrado com sucesso!', 'success')
        return redirect(url_for('alunos.listar_alunos'))
    return render_template('alunos/novo.html')

@alunos_bp.route('/editar/<int:id>', methods=['GET'])
@login_required
#@requer_permissao('alunos')
def editar_aluno(id):
    aluno = Aluno.query.get_or_404(id)
    return render_template('alunos/novo.html', aluno=aluno)

@alunos_bp.route('/atualizar/<int:id>', methods=['POST'])
@login_required
#@requer_permissao('alunos')
def atualizar_aluno(id):
    aluno = Aluno.query.get_or_404(id)
    aluno.nome = request.form['nome']
    aluno.cpf = request.form['cpf']
    aluno.data_nascimento = datetime.strptime(request.form['data_nascimento'], '%Y-%m-%d')
    aluno.telefone = request.form['telefone']
    aluno.email = request.form['email']
    aluno.responsavel = request.form['responsavel']
    aluno.endereco = request.form['endereco']
    aluno.contato_emergencia = request.form['contato_emergencia']
    db.session.commit()
    flash('Aluno atualizado com sucesso!', 'success')
    return redirect(url_for('alunos.listar_alunos'))

@alunos_bp.route('/excluir/<int:id>', methods=['POST'])
@login_required
#@requer_permissao('alunos')
def excluir_aluno(id):
    aluno = Aluno.query.get_or_404(id)
    db.session.delete(aluno)
    db.session.commit()
    flash('Aluno excluído com sucesso!', 'success')
    return redirect(url_for('alunos.listar_alunos'))
