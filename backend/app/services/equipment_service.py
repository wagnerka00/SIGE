from datetime import datetime, timezone

from app.models.equipment import Equipment, EquipmentStatus
from app.repositories.equipment_repository import EquipmentRepository
from app.utils.errors import BadRequest, NotFound
from app.utils.validation import parse_pagination, require_fields, validate_status


class EquipmentService:
    REQUIRED_FIELDS = ("patrimonio", "nome", "tipo", "status", "localizacao")

    def __init__(self):
        self.repo = EquipmentRepository()

    def list_equipments(self, args: dict) -> dict:
        page, per_page = parse_pagination(
            args,
            default_page=1,
            default_per_page=10,
            max_per_page=100,
        )
        search = args.get("search")
        status = args.get("status")
        tipo = args.get("tipo")
        localizacao = args.get("localizacao")

        pagination = self.repo.list(
            page=page,
            per_page=per_page,
            search=search,
            status=status,
            tipo=tipo,
            localizacao=localizacao,
        )
        return {
            "items": [e.to_dict() for e in pagination.items],
            "pagination": {
                "page": pagination.page,
                "per_page": pagination.per_page,
                "total": pagination.total,
                "pages": pagination.pages,
            },
        }

    def get_equipment(self, equipment_id: str) -> dict:
        equipment = self.repo.find_by_id(equipment_id)
        if not equipment:
            raise NotFound("Equipamento não encontrado")
        return equipment.to_dict()

    def _validate_required(self, data: dict) -> None:
        missing = require_fields(data, list(self.REQUIRED_FIELDS))
        if missing:
            raise BadRequest(f"Campos obrigatórios: {', '.join(missing)}")

    def _validate_and_normalize(self, data: dict) -> dict:
        self._validate_required(data)
        status = validate_status(data.get("status"))

        normalized = {
            "patrimonio": str(data.get("patrimonio")).strip(),
            "nome": str(data.get("nome")).strip(),
            "tipo": str(data.get("tipo")).strip(),
            "marca": (data.get("marca") or "").strip() or None,
            "modelo": (data.get("modelo") or "").strip() or None,
            "numero_serie": (data.get("numero_serie") or "").strip() or None,
            "status": status,
            "localizacao": str(data.get("localizacao")).strip(),
            "responsavel": (data.get("responsavel") or "").strip() or None,
            "observacoes": (data.get("observacoes") or "").strip() or None,
        }
        if not normalized["patrimonio"]:
            raise BadRequest("Patrimônio é obrigatório")
        if not normalized["localizacao"]:
            raise BadRequest("Localização é obrigatória")
        return normalized

    def create_equipment(self, data: dict) -> dict:
        payload = self._validate_and_normalize(data)

        existing = self.repo.find_by_patrimonio(payload["patrimonio"])
        if existing:
            raise BadRequest("Número de patrimônio já cadastrado")

        equipment = Equipment(**payload)
        self.repo.create(equipment)
        return equipment.to_dict()

    def update_equipment(self, equipment_id: str, data: dict) -> dict:
        equipment = self.repo.find_by_id(equipment_id)
        if not equipment:
            raise NotFound("Equipamento não encontrado")

        # RN02: descartados não podem ser editados
        if equipment.status == EquipmentStatus.DESCARTADO:
            raise BadRequest("Equipamentos descartados não podem ser editados")

        updates = {}
        # Permite payload parcial, mas aplica validações quando campos existirem.
        if "patrimonio" in data and data["patrimonio"]:
            patrimonio = str(data.get("patrimonio")).strip()
            if patrimonio and patrimonio != equipment.patrimonio:
                existing = self.repo.find_by_patrimonio(patrimonio, exclude_id=equipment.id)
                if existing:
                    raise BadRequest("Número de patrimônio já cadastrado")
                updates["patrimonio"] = patrimonio
        if "nome" in data and data["nome"]:
            updates["nome"] = str(data.get("nome")).strip()
        if "tipo" in data and data["tipo"]:
            updates["tipo"] = str(data.get("tipo")).strip()
        if "status" in data and data.get("status"):
            updates["status"] = validate_status(data.get("status"))
        if "marca" in data:
            updates["marca"] = (data.get("marca") or "").strip() or None
        if "modelo" in data:
            updates["modelo"] = (data.get("modelo") or "").strip() or None
        if "numero_serie" in data:
            updates["numero_serie"] = (data.get("numero_serie") or "").strip() or None
        if "localizacao" in data and data.get("localizacao"):
            updates["localizacao"] = str(data.get("localizacao")).strip()
        if "responsavel" in data:
            updates["responsavel"] = (data.get("responsavel") or "").strip() or None
        if "observacoes" in data:
            updates["observacoes"] = (data.get("observacoes") or "").strip() or None

        # Atualiza campos.
        for k, v in updates.items():
            setattr(equipment, k, v)
        equipment.updated_at = datetime.now(timezone.utc)

        self.repo.update(equipment)
        return equipment.to_dict()

    def delete_equipment(self, equipment_id: str, hard: bool = False) -> dict:
        equipment = self.repo.find_by_id(equipment_id, include_deleted=True)
        if not equipment:
            raise NotFound("Equipamento não encontrado")

        if hard:
            self.repo.hard_delete(equipment)
        else:
            self.repo.soft_delete(equipment)

        return {"id": equipment_id, "hard_delete": hard}

    def get_dashboard_stats(self) -> dict:
        by_status = self.repo.count_by_status()
        by_localizacao = self.repo.count_by_localizacao()
        total = self.repo.count_total()
        return {
            "total": total,
            "em_manutencao": by_status.get(EquipmentStatus.EM_MANUTENCAO, 0),
            "disponiveis": by_status.get(EquipmentStatus.DISPONIVEL, 0),
            "reservados": by_status.get(EquipmentStatus.RESERVADO, 0),
            "em_uso": by_status.get(EquipmentStatus.EM_USO, 0),
            "descartados": by_status.get(EquipmentStatus.DESCARTADO, 0),
            "by_status": by_status,
            "by_localizacao": by_localizacao,
        }

