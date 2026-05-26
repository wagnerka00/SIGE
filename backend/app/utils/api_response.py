from typing import Any

from flask import jsonify


def success(data: Any = None, message: str = "Operação realizada com sucesso", status: int = 200):
    body: dict[str, Any] = {"success": True, "message": message}
    if data is not None:
        body["data"] = data
    return jsonify(body), status


def error(
    message: str = "Erro na operação",
    status: int = 400,
    errors: Any = None,
):
    body: dict[str, Any] = {"success": False, "message": message}
    if errors is not None:
        body["errors"] = errors
    return jsonify(body), status

