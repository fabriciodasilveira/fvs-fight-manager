from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from models.models import db, Aluno, Matricula, Plano
from datetime import datetime

matriculas_bp = Blueprint('matriculas', __name__, url_prefix='/matriculas')

@matriculas_bp.route('/')
@login_required
def listar_matriculas():
    matriculas = Matricula.query.all()

    return render_template('matriculas/listar.html', matriculas=matriculas)

@matriculas_bp.route('/novo', methods=['GET', 'POST'])
@login_required
def nova_matricula():
    alunos = Aluno.query.all()
    planos = Plano.query.filter_by(ativo=True).all()

    if request.method == 'POST':
        aluno_id = request.form['aluno_id']
        plano_id = request.form['plano_id']

        aluno = Aluno.query.get_or_404(aluno_id)
        plano = Plano.query.get_or_404(plano_id)

        # Criar a matrícula corretamente
        matricula = Matricula(aluno_id=aluno.id, plano_id=plano.id, data_matricula=datetime.utcnow())
        db.session.add(matricula)
        db.session.commit()
        flash('Matrícula realizada com sucesso!', 'success')

        return redirect(url_for('matriculas.listar_matriculas'))

    return render_template('matriculas/matricular.html', alunos=alunos, planos=planos)


@matriculas_bp.route('/alterar_status_matricula/<int:matricula_id>', methods=['POST'])
@login_required
#@requer_permissao('admin')
def alterar_status_matricula(matricula_id):
    matricula = Matricula.query.get_or_404(matricula_id)

    # Alternar status entre 'ativo' e 'trancado'
    matricula.status = 'trancado' if matricula.status == 'ativo' else 'ativo'
    db.session.commit()

    flash(f'Status da matrícula alterado para "{matricula.status}" com sucesso!', 'success')
    return redirect(url_for('matriculas.listar_matriculas'))


@matriculas_bp.route('/matricula/excluir/<int:id>', methods=['POST'])
@login_required
#@requer_permissao('admin')
def excluir_matricula(id):
    matricula = Matricula.query.get_or_404(id)

    db.session.delete(matricula)
    db.session.commit()
    flash('Matrícula excluída com sucesso!', 'success')

    return redirect(url_for('matriculas.listar_matriculas'))