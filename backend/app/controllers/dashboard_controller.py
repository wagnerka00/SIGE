from app.services.dashboard_service import DashboardService
from app.utils.api_response import success


class DashboardController:
    def __init__(self):
        self.service = DashboardService()

    def stats(self):
        return success(self.service.stats(), "Dashboard carregado com sucesso", status=200)

