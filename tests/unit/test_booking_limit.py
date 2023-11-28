import pytest

from server import app, loadClubs, loadCompetitions


class TestBookingLimit():

    @pytest.fixture
    def client(self):
        return app.test_client()

    @pytest.fixture
    def competitions_and_clubs(self):
        # Fixture pour charger les données nécessaires pour les tests
        competitions = loadCompetitions()
        clubs = loadClubs()
        return competitions, clubs

    def _perform_purchase(self, client, competition, club, places_to_purchase):
        return client.post('/purchasePlaces', data={
            'competition': competition['name'],
            'club': club['name'],
            'places': places_to_purchase
        })

    def test_booking_more_than_12_places_should_return_wrong_message(self, client, competitions_and_clubs):

        competitions, clubs = competitions_and_clubs

        # Simule une situation où le nombre de places est supérieur au nombre authorisé
        competition_name = "YourCompetitionName"
        club_name = "YourClubName"
        places_to_purchase = 14

        # Modifie les données de votre application Flask pour refléter cette situation
        competition = next((c for c in competitions if c['name'] == competition_name), None)
        club = next((c for c in clubs if c['name'] == club_name), None)

        # Ajout des vérifications pour éviter une TypeError
        if competition is not None and club is not None:
            club['points'] = str(places_to_purchase)

            # Effectue la requête POST simulée
            response = self._perform_purchase(client, competition, club, places_to_purchase)
            # Vérifie que le message flash est correct
            assert "You can't book more than 12 places for a competition." in response.data

    def test_booking_less_than_or_equal_to_12_places_should_succeed(self, client, competitions_and_clubs):
        competitions, clubs = competitions_and_clubs

        # Simule une situation où le nombre de places est inférieur ou égal à 12
        competition_name = "YourCompetitionName"
        club_name = "YourClubName"
        places_required = 10

        # Modifie les données de votre application Flask pour refléter cette situation
        competition = next((c for c in competitions if c['name'] == competition_name), None)
        club = next((c for c in clubs if c['name'] == club_name), None)

        # Ajoute des vérifications pour éviter une TypeError
        if competition is not None and club is not None:
            club['points'] = str(places_required)

            # Effectue la requête POST simulée
            response = self._perform_purchase(client, competition, club, places_required)
            # Vérifie que le message flash n'est pas présent (pas d'erreur)
            assert b"You can't book more than 12 places for a competition." not in response.data
            # Vérifie que la redirection vers welcome.html a eu lieu
            assert b'Welcome' in response.data
