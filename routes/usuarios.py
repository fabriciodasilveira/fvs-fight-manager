from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models.models import db, Usuario, Permissao
from werkzeug.security import generate_password_hash
from functools import wraps

usuarios_bp = Blueprint('usuarios', __name__, url_prefix='/usuarios')

def requer_permissao(codigo_permissao):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.tem_permissao(codigo_permissao):
                flash('Acesso negado.', 'error')
                return redirect(url_for('index'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

@usuarios_bp.route('/')
@login_required
@requer_permissao('admin')
def listar_usuarios():
    usuarios = Usuario.query.all()
    return render_template('usuarios/listar.html', usuarios=usuarios)

@usuarios_bp.route('/novo', methods=['GET', 'POST'])
@login_required
@requer_permissao('admin')
def novo_usuario():
    if request.method == 'POST':
        permissoes_selecionadas = request.form.getlist('permissoes')
        
        novo_usuario = Usuario(
            username=request.form['username'],
            password=generate_password_hash(request.form['password']),
            nome_completo=request.form['nome_completo'],
            email=request.form['email'],
            tipo = request.form['tipo']
        )
        
        permissoes = Permissao.query.filter(Permissao.codigo.in_(permissoes_selecionadas)).all()
        novo_usuario.permissoes = permissoes
        
        db.session.add(novo_usuario)
        db.session.commit()
        flash('Usuário cadastrado com sucesso!')
        return redirect(url_for('usuarios.listar_usuarios'))
    
    permissoes = Permissao.query.all()
    return render_template('usuarios/novo.html', permissoes=permissoes)

# Rotas para Usuários
@usuarios_bp.route('/usuarios/editar/<int:id>', methods=['GET', 'POST'])
@login_required
#@requer_permissao('admin')
def editar_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    if request.method == 'POST':
        usuario.username = request.form['username']
        usuario.nome_completo = request.form['nome_completo']
        usuario.email = request.form['email']
        usuario.tipo = request.form['tipo']
        
        # Atualiza as permissões
        permissoes_selecionadas = request.form.getlist('permissoes')
        permissoes = Permissao.query.filter(Permissao.codigo.in_(permissoes_selecionadas)).all()
        usuario.permissoes = permissoes
        
        db.session.commit()
        flash('Usuário atualizado com sucesso!', 'success')
        return redirect(url_for('usuarios.listar_usuarios'))
    
    permissoes = Permissao.query.all()
    return render_template('usuarios/novo.html', usuario=usuario, permissoes=permissoes)

@usuarios_bp.route('/usuarios/excluir/<int:id>', methods=['POST'])
@login_required
#@requer_permissao('admin')
def excluir_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    if usuario.tipo == 'admin':
        flash('Não é possível excluir um usuário admin.', 'error')
    else:
        db.session.delete(usuario)
        db.session.commit()
        flash('Usuário excluído com sucesso!', 'success')
    return redirect(url_for('usuarios.listar_usuarios'))