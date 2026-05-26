from flask import request

from app.services.equipment_service import EquipmentService
from app.utils.api_response import success


class EquipmentController:
    def __init__(self):
        self.service = EquipmentService()

    def list(self):
        args = request.args.to_dict()
        return success(
            self.service.list_equipments(args),
            "Equipamentos carregados com sucesso",
            status=200,
        )

    def get(self, equipment_id: str):
        return success(
            self.service.get_equipment(equipment_id),
            "Equipamento carregado com sucesso",
            status=200,
        )

    def create(self):
        data = request.get_json(silent=True) or {}
        return success(
            self.service.create_equipment(data),
            "Equipamento cadastrado com sucesso",
            status=201,
        )

    def update(self, equipment_id: str):
        data = request.get_json(silent=True) or {}
        return success(
            self.service.update_equipment(equipment_id, data),
            "Equipamento atualizado com sucesso",
            status=200,
        )

    def delete(self, equipment_id: str):
        hard = request.args.get("hard", "false").lower() == "true"
        result = self.service.delete_equipment(equipment_id, hard=hard)
        return success(result, "Equipamento removido com sucesso", status=200)

