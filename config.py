# config.py
import os
from datetime import timedelta
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Configurações básicas
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'sua-chave-secreta-aqui'
    
    # Configuração do SQLAlchemy
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'instance', 'academy.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Configurações de Upload
    UPLOAD_FOLDER = os.path.join(basedir, 'static', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max-limit
    
    # Configurações do MercadoPago
    MERCADO_PAGO_PUBLIC_KEY = os.environ.get('MERCADO_PAGO_PUBLIC_KEY')
    MERCADO_PAGO_ACCESS_TOKEN = os.environ.get('MERCADO_PAGO_ACCESS_TOKEN')
    
    # Configurações de e-mail
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.gmail.com'
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    
    # Configurações PWA
    PWA_NAME = 'Academia de Lutas'
    PWA_ICON_PATH = os.path.join('static', 'images', 'icons')
    PWA_START_URL = '/'
    PWA_DISPLAY = 'standalone'
    
    # Configurações da Sessão
    PERMANENT_SESSION_LIFETIME = timedelta(days=31)
    SESSION_TYPE = 'filesystem'
    
    # Configurações de Paginação
    ITEMS_PER_PAGE = 10
    
    # Configurações de segurança
    SESSION_COOKIE_SECURE = True
    REMEMBER_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True
    
    # Configurações de logging
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
    
    @staticmethod
    def init_app(app):
        """Inicialização de configurações específicas da aplicação"""
        # Criar diretório de uploads se não existir
        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
        
        # Configurar logging
        if Config.LOG_TO_STDOUT:
            import logging
            from logging import StreamHandler
            file_handler = StreamHandler()
            file_handler.setLevel(logging.INFO)
            app.logger.addHandler(file_handler)

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    
class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False
    
class ProductionConfig(Config):
    # Configurações específicas de produção
    DEBUG = False
    TESTING = False
    
    # Usar variáveis de ambiente em produção
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    
    @classmethod
    def init_app(cls, app):
        Config.init_app(app)
        
        # Configuração de log para produção
        import logging
        from logging.handlers import RotatingFileHandler
        file_handler = RotatingFileHandler('logs/academy.log',
                                         maxBytes=10240,
                                         backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s '
            '[in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('Academia de Lutas startup')

# Dicionário com as configurações disponíveis
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}