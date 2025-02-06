from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from models.models import db, ContaPagar
from datetime import datetime

contas_bp = Blueprint('contas', __name__, url_prefix='/contas')

@contas_bp.route('/')
@login_required
def listar_contas():
    contas = ContaPagar.query.all()
    return render_template('contas/listar.html', contas=contas)

@contas_bp.route('/nova', methods=['GET', 'POST'])
@login_required
def nova_conta():
    if request.method == 'POST':
        conta = ContaPagar(
            descricao=request.form['descricao'],
            valor=float(request.form['valor']),
            data_vencimento=datetime.strptime(request.form['data_vencimento'], '%Y-%m-%d'),
            status='pendente'
        )
        db.session.add(conta)
        db.session.commit()
        flash('Conta cadastrada com sucesso!', 'success')
        return redirect(url_for('contas.listar_contas'))
    return render_template('contas/nova.html')

@contas_bp.route('/contas/editar/<int:id>', methods=['GET'])
@login_required
#@requer_permissao('contas')
def editar_conta(id):
    conta = ContaPagar.query.get_or_404(id)
    return render_template('contas/nova.html', conta=conta)

@contas_bp.route('/contas/atualizar/<int:id>', methods=['POST'])
@login_required
#@requer_permissao('contas')
def atualizar_conta(id):
    conta = ContaPagar.query.get_or_404(id)
    conta.descricao = request.form['descricao']
    conta.valor = float(request.form['valor'])
    conta.data_vencimento = datetime.strptime(request.form['data_vencimento'], '%Y-%m-%d')
    conta.status = request.form['status']
    db.session.commit()
    flash('Conta atualizada com sucesso!', 'success')
    return redirect(url_for('contas.listar_contas'))

@contas_bp.route('/contas/excluir/<int:id>', methods=['POST'])
@login_required
#@requer_permissao('contas')
def excluir_conta(id):
    conta = ContaPagar.query.get_or_404(id)
    db.session.delete(conta)
    db.session.commit()
    flash('Conta excluída com sucesso!', 'success')
    return redirect(url_for('contas.listar_contas'))
