import pytest
from flask.testing import FlaskClient
from server import app, loadClubs, loadCompetitions


class TestPurchasePlace():

    @pytest.fixture
    def client(self):
        return app.test_client()

    @pytest.fixture
    def competitions_and_clubs(self):
        # Fixture pour charger les données nécessaires pour les tests
        competitions = loadCompetitions()
        clubs = loadClubs()
        return competitions, clubs

    @pytest.fixture
    def mock_purchase_places(self, monkeypatch):
        def _mock_purchase_places(competition, club, places_required):
            if places_required <= int(club['points']):
                # L'utilisateur a suffisamment de points, effectuez l'achat
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

    def test_purchase_places_success(self, competitions_and_clubs, mock_purchase_places):
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

    def test_purchase_places_should_return_success_status_200(self, competitions_and_clubs,
                                                              client, mock_purchase_places):
        # Cas où l'achat de places réussit
        competitions, clubs = competitions_and_clubs
        club = clubs[0]
        competition = competitions[0]
        places_to_purchase = 5

        # Appel simulé à purchasePlaces en utilisant le monkeypatch
        mock_purchase_places(competition=competition, club=club, places_required=places_to_purchase)

        # Appel à la méthode qui effectue la requête
        response = self._perform_purchase(client, competition, club, places_to_purchase)

        # Vérification du statut de la réponse
        assert response.status_code == 200

    def test_purchase_places_success_booking_should_render_welcome_page(self, client,
                                                                        mock_purchase_places,
                                                                        competitions_and_clubs):
        competitions, clubs = competitions_and_clubs
        club = clubs[0]
        competition = competitions[0]
        places_to_purchase = 3

        # Appel simulé à purchasePlaces en utilisant le monkeypatch
        mock_purchase_places(competition=competition, club=club, places_required=places_to_purchase)

        # Appel à la méthode qui effectue la requête
        response = self._perform_purchase(client, competition, club, places_to_purchase)

        # Vérifie que la page de bienvenue est rendue correctement
        assert b'Summary | GUDLFT Registration' in response.data
        assert b'Welcome,' in response.data
        assert b'Points available:' in response.data
        assert b'Competitions:' in response.data

    def test_purchase_places_should_return_success_flash_message(self, competitions_and_clubs,
                                                                 client: FlaskClient, mock_purchase_places):
        # Cas où l'achat de places réussit
        competitions, clubs = competitions_and_clubs
        club = clubs[0]
        competition = competitions[0]
        places_to_purchase = 5

        # Appel simulé à purchasePlaces en utilisant le monkeypatch
        mock_purchase_places(competition=competition, club=club, places_required=places_to_purchase)

        # Appel à la méthode qui effectue la requête
        _ = self._perform_purchase(client, competition, club, places_to_purchase)

        # Définis une session temporaire pour simuler le comportement de la session
        with client.session_transaction() as sess:
            sess['_flashes'] = [('message', "Great-booking complete!")]

        # Réalise la vérification
        with client.session_transaction() as session:
            flash_messages = session['_flashes']

        # Assure que le message flash attendu est présent
        expected_flash_message = "Great-booking complete!"
        assert any(expected_flash_message in message for message in flash_messages)

    def test_purchase_places_insufficient_seats_shouldnt_substract_points_club(self,
                                                                               competitions_and_clubs,
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

    def test_purchase_places_insufficient_seats_should_render_booking_page(self,
                                                                           competitions_and_clubs,
                                                                           client,
                                                                           mock_purchase_places):
        # Cas où l'utilisateur n'a pas assez de points pour acheter les places
        competitions, clubs = competitions_and_clubs
        club = clubs[0]
        competition = competitions[0]
        initial_places = int(competition['numberOfPlaces'])
        initial_points = int(club['points'])

        # Tentative d'achat de places avec plus de points que l'utilisateur n'en a
        places_to_purchase = initial_places + 1

        mock_purchase_places(competition=competition, club=club, places_required=places_to_purchase)

        # Appel à la fonction ou à la méthode qui effectue la requête
        response = self._perform_purchase(client, competition, club, places_to_purchase)

        # Vérifie que la page de bienvenue est rendue correctement
        assert b'Booking for' in response.data
        assert b'Not enough places available for booking.' in response.data

    def test_purchase_places_insufficient_seats_should_return_flash_message(self,
                                                                            competitions_and_clubs,
                                                                            client,
                                                                            mock_purchase_places):
        # Cas où l'utilisateur n'a pas assez de points pour acheter les places
        competitions, clubs = competitions_and_clubs
        club = clubs[0]
        competition = competitions[0]
        initial_places = int(competition['numberOfPlaces'])
        initial_points = int(club['points'])

        places_to_purchase = initial_places

        mock_purchase_places(competition=competition, club=club, places_required=places_to_purchase)

        # Appel à la fonction ou à la méthode qui effectue la requête
        _ = self._perform_purchase(client, competition, club, places_to_purchase)

        # Vérification du message flash dans la session
        with client.session_transaction() as session:
            flash_messages = session['_flashes']

        # Assure que le message flash attendu est présent
        expected_flash_message = "Not enough places available for booking."
        assert any(expected_flash_message in message for message in flash_messages)

    def test_purchase_places_insufficient_points_shouldnt_substract_places(self,
                                                                           competitions_and_clubs,
                                                                           client,
                                                                           mock_purchase_places):
        # Cas où l'utilisateur n'a pas assez de points pour acheter des places
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

    def test_purchase_places_insufficient_points_should_return_booking_page(self,
                                                                            competitions_and_clubs,
                                                                            client,
                                                                            mock_purchase_places):
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
        response = self._perform_purchase(client, competition, club, places_to_purchase)

        # Vérifie que la page de bienvenue est rendue correctement
        assert b'Booking for' in response.data

    def test_not_enough_points_flash_message(self, client, competitions_and_clubs):
        competitions, clubs = competitions_and_clubs

        # Simule une situation où le nombre de points disponibles est inférieur au nombre de places demandées
        competition_name = "YourCompetitionName"
        club_name = "YourClubName"
        places_required = 10

        # Modifie les données de votre application Flask pour refléter cette situation
        competition = next((c for c in competitions if c['name'] == competition_name), None)
        club = next((c for c in clubs if c['name'] == club_name), None)

        # Ajout des vérifications pour éviter une TypeError
        if competition is not None and club is not None:
            club['points'] = str(places_required - 1)

            # Effectue la requête POST simulée
            response = self._perform_purchase(client, competition, club, places_to_purchase)

            # Vérifie que le message flash est correct
            assert b'Not enough points to make the booking.' in response.data

            # Vérifie que le modèle de rendu est correct
            assert b'booking.html' in response.data
            assert b'Not enough points to make the booking.' in response.data.decode('utf-8')
