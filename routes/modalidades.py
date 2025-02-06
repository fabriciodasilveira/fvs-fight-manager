from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from models.models import db, Modalidade

modalidades_bp = Blueprint('modalidades', __name__, url_prefix='/modalidades')

@modalidades_bp.route('/')
@login_required
def listar_modalidades():
    modalidades = Modalidade.query.all()
    return render_template('modalidades/listar.html', modalidades=modalidades)

@modalidades_bp.route('/nova', methods=['GET', 'POST'])
@login_required
def nova_modalidade():
    if request.method == 'POST':
        modalidade = Modalidade(nome=request.form['nome'])
        db.session.add(modalidade)
        db.session.commit()
        flash('Modalidade cadastrada com sucesso!', 'success')
        return redirect(url_for('modalidades.listar_modalidades'))
    return render_template('modalidades/nova.html')


@modalidades_bp.route('/modalidades/editar/<int:id>', methods=['GET'])
@login_required
#@requer_permissao('modalidades')
def editar_modalidade(id):
    modalidade = Modalidade.query.get_or_404(id)
    return render_template('modalidades/nova.html', modalidade=modalidade)

@modalidades_bp.route('/modalidades/atualizar/<int:id>', methods=['POST'])
@login_required
#@requer_permissao('modalidades')
def atualizar_modalidade(id):
    modalidade = Modalidade.query.get_or_404(id)
    modalidade.nome = request.form['nome']
    db.session.commit()
    flash('Modalidade atualizada com sucesso!', 'success')
    return redirect(url_for('modalidades.listar_modalidades'))

@modalidades_bp.route('/modalidades/excluir/<int:id>', methods=['POST'])
@login_required
#@requer_permissao('modalidades')
def excluir_modalidade(id):
    modalidade = Modalidade.query.get_or_404(id)
    db.session.delete(modalidade)
    db.session.commit()
    flash('Modalidade excluída com sucesso!', 'success')
    return redirect(url_for('modalidades.listar_modalidades'))