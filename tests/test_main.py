import requests

api_url = 'http://localhost:8000'

def test_healthcheck():
    response = requests.get(f'{api_url}/__health')
    assert response.status_code == 200

class TestAuthor():
    def test_get_empty_auth(self):
        response = requests.get(f'{api_url}/v1/auth')
        assert response.status_code == 200
        assert len(response.json()) == 0

    def test_add_author(self):
        body = { "title": "New author", "body": "genre" }
        response = requests.post(f'{api_url}/v1/auth', json = body)
        assert response.status_code == 200
        assert response.json().get('title') == 'New author'
        assert response.json().get('body') == 'genre'
        assert response.json().get('id') == 0

    def get_auth_by_id(self):
        response = requests.get(f'{api_url}/v1/auth/0')
        assert response.status_code == 200
        assert response.json().get('title') == 'New author'
        assert response.json().get('genre') == 'genre'
        assert response.json().get('id') == 0

    def test_get_not_empty_author(self):
        response = requests.get(f'{api_url}/v1/auth')
        assert response.status_code == 200
        assert len(response.json()) == 1