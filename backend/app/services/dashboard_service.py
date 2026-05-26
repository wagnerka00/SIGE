from app.services.equipment_service import EquipmentService


class DashboardService:
    def __init__(self):
        self.equipment_service = EquipmentService()

    def stats(self) -> dict:
        return self.equipment_service.get_dashboard_stats()

