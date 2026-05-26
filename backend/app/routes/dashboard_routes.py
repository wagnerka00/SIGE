from flask import Blueprint

from app.controllers.dashboard_controller import DashboardController
from app.middlewares.auth_middleware import admin_required

dashboard_bp = Blueprint("dashboard", __name__)
controller = DashboardController()


@dashboard_bp.route("/stats", methods=["GET"])
@admin_required
def dashboard_stats():
    return controller.stats()

