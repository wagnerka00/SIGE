from __future__ import annotations

from dataclasses import dataclass

from flask import Flask

from app.utils.api_response import error


class AppError(Exception):
    status_code: int = 400
    message: str = "Erro"

    def __init__(self, message: str | None = None, errors=None):
        super().__init__(message or self.message)
        self.errors = errors


class BadRequest(AppError):
    status_code = 400
    message = "Requisição inválida"


class NotFound(AppError):
    status_code = 404
    message = "Recurso não encontrado"


class Unauthorized(AppError):
    status_code = 401
    message = "Não autorizado"


class Forbidden(AppError):
    status_code = 403
    message = "Acesso proibido"


def register_error_handlers(app: Flask) -> None:
    @app.errorhandler(AppError)
    def handle_app_error(exc: AppError):
        return error(
            message=str(exc) or exc.message,
            status=exc.status_code,
            errors=getattr(exc, "errors", None),
        )

    @app.errorhandler(404)
    def handle_404(_exc):
        return error("Rota não encontrada", 404)

    @app.errorhandler(Exception)
    def handle_unexpected(exc: Exception):
        # Evita vazar detalhes sensíveis em produção.
        return error("Erro interno do servidor", 500)

