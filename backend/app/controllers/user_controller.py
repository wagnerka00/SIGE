from flask import request

from app.services.user_service import UserService
from app.utils.api_response import success


class UserController:
    def __init__(self):
        self.service = UserService()

    def list(self):
        args = request.args.to_dict()
        return success(
            self.service.list_users(args),
            "Usuários carregados com sucesso",
            status=200,
        )

    def get(self, user_id: str):
        return success(
            self.service.get_user(user_id),
            "Usuário carregado com sucesso",
            status=200,
        )

    def create(self):
        data = request.get_json(silent=True) or {}
        return success(
            self.service.create_user(data),
            "Usuário cadastrado com sucesso",
            status=201,
        )

    def update(self, user_id: str):
        data = request.get_json(silent=True) or {}
        return success(
            self.service.update_user(user_id, data),
            "Usuário atualizado com sucesso",
            status=200,
        )

    def delete(self, user_id: str):
        result = self.service.delete_user(user_id)
        return success(result, "Usuário removido com sucesso", status=200)

