import asyncio
import sys
from logging.config import fileConfig

from alembic import context
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

sys.path.append('../')

from src.common.model import MappedBase
from src.database.db import db

# Import all your models here so SQLAlchemy can discover them
from src.backend import *  # noqa: F403

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
alembic_config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if alembic_config.config_file_name is not None:
    fileConfig(alembic_config.config_file_name)

# model's MetaData object
# for 'autogenerate' support
target_metadata = MappedBase.metadata

# --- DIAGNOSTIC BLOCK START ---
# This block explicitly forces SQLAlchemy to configure all mappers.
# If the error still occurs here, it means the models are not being
# correctly registered with the shared MappedBase.metadata.
try:
    # Ensure all models are loaded and registered with the metadata
    # The imports above should handle this, but this explicitly triggers
    # the mapper configuration process.
    MappedBase.registry.configure()
    print("\n--- SQLAlchemy mappers configured successfully in env.py ---")
    print("Registered models:")
    for mapper in MappedBase.registry.mappers:
        print(f"  - {mapper.class_.__name__}")
    print("-----------------------------------------------------------\n")
except Exception as e:
    print(f"\n!!! ERROR during SQLAlchemy mapper configuration in env.py: {e} !!!\n")
    # Re-raise the exception to ensure the original error is still visible
    raise
# --- DIAGNOSTIC BLOCK END ---


# other values from the config, defined by the needs of env.py,
alembic_config.set_main_option('sqlalchemy.url', db.url.render_as_string(hide_password=False))

def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = alembic_config.get_main_option('sqlalchemy.url')
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={'paramstyle': 'named'},
        compare_type=True,
        compare_server_default=True,
        transaction_per_migration=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    def process_revision_directives(context, revision, directives):
        if alembic_config.cmd_opts.autogenerate:
            script = directives[0]
            if script.upgrade_ops.is_empty():
                directives[:] = []
                print('\nNo changes in model detected')

    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
        compare_server_default=True,
        transaction_per_migration=True,
        process_revision_directives=process_revision_directives,
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """In this scenario we need to create an Engine
    and associate a connection with the context.

    """

    connectable = async_engine_from_config(
        alembic_config.get_section(alembic_config.config_ini_section, {}),
        prefix='sqlalchemy.',
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
        
    await connectable.dispose()

def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    asyncio.run(run_async_migrations())

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()