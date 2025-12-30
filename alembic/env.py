import os
import sys

# CRÍTICO: Limpiar variables de entorno problemáticas ANTES de cualquier import
# Estas variables pueden tener encoding incorrecto en Windows
vars_to_clear = [
    'PGCLIENTENCODING', 'PGSSLMODE', 'PGSSLCERT', 'PGSSLKEY',
    'PGSSLROOTCERT', 'PGPASSFILE', 'PGSERVICEFILE', 'PGOPTIONS',
    'PGAPPNAME', 'CURL_CA_BUNDLE', 'SSL_CERT_FILE'
]

for var in vars_to_clear:
    os.environ.pop(var, None)

# Configurar encoding explícitamente
os.environ['LANG'] = 'en_US.UTF-8'
os.environ['LC_ALL'] = 'en_US.UTF-8'
os.environ['PYTHONIOENCODING'] = 'utf-8'

from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.core.config import get_settings
from app.db.session import Base
from app.models import user, task  # Import all models

# this is the Alembic Config object
config = context.config

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Get settings and set sqlalchemy.url
settings = get_settings()
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

# Add your model's MetaData object here for 'autogenerate' support
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    
    # Configuración con opciones de encoding explícitas
    configuration = config.get_section(config.config_ini_section, {})
    
    # Agregar connect_args para forzar UTF-8
    configuration['connect_args'] = {
        'options': '-c client_encoding=UTF8',
        'client_encoding': 'utf8'
    }
    
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
