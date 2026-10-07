from logging.config import fileConfig
from alembic import context
from flask import current_app

config = context.config
if config.config_file_name:
    fileConfig(config.config_file_name)
target_db = current_app.extensions['migrate'].db
target_metadata = target_db.metadata


def run_migrations_offline():
    url = str(target_db.engine.url.render_as_string(hide_password=False))
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    with target_db.engine.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata,
                          **current_app.extensions['migrate'].configure_args)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
