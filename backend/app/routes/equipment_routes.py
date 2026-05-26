from flask import Blueprint

from app.controllers.equipment_controller import EquipmentController
from app.middlewares.auth_middleware import admin_required, authenticated_required, tecnico_or_admin_required

equipment_bp = Blueprint("equipments", __name__)
controller = EquipmentController()


@equipment_bp.route("", methods=["GET"])
@authenticated_required
def list_equipments():
    return controller.list()


@equipment_bp.route("/<equipment_id>", methods=["GET"])
@authenticated_required
def get_equipment(equipment_id: str):
    return controller.get(equipment_id)


@equipment_bp.route("", methods=["POST"])
@tecnico_or_admin_required
def create_equipment():
    return controller.create()


@equipment_bp.route("/<equipment_id>", methods=["PUT"])
@tecnico_or_admin_required
def update_equipment(equipment_id: str):
    return controller.update(equipment_id)


@equipment_bp.route("/<equipment_id>", methods=["DELETE"])
@admin_required
def delete_equipment(equipment_id: str):
    return controller.delete(equipment_id)

