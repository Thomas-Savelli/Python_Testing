import pytest
from server import app, loadClubs, loadCompetitions


class TestReservationPlaces():
    @pytest.fixture
    def client(self):
        return app.test_client()

    def test_select_competition_for_purchase(self, client):
        clubs = loadClubs()
        club = clubs[0]
        response = client.post('/showSummary', data=club, follow_redirects=True)
        assert response.status_code == 200
        assert b"Welcome," in response.data

        # Sélectionne une compétition pour l'achat de places.
        competitions = loadCompetitions()
        competition = competitions[0]
        response = client.get(f'/book/{competition["name"]}/{club["name"]}')
        assert response.status_code == 200
        assert competition['name'].encode() in response.data
        assert b'Places available:' in response.data

        # Déconnection
        response = client.get('/logout')
        assert b"GUDLFT Registration" in response.data

    def test_select_competition_past_for_purchase(self, client):
        clubs = loadClubs()
        club = clubs[0]
        response = client.post('/showSummary', data=club, follow_redirects=True)

        assert response.status_code == 200
        assert b"Welcome," in response.data

        # Sélectionne une compétition passée pour l'achat de places.
        competitions = loadCompetitions()
        competition = competitions[1]
        response = client.get(f'/book/{competition["name"]}/{club["name"]}')
        assert b"Welcome," in response.data
        assert b"You can&#39;t book places for a past competition." in response.data

        # Déconnection
        response = client.get('/logout')
        assert b"GUDLFT Registration" in response.data

    def test_purchase_places_success(self, client):
        clubs = loadClubs()
        competitions = loadCompetitions()

        # Sélectionne un club et une compétition pour le test
        club = clubs[0]
        competition = competitions[0]

        # S'identifie avec son email
        response = client.post('/showSummary', data=club, follow_redirects=True)

        assert response.status_code == 200
        assert b"Welcome," in response.data

        # Sélectionne une compétition valide pour l'achat de places.
        response = client.get(f'/book/{competition["name"]}/{club["name"]}')

        assert response.status_code == 200
        assert competition['name'].encode() in response.data
        assert b'Places available:' in response.data

        # Stock l'état initial des points et places
        initial_points = int(club['points'])
        initial_places = int(competition['numberOfPlaces'])

        # Soumet le formulaire purchasePlaces avec des données valides
        response = client.post('/purchasePlaces', data={
            'club': club['name'],
            'competition': competition['name'],
            'places': 2
        })

        # Simule la mise à jour des données
        club_index = next((i for i, c in enumerate(clubs) if c['name'] == club['name']), None)
        competitions_index = next((i for i, c in enumerate(competitions) if c['name'] == competition['name']), None)

        if club_index is not None and competitions_index is not None:
            # Met à jour les points du club
            clubs[club_index]['points'] = str(initial_points - 2)
            # Met à jour le nombre de places pour la compétition
            competitions[competitions_index]['numberOfPlaces'] = str(initial_places - 2)

        assert response.status_code == 200
        assert b'Welcome,' in response.data
        assert b'Great-booking complete!' in response.data
        assert int(club['points']) == initial_points - 2
        assert int(competition['numberOfPlaces']) == initial_places - 2

        # Déconnection
        response = client.get('/logout')
        assert b"GUDLFT Registration" in response.data

    def test_purchase_places_insufficient_seats(self, client):
        clubs = loadClubs()
        competitions = loadCompetitions()

        # Sélectionne un club et une compétition pour le test
        club = clubs[0]
        competition = competitions[3]

        # S'identifie avec son email
        response = client.post('/showSummary', data=club, follow_redirects=True)

        assert response.status_code == 200
        assert b"Welcome," in response.data

        # Sélectionne une compétition valide pour l'achat de places.
        response = client.get(f'/book/{competition["name"]}/{club["name"]}')

        assert response.status_code == 200
        assert competition['name'].encode() in response.data
        assert competition['numberOfPlaces'].encode() in response.data

        # Stock l'état initial des points et places
        initial_points = int(club['points'])
        initial_places = int(competition['numberOfPlaces'])

        # Soumet le formulaire purchasePlaces avec des données valides
        response = client.post('/purchasePlaces', data={
            'club': club['name'],
            'competition': competition['name'],
            'places': 6
        })

        assert competition['name'].encode() in response.data
        assert b'Not enough places available for booking.' in response.data
        assert int(club['points']) == initial_points
        assert int(competition['numberOfPlaces']) == initial_places

        # Déconnection
        response = client.get('/logout')
        assert b"GUDLFT Registration" in response.data

    def test_purchase_places_more_than_12_places(self, client):
        clubs = loadClubs()
        competitions = loadCompetitions()

        # Sélectionne un club et une compétition pour le test
        club = clubs[0]
        competition = competitions[0]

        # S'identifie avec son email
        response = client.post('/showSummary', data=club, follow_redirects=True)

        assert response.status_code == 200
        assert b"Welcome," in response.data

        # Sélectionne une compétition valide pour l'achat de places.
        response = client.get(f'/book/{competition["name"]}/{club["name"]}')

        assert response.status_code == 200
        assert competition['name'].encode() in response.data

        # Stock l'état initial des points et places
        initial_points = int(club['points']) - 17
        initial_places = int(competition['numberOfPlaces'])

        # Soumet le formulaire purchasePlaces avec des données valides
        response = client.post('/purchasePlaces', data={
            'club': club['name'],
            'competition': competition['name'],
            'places': 20
        })

        assert competition['name'].encode() in response.data
        assert b'You can&#39;t book more than 12 places for a competition.' in response.data
        assert int(club['points']) - 17 == initial_points
        assert int(competition['numberOfPlaces']) == initial_places

        # Déconnection
        response = client.get('/logout')
        assert b"GUDLFT Registration" in response.data

    def test_purchase_places_insufficient_points(self, client):
        clubs = loadClubs()
        competitions = loadCompetitions()

        # Sélectionne un club et une compétition pour le test
        club = clubs[1]
        competition = competitions[0]

        # S'identifie avec son email
        response = client.post('/showSummary', data=club, follow_redirects=True)

        assert response.status_code == 200
        assert b"Welcome," in response.data

        # Sélectionne une compétition valide pour l'achat de places.
        response = client.get(f'/book/{competition["name"]}/{club["name"]}')

        assert response.status_code == 200
        assert competition['name'].encode() in response.data

        # Stock l'état initial des points et places
        initial_points = int(club['points'])
        initial_places = int(competition['numberOfPlaces'])

        # Soumet le formulaire purchasePlaces avec des données valides
        response = client.post('/purchasePlaces', data={
            'club': club['name'],
            'competition': competition['name'],
            'places': 5
        })

        assert competition['name'].encode() in response.data
        assert b'Not enough points to make the booking.' in response.data
        assert int(club['points']) == initial_points
        assert int(competition['numberOfPlaces']) == initial_places

        # Déconnection
        response = client.get('/logout')
        assert b"GUDLFT Registration" in response.data
