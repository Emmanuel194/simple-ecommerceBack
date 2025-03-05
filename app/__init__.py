from flask import Flask
from .models import db  
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('../instance/config.py')

  
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

   
    from .routes import main  
    app.register_blueprint(main)  

  
    with app.app_context():
        db.create_all()

    
    CORS(app)  

    return app
