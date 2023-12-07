import pytest
from server import app, loadClubs


class TestPointsDisplayBoard():
    @pytest.fixture
    def client(self):
        return app.test_client()

    def test_offline_points_display(self, client):
        clubs = loadClubs()

        response = client.get('/pointsDisplay')

        assert response.status_code == 200
        assert b"Club" in response.data
        assert b"Points" in response.data

        for club in clubs:
            assert club['name'].encode() in response.data
            assert club['points'].encode() in response.data

    def test_online_points_display(self, client):
        clubs = loadClubs()
        club = clubs[0]
        response = client.post('showSummary', data=club, follow_redirects=True)
        assert response.status_code == 200
        assert b"Welcome," in response.data

        response = client.get('/pointsDisplay', follow_redirects=True)
        assert response.status_code == 200
        assert b"Club" in response.data
        assert b"Points" in response.data

        for club in clubs:
            assert club['name'].encode() in response.data
            assert club['points'].encode() in response.data

        response = client.get('/logout', follow_redirects=True)
        assert b"GUDLFT Registration" in response.data
