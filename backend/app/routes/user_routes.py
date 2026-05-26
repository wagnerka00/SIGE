from flask import Blueprint

from app.controllers.user_controller import UserController
from app.middlewares.auth_middleware import admin_required

user_bp = Blueprint("users", __name__)
controller = UserController()


@user_bp.route("", methods=["GET"])
@admin_required
def list_users():
    return controller.list()


@user_bp.route("/<user_id>", methods=["GET"])
@admin_required
def get_user(user_id: str):
    return controller.get(user_id)


@user_bp.route("", methods=["POST"])
@admin_required
def create_user():
    return controller.create()


@user_bp.route("/<user_id>", methods=["PUT"])
@admin_required
def update_user(user_id: str):
    return controller.update(user_id)


@user_bp.route("/<user_id>", methods=["DELETE"])
@admin_required
def delete_user(user_id: str):
    return controller.delete(user_id)

