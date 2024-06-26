from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
from urllib.parse import urlparse

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
from fastagi.models.base_model import DBBaseModel
target_metadata = DBBaseModel.metadata
from fastagi.models import *
from fastagi.config.config import get_config

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

db_host = get_config('DB_HOST', 'fast__postgres')
db_username = get_config('DB_USERNAME')
db_password = get_config('DB_PASSWORD')
db_name = get_config('DB_NAME')
database_url = get_config('DB_URL', None)

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """

    db_url = database_url
    if db_url is None:
        if db_username is None:
            db_url = f'postgresql://{db_host}/{db_name}'
        else:
            db_url = f'postgresql://{db_username}:{db_password}@{db_host}/{db_name}'
    else:
        db_url = urlparse(db_url)
        db_url = db_url.scheme + "://" + db_url.netloc + db_url.path

    config.set_main_option("sqlalchemy.url", db_url)

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
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """

    db_host = get_config('DB_HOST', 'fast__postgres')
    db_username = get_config('DB_USERNAME')
    db_password = get_config('DB_PASSWORD')
    db_name = get_config('DB_NAME')
    db_url = get_config('DB_URL', None)

    if db_url is None:
        if db_username is None:
            db_url = f'postgresql://{db_host}/{db_name}'
        else:
            db_url = f'postgresql://{db_username}:{db_password}@{db_host}/{db_name}'
    else:
        db_url = urlparse(db_url)
        db_url = db_url.scheme + "://" + db_url.netloc + db_url.path
        
    config.set_main_option('sqlalchemy.url', db_url)
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
