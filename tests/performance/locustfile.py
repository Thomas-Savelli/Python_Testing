from locust import HttpUser, task
from datetime import datetime
import random


def competition_is_past(competition_date_str):
    # Converti la date de la compétition en objet datetime
    competition_date = datetime.strptime(competition_date_str, '%Y-%m-%d %H:%M:%S')

    # Renvoie True si la compétition est passée, sinon False
    return competition_date < datetime.now()


class PerfTest(HttpUser):
    host = "http://localhost:5000"

    # Chargement des données depuis les fichiers JSON
    clubs = [
        {"name": "Simply Lift", "email": "john@simplylift.co", "points": "18"},
        {"name": "Iron Temple", "email": "admin@irontemple.com", "points": "4"},
        {"name": "She Lifts", "email": "kate@shelifts.co.uk", "points": "12"}
    ]

    competitions = [
        {"name": "Spring Festival", "date": "2024-03-27 10:00:00", "numberOfPlaces": "25"},
        {"name": "Fall Classic", "date": "2020-10-22 13:30:00", "numberOfPlaces": "13"},
        {"name": "Open Ile Rousse", "date": "2023-12-22 13:30:00", "numberOfPlaces": "40"},
        {"name": "Open calvi", "date": "2023-12-22 13:30:00", "numberOfPlaces": "5"}
    ]

    @task
    def test_login(self):
        credentials = {"email": "john@simplylift.co"}
        self.client.post("/showSummary", data=credentials)

    @task
    def test_display_points(self):
        self.client.get("/pointsDisplay")

    @task
    def test_book(self):
        # Sélection aléatoire d'un club et d'une compétition à partir des données chargées
        club = random.choice(self.clubs)
        competition = random.choice(self.competitions)

        # Accés à la page de réservation
        self.client.get(f"/book/{competition['name']}/{club['name']}")

    @task
    def test_purchase_places(self):
        # Sélection aléatoire d'un club et d'une compétition à partir des données chargées
        club = random.choice(self.clubs)
        competition = random.choice(self.competitions)

        # Effectuer une réservation (POST)
        places_to_book = random.randint(1, min(int(competition['numberOfPlaces']), int(club['points'])))
        payload = {
            "competition": competition['name'],
            "club": club['name'],
            "places": places_to_book
        }

        # Accéder à la page de réservation et effectuer la réservation
        self.client.post("/purchasePlaces", data=payload)

    @task
    def test_view_logout(self):
        self.client.get("/logout")
