from flask_jwt_extended import create_access_token

from app import bcrypt
from app.repositories.user_repository import UserRepository
from app.utils.validation import validate_email
from app.utils.errors import BadRequest


class AuthService:
    def __init__(self):
        self.user_repo = UserRepository()

    def login(self, email: str, password: str) -> dict:
        email = (email or "").strip()
        if not email or not password:
            raise BadRequest("E-mail e senha são obrigatórios")

        email = validate_email(email)

        user = self.user_repo.find_by_email(email)
        if not user or not user.active:
            raise BadRequest("Credenciais inválidas")

        if not bcrypt.check_password_hash(user.password_hash, password):
            raise BadRequest("Credenciais inválidas")

        token = create_access_token(
            identity=user.id,
            additional_claims={"role": user.role, "email": user.email},
        )

        return {"token": token, "user": user.to_dict()}

