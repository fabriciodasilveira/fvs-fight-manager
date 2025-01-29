# app.py
from flask import Flask
from flask_migrate import Migrate
from models import db
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize extensions
    db.init_app(app)
    migrate = Migrate(app, db)
    
    return app

app = create_app()

# Este trecho é importante para o Flask CLI encontrar a aplicação
if __name__ == '__main__':
    app.run(debug=True)