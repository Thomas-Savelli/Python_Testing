import pytest
from selenium import webdriver


@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    yield driver


def test_logout_successful(driver):
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

    # Identifie le bouton ou le lien de déconnexion
    logout_button = driver.find_element("xpath", "//a[text()='Logout']")

    # Clique sur le bouton ou le lien de déconnexion
    logout_button.click()

    # Vérifie que l'utilisateur est redirigé vers la page d'accueil
    assert driver.current_url == "http://localhost:5000/logout"
