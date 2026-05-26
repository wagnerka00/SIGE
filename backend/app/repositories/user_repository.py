from app import db
from app.models.user import User


class UserRepository:
    def find_by_email(self, email: str) -> User | None:
        if not email:
            return None
        return User.query.filter(db.func.lower(User.email) == email.strip().lower()).first()

    def find_by_id(self, user_id: str) -> User | None:
        return User.query.filter_by(id=user_id).first()

    def list(self, page: int, per_page: int, search: str | None = None):
        query = User.query
        if search:
            term = f"%{search}%"
            query = query.filter(
                db.or_(
                    User.name.ilike(term),
                    User.email.ilike(term),
                )
            )
        pagination = query.order_by(User.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        return pagination

    def create(self, user: User) -> User:
        db.session.add(user)
        db.session.commit()
        return user

    def update(self, user: User) -> User:
        db.session.commit()
        return user

    def delete(self, user: User) -> None:
        db.session.delete(user)
        db.session.commit()

