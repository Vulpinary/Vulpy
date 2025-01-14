import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

from alembic import context

# Добавьте путь к вашему проекту в sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Импортируйте вашу модель
from app.models import Base  # Убедитесь, что этот импорт работает

target_metadata = Base.metadata



# Определение функции для работы с миграциями
def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = context.config.get_main_option("sqlalchemy.url")
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
    configuration = context.config.get_section(context.config.config_ini_section)
    url = configuration['sqlalchemy.url']
    connectable = create_engine(url, echo=True)

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()