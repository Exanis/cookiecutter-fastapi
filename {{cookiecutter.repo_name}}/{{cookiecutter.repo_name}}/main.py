"""
Main file for {{cookiecutter.repo_name}}.
This file is the entry point for the application.
"""

import logging
from typing import TYPE_CHECKING
from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware
from .routers import routers
from .settings import get_settings, get_database
from .tools import migrate
from . import __version__


if TYPE_CHECKING:
    from databases import Database
    from .settings import Settings


settings: 'Settings' = get_settings()
app = FastAPI(
    debug=settings.debug,
    title='{{cookiecutter.repo_name}}',
    description='{{cookiecutter.description}}',
    version=__version__,
    {% if cookiecutter.use_openapi == 'yes' %}
    openapi_url='/openapi.json',
    {% endif %}
    {% if cookiecutter.use_docs == 'yes' %}
    docs_url='/docs',
    {% endif %}
    {% if cookiecutter.use_redoc == 'yes' %}
    redoc_url='/redoc',
    {% endif %}
)

for router in routers:
    app.include_router(router)

app.add_middleware(GZipMiddleware, minimum_size=1000)

@app.on_event('startup')
async def startup():
    """
    Startup event.
    """
    logging.basicConfig(level=logging.DEBUG if settings.debug else logging.WARNING)
    logging.info('Starting up...')
    database: 'Database' = get_database()
    await database.connect()
    await migrate(database)

@app.on_event('shutdown')
async def shutdown():
    """
    Shutdown event.
    """
    logging.info('Shutting down...')
    database: 'Database' = get_database()
    await database.disconnect()