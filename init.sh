#!/bin/bash

# Criar ambiente virtual
# python -m venv venv

# Ativar ambiente virtual
# source venv/bin/activate  # No Windows use: venv\Scripts\activate

# Instalar dependências
# pip install -r requirements.txt
# pip install python-dotenv

# Remover banco de dados antigo se existir
rm -f instance/academy.db

# Criar diretório instance se não existir
mkdir -p instance

# Exportar a variável FLASK_APP
export FLASK_APP=app.py

# Inicializar banco de dados
flask db init
flask db migrate -m "Initial migration"
flask db upgrade

# Criar usuário admin e dados iniciais
python utils/db_init.py

echo "Sistema inicializado com sucesso!"
echo "Usuário admin criado:"
echo "Username: admin"