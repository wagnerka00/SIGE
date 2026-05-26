from sqlalchemy import func

from app import db
from app.models.equipment import Equipment, EquipmentStatus


class EquipmentRepository:
    def _base_query(self, include_deleted: bool = False):
        query = Equipment.query
        if not include_deleted:
            query = query.filter_by(deleted=False)
        return query

    def find_by_id(self, equipment_id: str, include_deleted: bool = False) -> Equipment | None:
        return self._base_query(include_deleted).filter_by(id=equipment_id).first()

    def find_by_patrimonio(
        self, patrimonio: str, exclude_id: str | None = None
    ) -> Equipment | None:
        query = self._base_query()
        query = query.filter(func.lower(Equipment.patrimonio) == patrimonio.strip().lower())
        if exclude_id:
            query = query.filter(Equipment.id != exclude_id)
        return query.first()

    def list(
        self,
        page: int,
        per_page: int,
        search: str | None = None,
        status: str | None = None,
        tipo: str | None = None,
        localizacao: str | None = None,
    ):
        query = self._base_query()

        if search:
            term = f"%{search}%"
            query = query.filter(
                db.or_(
                    Equipment.patrimonio.ilike(term),
                    Equipment.nome.ilike(term),
                    Equipment.tipo.ilike(term),
                    Equipment.marca.ilike(term),
                    Equipment.modelo.ilike(term),
                    Equipment.numero_serie.ilike(term),
                    Equipment.localizacao.ilike(term),
                    Equipment.responsavel.ilike(term),
                )
            )
        if status:
            query = query.filter(Equipment.status == status)
        if tipo:
            query = query.filter(Equipment.tipo.ilike(f"%{tipo}%"))
        if localizacao:
            query = query.filter(Equipment.localizacao.ilike(f"%{localizacao}%"))

        pagination = query.order_by(Equipment.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        return pagination

    def create(self, equipment: Equipment) -> Equipment:
        db.session.add(equipment)
        db.session.commit()
        return equipment

    def update(self, equipment: Equipment) -> Equipment:
        db.session.commit()
        return equipment

    def soft_delete(self, equipment: Equipment) -> Equipment:
        equipment.deleted = True
        db.session.commit()
        return equipment

    def hard_delete(self, equipment: Equipment) -> None:
        db.session.delete(equipment)
        db.session.commit()

    def count_by_status(self) -> dict:
        rows = (
            self._base_query()
            .with_entities(Equipment.status, func.count(Equipment.id))
            .group_by(Equipment.status)
            .all()
        )
        result = {s: 0 for s in EquipmentStatus.ALL}
        for status, count in rows:
            result[status] = int(count)
        return result

    def count_by_localizacao(self) -> dict:
        rows = (
            self._base_query()
            .with_entities(Equipment.localizacao, func.count(Equipment.id))
            .group_by(Equipment.localizacao)
            .order_by(func.count(Equipment.id).desc())
            .all()
        )
        return {str(loc): int(count) for loc, count in rows}

    def count_total(self) -> int:
        return int(self._base_query().count())

