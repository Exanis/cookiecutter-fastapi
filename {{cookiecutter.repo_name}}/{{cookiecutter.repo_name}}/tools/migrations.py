"""
Tool used to migrate the database. Unlike some other tools (like Alembic),
this is not meant to be able to rollback migrations. It is meant to be
used to install migrations on a fresh database, or to install migrations
on an existing database that is missing some migrations.
"""

from os import listdir, path
from logging import info, debug
from typing import TYPE_CHECKING
from asyncpg.exceptions import UndefinedTableError


if TYPE_CHECKING:
    from databases import Database


async def _run_one_migration(filename: str, database: 'Database'):
    """
    Run a single migration.
    """
    with open(path.join('migrations', filename), 'r') as fp:
        migration = fp.read()
    for request in migration.split(';'):
        proper_query = request.strip()
        if proper_query:
            debug(f'Migration query: {proper_query}')
            await database.execute(request)
    query = 'INSERT INTO "migrations" ("filename") VALUES (:filename)'
    await database.execute(
        query,
        {
            'filename': filename
        }
    )


async def migrate(database: 'Database'):
    """
    Apply all migrations to the database.
    """
    query = 'SELECT "filename" FROM "migrations"'
    try:
        result = await database.fetch_all(query)
        existing = [row['filename'] for row in result]
    except UndefinedTableError:
        # Table does not exist, so there is no pre-existing migrations (first run)
        existing = []
    migrations = [
        filename for filename in listdir('migrations')
        if path.isfile(path.join('migrations', filename))
        and filename not in existing
    ]
    migrations.sort()
    for file in migrations:
        info(f'Installing migration {file}...')
        await _run_one_migration(file, database)
        info(f'Installation done.')
