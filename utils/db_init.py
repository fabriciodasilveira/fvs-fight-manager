# utils/db_init.py
from models import db, User, Permission
from werkzeug.security import generate_password_hash

def init_db():
    """Inicializa o banco de dados com dados básicos"""
    # Criar tabelas
    db.create_all()
    
    # Verificar se já existe um usuário admin
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        # Criar usuário admin
        admin = User(
            username='admin',
            full_name='Administrador',
            email='admin@example.com',
            is_admin=True
        )
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        
        # Criar todas as permissões para o admin
        permissions = Permission.create_default_permissions(admin.id)
        for perm in permissions:
            perm.can_create = True
            perm.can_edit = True
            perm.can_delete = True
            db.session.add(perm)
        
        db.session.commit()

if __name__ == '__main__':
    init_db()