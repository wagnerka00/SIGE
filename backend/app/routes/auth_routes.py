from flask import Blueprint

from app.controllers.auth_controller import AuthController

auth_bp = Blueprint("auth", __name__)
controller = AuthController()


@auth_bp.route("/login", methods=["POST"])
def login():
    return controller.login()

