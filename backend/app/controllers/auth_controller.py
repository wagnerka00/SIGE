from flask import Request, request

from app.services.auth_service import AuthService
from app.utils.api_response import success


class AuthController:
    def __init__(self):
        self.service = AuthService()

    def login(self):
        data: dict = request.get_json(silent=True) or {}
        result = self.service.login(data.get("email"), data.get("password"))
        return success(result, "Login realizado com sucesso", status=200)

