from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from models.models import db, Plano, Modalidade

planos_bp = Blueprint('planos', __name__, url_prefix='/planos')

@planos_bp.route('/')
@login_required
def listar_planos():
    planos = Plano.query.all()
    return render_template('planos/listar.html', planos=planos)

@planos_bp.route('/novo', methods=['GET', 'POST'])
@login_required
def novo_plano():
    modalidades = Modalidade.query.all()
    if request.method == 'POST':
        plano = Plano(
            nome=request.form['nome'],
            descricao=request.form['descricao'],
            valor_mensal=float(request.form['valor_mensal']),
            modalidade_id=request.form['modalidade_id']
        )
        db.session.add(plano)
        db.session.commit()
        flash('Plano cadastrado com sucesso!', 'success')
        return redirect(url_for('planos.listar_planos'))
    return render_template('planos/novo.html', modalidades=modalidades)


@planos_bp.route('/planos/editar/<int:id>', methods=['GET', 'POST'])
@login_required
#@requer_permissao('admin')
def editar_plano(id):
    plano = Plano.query.get_or_404(id)
    modalidades = Modalidade.query.all()
    if request.method == 'POST':
        plano.nome = request.form['nome']
        plano.descricao = request.form['descricao']
        plano.valor_mensal = float(request.form['valor_mensal'])
        db.session.commit()
        flash('Plano atualizado com sucesso!', 'success')
        return redirect(url_for('planos.listar_planos'))
    return render_template('planos/novo.html', plano=plano, modalidades=modalidades)

@planos_bp.route('/planos/excluir/<int:id>', methods=['POST'])
@login_required
#@requer_permissao('admin')
def excluir_plano(id):
    plano = Plano.query.get_or_404(id)
    db.session.delete(plano)
    db.session.commit()
    flash('Plano excluído com sucesso!', 'success')
    return redirect(url_for('planos.listar_planos'))