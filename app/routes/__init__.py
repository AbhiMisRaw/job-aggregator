from .job_routes import routes as job_routes
from .user_routes import routes as user_routes
from .health_routes import routes as health_routes
from .company_career_routes import routes as career_page_routes
from .job_desc_routes import routes as job_desc_routes

__all__ = [
    "career_page_routes",
    "health_routes",
    "job_routes",
    "job_desc_routes",
    "user_routes",
]