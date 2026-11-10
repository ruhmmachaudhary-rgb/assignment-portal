import pytest
from app import app, submissions

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_complete_and_valid_submission(client):
    submissions.clear()
    response = client.post('/submit', data={
        'name': 'Ali Khan',
        'reg_no': 'BC2102001',
        'title': 'DevOps Lab 1',
        'url': 'https://github.com/ali/repo'
    })
    assert response.status_code == 200
    assert b"Assignment submitted successfully!" in response.data
    assert len(submissions) == 1

def test_missing_registration_number(client):
    submissions.clear()
    response = client.post('/submit', data={
        'name': 'Ali Khan',
        'reg_no': '',
        'title': 'DevOps Lab 1',
        'url': 'https://github.com/ali/repo'
    })
    assert response.status_code == 400
    assert b"Registration number is missing!" in response.data
    assert len(submissions) == 0

def test_invalid_submission_url(client):
    submissions.clear()
    response = client.post('/submit', data={
        'name': 'Ali Khan',
        'reg_no': 'BC2102001',
        'title': 'DevOps Lab 1',
        'url': 'ftp://invalid-url.com'
    })
    assert response.status_code == 400
    assert b"Invalid submission URL!" in response.data
    assert len(submissions) == 0