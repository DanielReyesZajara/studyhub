import os
import pytest
from app import create_app
from app.extensions import db
from sqlalchemy.engine import make_url


@pytest.fixture
def app(tmp_path):
    uri = os.getenv('TEST_DATABASE_URL', 'sqlite:///' + str(tmp_path / 'test.db'))
    url = make_url(uri)
    if url.get_backend_name() != 'sqlite' and not (url.database or '').endswith('_test'):
        raise ValueError('Usa una base exclusiva de pruebas cuyo nombre termine en _test.')
    application = create_app({'TESTING': True, 'DEBUG': False,
                              'SQLALCHEMY_DATABASE_URI': uri})
    with application.app_context():
        db.create_all()
        yield application
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()
