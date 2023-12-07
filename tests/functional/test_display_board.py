import pytest
from selenium import webdriver


@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    yield driver


def test_inline_points_display_access(driver):
    # Accéde à la page de connexion
    driver.get("http://localhost:5000/")

    # Identifie les éléments de la page (champ email et boutton)
    email_input = driver.find_element("name", "email")
    login_button = driver.find_element("xpath", "//button[text()='Enter']")

    # Saisis les informations de connexion
    email_input.send_keys("john@simplylift.co")

    # Soumets le formulaire
    login_button.click()

    # Vérifie que l'utilisateur est redirigé vers la page d'accueil
    assert driver.current_url == "http://localhost:5000/showSummary"

    # Identifier le lien "Points Display" et cliquer dessus
    display_points_link = driver.find_element("xpath", "//a[text()='Points Display']")
    display_points_link.click()

    assert driver.current_url == "http://localhost:5000/pointsDisplay"

    # Vérifier que les points des clubs avec leurs noms sont bien affichés
    club_rows = driver.find_elements("xpath", "//table/tbody/tr")
    assert club_rows, "Aucune ligne de club trouvée sur la page."

    for club_row in club_rows:
        club_name = club_row.find_element("xpath", "./td[1]").text
        club_points = club_row.find_element("xpath", "./td[2]").text

        # Assurez-vous que les cellules ne sont pas vides
        assert club_name.strip(), f"La cellule du nom du club est vide pour le club {club_name}."
        assert club_points.strip(), f"La cellule des points du club est vide pour le club {club_points}."


def test_offline_points_display_access(driver):
    # Accéde à la page de connexion
    driver.get("http://localhost:5000/")

    # Identifier le lien "Points Display" et cliquer dessus
    display_points_link = driver.find_element("xpath", "//a[text()='Points Display']")
    display_points_link.click()

    assert driver.current_url == "http://localhost:5000/pointsDisplay"

    # Vérifier que les points des clubs avec leurs noms sont bien affichés
    club_rows = driver.find_elements("xpath", "//table/tbody/tr")
    assert club_rows, "Aucune ligne de club trouvée sur la page."

    for club_row in club_rows:
        club_name = club_row.find_element("xpath", "./td[1]").text
        club_points = club_row.find_element("xpath", "./td[2]").text

        # Assurez-vous que les cellules ne sont pas vides
        assert club_name.strip(), f"La cellule du nom du club est vide pour le club {club_name}."
        assert club_points.strip(), f"La cellule des points du club est vide pour le club {club_points}."
