from flask import Flask
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy

from config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()


def create_app(config_class=Config) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # Permite que o frontend (servido localmente) chame a API.
    CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)

    from app.routes.auth_routes import auth_bp
    from app.routes.equipment_routes import equipment_bp
    from app.routes.user_routes import user_bp
    from app.routes.dashboard_routes import dashboard_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(equipment_bp, url_prefix="/api/equipments")
    app.register_blueprint(user_bp, url_prefix="/api/users")
    app.register_blueprint(dashboard_bp, url_prefix="/api/dashboard")

    @app.get("/api/health")
    def health():
        return {"status": "ok", "service": "SIGE UFPI"}, 200

    # Importa handlers de erro e callbacks do JWT
    from app.utils.errors import register_error_handlers
    from app.utils.jwt_handlers import register_jwt_handlers

    register_error_handlers(app)
    register_jwt_handlers(app)

    return app

