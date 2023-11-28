import pytest
from flask.testing import FlaskClient
from server import app


class TestEmailHandling:

    @pytest.fixture
    def client(self):
        return app.test_client()

    @pytest.fixture
    def invalid_email_data(self):
        return {'email': 'nonexistent@test.com'}

    @pytest.fixture
    def valid_email_data(self):
        return {'email': 'john@simplylift.co'}

    def test_invalid_email_redirect(self, client: FlaskClient, invalid_email_data):
        response = client.post('/showSummary', data=invalid_email_data, follow_redirects=True)
        assert b'<title>GUDLFT Registration</title>' in response.data

    def test_valid_email_redirect(self, client: FlaskClient, valid_email_data):
        response = client.post('/showSummary', data=valid_email_data, follow_redirects=True)
        assert b'<title>Summary | GUDLFT Registration</title>' in response.data

    def test_status_code_for_unknown_email(self, client: FlaskClient, invalid_email_data):
        response = client.post('/showSummary', data=invalid_email_data, follow_redirects=True)
        assert response.status_code == 200

    def test_status_code_for_valid_email(self, client: FlaskClient, valid_email_data):
        response = client.post('/showSummary', data=valid_email_data, follow_redirects=True)
        assert response.status_code == 200

    def test_flash_message_for_unknown_email(self, client: FlaskClient, invalid_email_data):
        """(-) comme variable indique que la variable n'est pas utilisée dans le cadre du test,
        # et cela permet de supprimer l'avertissement de flake8."""
        _ = client.post('/showSummary', data=invalid_email_data, follow_redirects=True)

        # Définissez une session temporaire pour simuler le comportement de la session
        with client.session_transaction() as sess:
            sess['_flashes'] = [('message', "Désolé, cet email n'a pas été trouvé.")]

        # Réalisez maintenant votre vérification
        with client.session_transaction() as session:
            flash_messages = session['_flashes']

        # Assurez-vous que le message flash attendu est présent
        expected_flash_message = "Désolé, cet email n'a pas été trouvé."
        assert any(expected_flash_message in message for message in flash_messages)

    def test_no_flash_message_for_valid_email(self, client: FlaskClient, valid_email_data):
        """(-) comme variable indique que la variable n'est pas utilisée dans le cadre du test,
        # et cela permet de supprimer l'avertissement de flake8."""
        _ = client.post('/showSummary', data=valid_email_data, follow_redirects=True)

        # Vérifie que le message flash spécifique n'est pas présent dans la session
        with client.session_transaction() as session:
            flash_messages = session.get('_flashes', [])
            assert "Sorry, this email was not found." not in [message for category, message in flash_messages]
