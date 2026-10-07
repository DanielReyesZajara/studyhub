"""Espera hasta 60 segundos a la base configurada, sin imprimir credenciales."""
import time
from app import create_app
from app.extensions import db
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

app = create_app()
for attempt in range(30):
    with app.app_context():
        try:
            db.session.execute(text('SELECT 1'))
            print('Base de datos disponible.')
            break
        except SQLAlchemyError:
            db.session.rollback()
    time.sleep(2)
else:
    raise SystemExit('La base de datos no respondió en 60 segundos.')
