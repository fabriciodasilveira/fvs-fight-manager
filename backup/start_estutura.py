import os

def criar_estrutura_projeto(nome_projeto):
    """Cria a estrutura de um projeto Python.

    Args:
        nome_projeto (str): Nome do projeto.
    """

    # Cria o diretório principal do projeto
    os.makedirs(nome_projeto)

    # Cria o diretório app e suas subpastas
    os.makedirs(os.path.join(nome_projeto, 'app', 'static', 'css'))
    os.makedirs(os.path.join(nome_projeto, 'app', 'static', 'js'))
    os.makedirs(os.path.join(nome_projeto, 'app', 'static', 'img'))
    os.makedirs(os.path.join(nome_projeto, 'app', 'templates'))
    os.makedirs(os.path.join(nome_projeto, 'app', 'templates', 'usuarios'))
    os.makedirs(os.path.join(nome_projeto, 'app', 'templates', 'pagamentos'))
    os.makedirs(os.path.join(nome_projeto, 'app', 'templates', 'profissionais'))
    os.makedirs(os.path.join(nome_projeto, 'app', 'templates', 'matriculas'))

    # Cria os arquivos dentro do diretório app
    with open(os.path.join(nome_projeto, 'app', 'templates', 'base.html'), 'w') as f:
        f.write("<!DOCTYPE html>\n<html>\n<head>\n<title>Meu Projeto</title>\n</head>\n<body>\n</body>\n</html>")

    with open(os.path.join(nome_projeto, 'app', 'models.py'), 'w') as f:
        pass  # Adicione aqui o código para definir seus modelos

    with open(os.path.join(nome_projeto, 'app', 'views.py'), 'w') as f:
        pass  # Adicione aqui o código para definir suas views

    with open(os.path.join(nome_projeto, 'app', 'routes.py'), 'w') as f:
        pass  # Adicione aqui o código para definir suas rotas

    with open(os.path.join(nome_projeto, 'app', 'controllers.py'), 'w') as f:
        pass  # Adicione aqui o código para definir seus controladores

# Exemplo de uso
criar_estrutura_projeto('FVS-Gym-Fight')