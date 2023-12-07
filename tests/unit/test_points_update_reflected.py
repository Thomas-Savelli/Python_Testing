import pytest
from flask.testing import FlaskClient
from server import app, loadClubs, loadCompetitions


class TestPointsUpdateReflected():

    @pytest.fixture
    def client(self):
        return app.test_client()

    @pytest.fixture
    def competitions_and_clubs(self):
        competitions = loadCompetitions()
        clubs = loadClubs()
        return competitions, clubs

    @pytest.fixture
    def mock_purchase_places(self, monkeypatch):
        def _mock_purchase_places(competition, club, places_required):
            if places_required <= int(club['points']):
                # L'utilisateur a suffisamment de points, effectue l'achat
                club['points'] = str(int(club['points']) - places_required)
                competition['numberOfPlaces'] = str(int(competition['numberOfPlaces']) - places_required)

        monkeypatch.setattr("server.purchasePlaces", _mock_purchase_places)
        return _mock_purchase_places

    def _perform_purchase(self, client, competition, club, places_to_purchase):
        return client.post('/purchasePlaces', data={
            'competition': competition['name'],
            'club': club['name'],
            'places': places_to_purchase
        })

    def test_points_update_reflected_success(self, competitions_and_clubs, mock_purchase_places):
        # Cas où l'achat de places réussit
        competitions, clubs = competitions_and_clubs
        club = clubs[0]
        competition = competitions[0]
        initial_points = int(club['points'])
        initial_places = int(competition['numberOfPlaces'])

        places_to_purchase = 5

        expected_club_points = initial_points - places_to_purchase
        expected_competition_places = initial_places - places_to_purchase

        # Appel simulé à purchasePlaces en utilisant le monkeypatch
        mock_purchase_places(competition=competition, club=club, places_required=places_to_purchase)

        assert club['points'] == str(expected_club_points)
        assert competition['numberOfPlaces'] == str(expected_competition_places)

    def test_insufficient_points_update_shouldnt_update_data(self, competitions_and_clubs,
                                                             client, mock_purchase_places):
        # Cas où l'utilisateur n'a pas assez de points pour acheter les places
        competitions, clubs = competitions_and_clubs
        club = clubs[0]
        competition = competitions[0]
        initial_places = int(competition['numberOfPlaces'])
        initial_points = int(club['points'])

        # Tentative d'achat de places avec plus de points que l'utilisateur n'en a
        places_to_purchase = initial_points + 1

        mock_purchase_places(competition=competition, club=club, places_required=places_to_purchase)

        # Appel à la fonction ou à la méthode qui effectue la requête
        _ = self._perform_purchase(client, competition, club, places_to_purchase)

        # S'assure que le nombre de places n'a pas changé
        assert int(competition['numberOfPlaces']) == initial_places

        # S'assure que le nombre de points du club n'a pas changé
        assert int(club['points']) == initial_points
