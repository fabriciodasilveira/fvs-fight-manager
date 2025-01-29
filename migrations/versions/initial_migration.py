"""Initial migration

Revision ID: 1a2b3c4d5e6f
Revises: 
Create Date: 2024-01-29 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

revision = '1a2b3c4d5e6f'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Criação de todas as tabelas
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(length=80), nullable=False),
        sa.Column('password_hash', sa.String(length=128)),
        sa.Column('full_name', sa.String(length=120), nullable=False),
        sa.Column('phone', sa.String(length=20)),
        sa.Column('email', sa.String(length=120), nullable=False),
        sa.Column('is_admin', sa.Boolean(), default=False),
        sa.Column('is_active', sa.Boolean(), default=True),
        sa.Column('created_at', sa.DateTime(), default=sa.func.now()),
        sa.Column('last_login', sa.DateTime()),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('username'),
        sa.UniqueConstraint('email')
    )
    
    # Criar usuário admin inicial
    op.execute("""
        INSERT INTO users (username, password_hash, full_name, email, is_admin)
        VALUES (
            'admin',
            'pbkdf2:sha256:260000$FvnUsyh07BfMldxb$d9a3fd1793cd9c1527f74ff4f11162ebf48045d8c85b2c0f0066e869e2b80b91',
            'Administrador',
            'admin@example.com',
            TRUE
        )
    """)

def downgrade():
    op.drop_table('users')