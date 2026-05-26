"""
Seed inicial do SIGE UFPI.

Cria tabelas (db.create_all) e insere usuários e equipamentos de exemplo
quando o banco estiver vazio.
"""

from app import create_app, db, bcrypt
from app.models.equipment import Equipment, EquipmentStatus
from app.models.user import User, UserRole


def seed():
    app = create_app()
    with app.app_context():
        db.create_all()

        if User.query.first():
            print("Banco já possui usuários. Seed ignorado.")
            return

        users = [
            User(
                name="Administrador SIGE",
                email="admin@ufpi.edu.br",
                password_hash=bcrypt.generate_password_hash("admin123").decode(
                    "utf-8"
                ),
                role=UserRole.ADMIN,
                active=True,
            ),
            User(
                name="Técnico de Informática",
                email="tecnico@ufpi.edu.br",
                password_hash=bcrypt.generate_password_hash("tecnico123").decode(
                    "utf-8"
                ),
                role=UserRole.TECNICO,
                active=True,
            ),
            User(
                name="Visitante Consulta",
                email="visitante@ufpi.edu.br",
                password_hash=bcrypt.generate_password_hash("visitante123").decode(
                    "utf-8"
                ),
                role=UserRole.VISITANTE,
                active=True,
            ),
        ]
        db.session.add_all(users)
        db.session.commit()

        equipments = [
            Equipment(
                patrimonio="UFPI-2024-001",
                nome="Desktop Dell OptiPlex",
                tipo="Computador",
                marca="Dell",
                modelo="OptiPlex 7090",
                numero_serie="DL7090-001",
                status=EquipmentStatus.DISPONIVEL,
                localizacao="Lab. Informática - CCNT",
                responsavel="João Silva",
                observacoes="Equipamento novo, em perfeito estado.",
            ),
            Equipment(
                patrimonio="UFPI-2024-002",
                nome="Notebook Lenovo ThinkPad",
                tipo="Notebook",
                marca="Lenovo",
                modelo="ThinkPad E14",
                numero_serie="LN-E14-002",
                status=EquipmentStatus.EM_USO,
                localizacao="Secretaria - Reitoria",
                responsavel="Maria Santos",
            ),
            Equipment(
                patrimonio="UFPI-2024-003",
                nome="Impressora HP LaserJet",
                tipo="Impressora",
                marca="HP",
                modelo="LaserJet Pro M404",
                numero_serie="HP-M404-003",
                status=EquipmentStatus.EM_MANUTENCAO,
                localizacao="Setor Administrativo - CCS",
                responsavel="Carlos Oliveira",
                observacoes="Aguardando peça de reposição.",
            ),
            Equipment(
                patrimonio="UFPI-2024-004",
                nome="Projetor Epson",
                tipo="Projetor",
                marca="Epson",
                modelo="PowerLite X49",
                numero_serie="EP-X49-004",
                status=EquipmentStatus.RESERVADO,
                localizacao="Sala 12 - Bloco A",
                responsavel="Ana Costa",
            ),
            Equipment(
                patrimonio="UFPI-2024-005",
                nome="Monitor Samsung 24",
                tipo="Monitor",
                marca="Samsung",
                modelo="F24T450",
                numero_serie="SM-F24-005",
                status=EquipmentStatus.DESCARTADO,
                localizacao="Almoxarifado TI",
                responsavel="TI UFPI",
                observacoes="Equipamento obsoleto, descartado conforme laudo.",
            ),
            Equipment(
                patrimonio="UFPI-2024-006",
                nome="Switch Cisco 24 portas",
                tipo="Rede",
                marca="Cisco",
                modelo="CBS250-24T",
                numero_serie="CS-250-006",
                status=EquipmentStatus.DISPONIVEL,
                localizacao="Lab. Redes - CCNT",
                responsavel="Pedro Lima",
            ),
        ]
        db.session.add_all(equipments)
        db.session.commit()

        print("Seed concluído com sucesso!")
        print("Usuários de teste:")
        print("  admin@ufpi.edu.br / admin123 (administrador)")
        print("  tecnico@ufpi.edu.br / tecnico123 (tecnico)")
        print("  visitante@ufpi.edu.br / visitante123 (visitante)")


if __name__ == "__main__":
    seed()

