import os
import tempfile
import pytest
from app import app, db

@pytest.fixture
def client():
    db_fd, db_path = tempfile.mkstemp()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path

    with app.test_client() as client:
        with app.app_context():
            db.init_app(app)
            db.create_all()
        yield client

    os.close(db_fd)
    os.unlink(db_path)

def test_index(client):
    """Test the index page."""
    response = client.get('/')
    assert response.status_code == 200  # サーバーが200 OKステータスコードを返すか確認
    assert b"Together for" in response.data  # HTML内に特定のテキストが含まれているか確認

def test_register(client):
    """Test registering."""
    response = client.post('/register', data={'username': 'test', 'password': 'test', 'confirmation': 'test'})
    assert response.status_code == 200  # adjust according to your application's behavior

def test_login(client):
    """Test logging in."""
    response = client.post('/login', data={'username': 'test', 'password': 'test'})
    assert response.status_code == 200  # adjust according to your application's behavior

# More tests can be added as needed
