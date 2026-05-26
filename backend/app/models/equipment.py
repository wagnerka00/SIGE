import uuid
from datetime import datetime, timezone

from app import db


class EquipmentStatus:
    DISPONIVEL = "disponivel"
    EM_USO = "em_uso"
    EM_MANUTENCAO = "em_manutencao"
    DESCARTADO = "descartado"
    RESERVADO = "reservado"

    ALL = (DISPONIVEL, EM_USO, EM_MANUTENCAO, DESCARTADO, RESERVADO)

    LABELS = {
        DISPONIVEL: "Disponível",
        EM_USO: "Em uso",
        EM_MANUTENCAO: "Em manutenção",
        DESCARTADO: "Descartado",
        RESERVADO: "Reservado",
    }


class Equipment(db.Model):
    __tablename__ = "equipments"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    patrimonio = db.Column(db.String(50), unique=True, nullable=False, index=True)
    nome = db.Column(db.String(150), nullable=False)
    tipo = db.Column(db.String(80), nullable=False)
    marca = db.Column(db.String(80), nullable=True)
    modelo = db.Column(db.String(80), nullable=True)
    numero_serie = db.Column(db.String(80), nullable=True)

    status = db.Column(db.String(30), nullable=False, default=EquipmentStatus.DISPONIVEL)
    localizacao = db.Column(db.String(150), nullable=False)
    responsavel = db.Column(db.String(120), nullable=True)
    observacoes = db.Column(db.Text, nullable=True)

    deleted = db.Column(db.Boolean, default=False, nullable=False)

    created_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    updated_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "patrimonio": self.patrimonio,
            "nome": self.nome,
            "tipo": self.tipo,
            "marca": self.marca,
            "modelo": self.modelo,
            "numero_serie": self.numero_serie,
            "status": self.status,
            "status_label": EquipmentStatus.LABELS.get(self.status, self.status),
            "localizacao": self.localizacao,
            "responsavel": self.responsavel,
            "observacoes": self.observacoes,
            "deleted": self.deleted,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

