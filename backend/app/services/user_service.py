from app import bcrypt
from app.models.user import User, UserRole
from app.repositories.user_repository import UserRepository
from app.utils.errors import BadRequest, NotFound
from app.utils.validation import parse_pagination, require_fields, validate_email, validate_role


class UserService:
    def __init__(self):
        self.repo = UserRepository()

    def list_users(self, args: dict):
        page, per_page = parse_pagination(
            args,
            default_page=1,
            default_per_page=10,
            max_per_page=100,
        )
        search = args.get("search")
        pagination = self.repo.list(page=page, per_page=per_page, search=search)
        return {
            "items": [u.to_dict() for u in pagination.items],
            "pagination": {
                "page": pagination.page,
                "per_page": pagination.per_page,
                "total": pagination.total,
                "pages": pagination.pages,
            },
        }

    def get_user(self, user_id: str) -> dict:
        user = self.repo.find_by_id(user_id)
        if not user:
            raise NotFound("Usuário não encontrado")
        return user.to_dict()

    def create_user(self, data: dict) -> dict:
        missing = require_fields(data, ["name", "email", "password", "role"])
        if missing:
            raise BadRequest(f"Campos obrigatórios: {', '.join(missing)}")

        name = data["name"].strip()
        email = validate_email(data["email"])
        role = validate_role(data["role"])
        password = data["password"]

        if len(password) < 6:
            raise BadRequest("Senha deve ter pelo menos 6 caracteres")

        if self.repo.find_by_email(email):
            raise BadRequest("E-mail já cadastrado")

        user = User(
            name=name,
            email=email,
            password_hash=bcrypt.generate_password_hash(password).decode("utf-8"),
            role=role,
            active=bool(data.get("active", True)),
        )
        self.repo.create(user)
        return user.to_dict()

    def update_user(self, user_id: str, data: dict) -> dict:
        user = self.repo.find_by_id(user_id)
        if not user:
            raise NotFound("Usuário não encontrado")

        if "name" in data and data["name"]:
            user.name = data["name"].strip()

        if "email" in data and data["email"]:
            email = validate_email(data["email"])
            existing = self.repo.find_by_email(email)
            if existing and existing.id != user_id:
                raise BadRequest("E-mail já cadastrado")
            user.email = email

        if "role" in data and data["role"]:
            user.role = validate_role(data["role"])

        if "active" in data:
            user.active = bool(data["active"])

        if "password" in data and data["password"]:
            password = data["password"]
            if len(password) < 6:
                raise BadRequest("Senha deve ter pelo menos 6 caracteres")
            user.password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

        self.repo.update(user)
        return user.to_dict()

    def delete_user(self, user_id: str) -> dict:
        user = self.repo.find_by_id(user_id)
        if not user:
            raise NotFound("Usuário não encontrado")
        self.repo.delete(user)
        return {"id": user_id}

