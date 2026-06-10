import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from src.infrastructure.models import db
from src.presentation.controllers import bp as api_bp

def create_app():
    app = Flask(__name__)
    app.json.ensure_ascii = False

    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://user:password@localhost/db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'GjGISdgJSDHudhuBGBDuHDSUHbGUDIgRIHGEIldafJ-key')

    db.init_app(app)
    jwt = JWTManager(app)

    app.register_blueprint(api_bp, url_prefix='/api/v1')

    with app.app_context():
        db.create_all()

    return app

app = create_app()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
