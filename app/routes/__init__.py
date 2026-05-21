from .job_routes import routes as job_routes
from .user_routes import routes as user_routes
from .health_routes import routes as health_routes

__all__ = [
    "health_routes",
    "job_routes",
    "user_routes",
]