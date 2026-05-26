from functools import wraps

from flask import g
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity

from app.models.user import UserRole
from app.repositories.user_repository import UserRepository
from app.utils.errors import Forbidden


user_repo = UserRepository()


def load_user_from_jwt() -> None:
    user_id = get_jwt_identity()
    if not user_id:
        g.current_user = None
        return
    user = user_repo.find_by_id(user_id)
    # Pode ter ficado inativo após login.
    g.current_user = user if user and user.active else None


def roles_required(*allowed_roles: str):
    def decorator(fn):
        @wraps(fn)
        @jwt_required()
        def wrapper(*args, **kwargs):
            load_user_from_jwt()
            if not g.current_user:
                raise Forbidden("Usuário não autenticado ou inativo")
            claims = get_jwt()
            role = claims.get("role") or g.current_user.role
            if role not in allowed_roles:
                raise Forbidden("Permissão negada para esta operação")
            return fn(*args, **kwargs)

        return wrapper

    return decorator


def admin_required(fn):
    return roles_required(UserRole.ADMIN)(fn)


def tecnico_or_admin_required(fn):
    return roles_required(UserRole.ADMIN, UserRole.TECNICO)(fn)


def authenticated_required(fn):
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        load_user_from_jwt()
        if not g.current_user:
            raise Forbidden("Usuário não autenticado ou inativo")
        return fn(*args, **kwargs)

    return wrapper

