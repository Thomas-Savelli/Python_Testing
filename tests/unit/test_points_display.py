import pytest

from server import app, loadClubs


class TestPointsDisplayBoard:
    @pytest.fixture
    def client(self):
        app.config['TESTING'] = True
        client = app.test_client()
        yield client

    def test_loadClubs(self):
        clubs = loadClubs()
        assert clubs is not None
        assert isinstance(clubs, list)
        assert len(clubs) >= 0

    def test_points_display_board_not_logged_in(self, client):
        response = client.get('/pointsDisplay')
        assert response.status_code == 200
        assert b'Points Display Board' in response.data

    def test_points_display_board_logged_in(self, mocker, client):
        # Mock de la liste de clubs pour ajouter un club avec l'email test@test.com
        mocker.patch('server.clubs', [{'name': 'Test Name', 'email': 'test@test.com', 'points': 10}])

        # Simule la connexion avec l'email fictif
        response_login = client.post('/showSummary', data={'name': 'Test Name', 'email': 'test@test.com'})
        assert response_login.status_code == 200

        # Accéde correctement à la page pointsDisplay
        response_display = client.get('/pointsDisplay')
        assert response_display.status_code == 200
        assert b'Points Display Board' in response_display.data

    def test_points_display_board_empty_clubs(self, mocker, client):
        # Mock de la liste de clubs vide
        mocker.patch('server.clubs', [])

        # Accède correctement à la page pointsDisplay
        response_display = client.get('/pointsDisplay')
        assert response_display.status_code == 200
        assert b'Points Display Board' in response_display.data
