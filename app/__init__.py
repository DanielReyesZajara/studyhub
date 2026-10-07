"""Factoría de la aplicación; los imports se retrasan para aislar las unitarias."""
import os
from pathlib import Path


def create_app(test_config=None):
    from dotenv import load_dotenv
    from flask import Flask
    from sqlalchemy import URL
    from .extensions import db, migrate

    root = Path(__file__).resolve().parent.parent
    load_dotenv(root / '.env')
    app = Flask(__name__, instance_relative_config=True)
    if os.getenv('DATABASE_URL'):
        uri = os.environ['DATABASE_URL']
    elif os.getenv('MARIADB_HOST'):
        uri = URL.create(
            'mysql+pymysql', username=os.getenv('MARIADB_USER', 'studyhub'),
            password=os.getenv('MARIADB_PASSWORD', 'studyhub_local'),
            host=os.environ['MARIADB_HOST'], port=3306,
            database=os.getenv('MARIADB_DATABASE', 'studyhub'),
        )
    else:
        uri = 'sqlite:///studyhub.db'
    app.config.from_mapping(
        SECRET_KEY=os.getenv('SECRET_KEY', 'studyhub_local_development'),
        SQLALCHEMY_DATABASE_URI=uri,
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SQLALCHEMY_ENGINE_OPTIONS={'pool_pre_ping': True},
        DEBUG=os.getenv('FLASK_DEBUG', '0') == '1',
    )
    if test_config:
        app.config.update(test_config)
    Path(app.instance_path).mkdir(parents=True, exist_ok=True)
    db.init_app(app)
    migrate.init_app(app, db, directory=str(root / 'migrations'))
    from . import models
    from .routes import bp
    app.register_blueprint(bp)
    return app
