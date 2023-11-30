from flask import Flask
import pytest
from server import app  # Assurez-vous d'importer votre application Flask
from flask.testing import FlaskClient


class TestBookingPastCompetition():

    @pytest.fixture
    def client(self):
        app.config['TESTING'] = True
        client = app.test_client()
        yield client

    def test_book_past_competition_error_message(self, client: FlaskClient):
        # Simule la connexion de l'utilisateur (vous devrez peut-être ajuster cela selon votre logique de connexion)
        response = client.post('/showSummary', data={'email': 'john@simplylift.co'})

        # S"assure que la page welcome.html a bien été rendue
        assert 'Welcome,' in response.data.decode('utf-8')

        # Tente de réserver des places pour une compétition passée
        response = client.get('/book/Spring Festival/Simply Lift')

        # S'assure que le message d'erreur est affiché sur la page welcome.html
        assert "can't book places for a past competition" in response.data.decode('utf-8').replace('&#39;', "'").lower()

    def test_book_future_competition(self, client: FlaskClient):
        # Simule la connexion de l'utilisateur (vous devrez peut-être ajuster cela selon votre logique de connexion)
        response = client.post('/showSummary', data={'email': 'john@simplylift.co'})

        # S'assure que la page welcome.html a bien été rendue
        assert 'Welcome,' in response.data.decode('utf-8')

        # Tente de réserver des places pour une compétition future
        response = client.get('/book/Open Ile Rousse/Simply Lift')

        # Affiche le contenu de response.data pour le débogage
        print("response.data:", response.data)

        # S'assure que la page de réservation est rendue sans message d'erreur
        assert b'Booking for' in response.data
        assert "can't book places for a past competition" not in response.data.decode('utf-8').replace('&#39;', "'").lower()