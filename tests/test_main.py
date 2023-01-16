import requests

api_url = 'http://localhost:8001'

def test_healthcheck():
    response = requests.get(f'{api_url}/__health')
    assert response.status_code == 200

class TestAuthors():
    def test_get_empty_authors(self):
        response = requests.get(f'{api_url}/v1/auth')
        assert response.status_code == 200
        assert len(response.json()) == 0

    def test_create_authors(self):
        body = { "nickname": "nickname", "genre": "genre" }
        response = requests.post(f'{api_url}/v1/auth', json = body)
        assert response.status_code == 200
        assert response.json().get('nickname') == 'nickname'
        assert response.json().get('genre') == 'genre'
        assert response.json().get('id') == 0

    def test_get_authors_by_id(self):
        response = requests.get(f'{api_url}/v1/auth/0')
        assert response.status_code == 200
        assert response.json().get('nickname') == 'nickname'
        assert response.json().get('genre') == 'genre'
        assert response.json().get('id') == 0

    def test_get_not_empty_authors():
        response = requests.get(f'{api_url}/v1/auth')
        assert response.status_code == 200
        assert len(response.json()) == 1