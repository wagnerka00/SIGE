from flask_jwt_extended.exceptions import (
    JWTDecodeError,
    InvalidHeaderError,
    NoAuthorizationError,
    FreshTokenRequired,
    WrongTokenError,
    RevokedTokenError,
)
from app.utils.api_response import error


def register_jwt_handlers(app) -> None:
    # Handlers básicos de erro do JWT para respostas consistentes.
    @app.errorhandler(NoAuthorizationError)
    def handle_no_auth(_exc):
        return error("Token de autenticação ausente", 401)

    @app.errorhandler(JWTDecodeError)
    def handle_decode(_exc):
        return error("Token inválido", 401)

    @app.errorhandler(InvalidHeaderError)
    def handle_invalid_header(_exc):
        return error("Cabeçalho de autorização inválido", 401)

    @app.errorhandler(FreshTokenRequired)
    def handle_fresh(_exc):
        return error("Token fresco necessário", 401)

    @app.errorhandler(WrongTokenError)
    def handle_wrong_token(_exc):
        return error("Token expirado ou inválido", 401)

    @app.errorhandler(RevokedTokenError)
    def handle_revoked(_exc):
        return error("Token revogado", 401)

