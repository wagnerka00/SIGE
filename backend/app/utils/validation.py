import re

from app.models.equipment import EquipmentStatus
from app.models.user import UserRole


def require_fields(data: dict, fields: list[str]) -> list[str]:
    missing = []
    for f in fields:
        if f not in data or data.get(f) in (None, "", []):
            missing.append(f)
    return missing


def validate_email(email: str) -> str:
    if not email:
        raise ValueError("E-mail é obrigatório")
    email = email.strip().lower()
    # Validação simples; para maior robustez usar libraries específicas.
    if not re.match(r"^[^@\\s]+@[^@\\s]+\\.[^@\\s]+$", email):
        raise ValueError("E-mail inválido")
    return email


def validate_role(role: str) -> str:
    if not role:
        raise ValueError("Perfil é obrigatório")
    role = role.strip().lower()
    if role not in UserRole.ALL:
        raise ValueError(f"Perfil inválido. Valores: {', '.join(UserRole.ALL)}")
    return role


def validate_status(status: str) -> str:
    if not status:
        raise ValueError("Status é obrigatório")
    status = status.strip().lower()
    if status not in EquipmentStatus.ALL:
        raise ValueError(
            f"Status inválido. Valores: {', '.join(EquipmentStatus.ALL)}"
        )
    return status


def parse_pagination(args, default_page: int, default_per_page: int, max_per_page: int):
    try:
        page = int(args.get("page", default_page))
    except Exception:
        page = default_page
    try:
        per_page = int(args.get("per_page", default_per_page))
    except Exception:
        per_page = default_per_page
    if page < 1:
        page = default_page
    if per_page < 1:
        per_page = default_per_page
    if per_page > max_per_page:
        per_page = max_per_page
    return page, per_page

