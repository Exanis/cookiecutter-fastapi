"""
This module contains the routers for the application.
"""

from .healthcheck import router as healthcheck_router

routers = [
    healthcheck_router,
]
