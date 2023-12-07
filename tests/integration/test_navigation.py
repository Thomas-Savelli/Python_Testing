import pytest
from server import app, loadClubs, loadCompetitions


class TestNavigation():
    @pytest.fixture
    def client(self):
        return app.test_client()

    def test_page_navigation(self, client):
        clubs = loadClubs()
        competitions = loadCompetitions()
        club = clubs[0]
        competition = competitions[0]

        # Soumet des requêtes pour accéder à différentes pages
        response1 = client.get('/')
        response2 = client.get('/pointsDisplay')
        response3 = client.post('showSummary', data=club, follow_redirects=True)
        response4 = client.get(f'/book/{competition["name"]}/{club["name"]}')
        response5 = client.post('/purchasePlaces', data={
                                'club': club['name'],
                                'competition': competition['name'],
                                'places': 1
                                })
        response6 = client.get('/logout')

        assert response1.status_code == 200
        assert response2.status_code == 200
        assert response3.status_code == 200
        assert response4.status_code == 200
        assert response5.status_code == 200
        assert response6.status_code == 200

    def test_navigation_links(self, client):
        clubs = loadClubs()
        competitions = loadCompetitions()
        club = clubs[0]
        competition = competitions[0]

        # Soumet des requêtes pour accéder à différentes pages
        response1 = client.get('/')
        response2 = client.get('/pointsDisplay')
        response3 = client.post('showSummary', data=club, follow_redirects=True)
        response4 = client.get(f'/book/{competition["name"]}/{club["name"]}')
        response5 = client.post('/purchasePlaces', data={
                                'club': club['name'],
                                'competition': competition['name'],
                                'places': 1
                                })
        response6 = client.get('/logout')

        assert b"Welcome to the GUDLFT Registration Portal!" in response1.data

        for current_club in clubs:
            assert current_club['name'].encode(), current_club['points'].encode() in response2.data

        assert b"Welcome," in response3.data
        assert competition['name'].encode(), competition['numberOfPlaces'].encode() in response4.data
        assert b'Welcome,', b'Great-booking complete!' in response5.data
        assert b'GUDLFT Registration' in response6.data
