from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from models.models import db, Professor, Modalidade

professores_bp = Blueprint('professores', __name__, url_prefix='/professores')

@professores_bp.route('/')
@login_required
def listar_professores():
    professores = Professor.query.all()
    return render_template('professores/listar.html', professores=professores)

@professores_bp.route('/novo', methods=['GET', 'POST'])
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
        flash('Professor cadastrado com sucesso!', 'success')
        return redirect(url_for('professores.listar_professores'))
    return render_template('professores/novo.html')

@professores_bp.route('/professores/editar/<int:id>', methods=['GET'])
@login_required
#@requer_permissao('professores')
def editar_professor(id):
    modalidades = Modalidade.query.all()
    professor = Professor.query.get_or_404(id)
    return render_template('professores/novo.html', professor=professor, modalidades=modalidades)

@professores_bp.route('/professores/atualizar/<int:id>', methods=['POST'])
@login_required
#@requer_permissao('professores')
def atualizar_professor(id):
    professor = Professor.query.get_or_404(id)
    professor.nome = request.form['nome']
    professor.cpf = request.form['cpf']
    professor.especialidade = request.form['especialidade']
    professor.telefone = request.form['telefone']
    professor.email = request.form['email']
    db.session.commit()
    flash('Professor atualizado com sucesso!', 'success')
    return redirect(url_for('professores.listar_professores'))

@professores_bp.route('/professores/excluir/<int:id>', methods=['POST'])
@login_required
#@requer_permissao('professores')
def excluir_professor(id):
    professor = Professor.query.get_or_404(id)
    db.session.delete(professor)
    db.session.commit()
    flash('Professor excluído com sucesso!', 'success')
    return redirect(url_for('professores.listar_professores'))