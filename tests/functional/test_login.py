import pytest
from selenium import webdriver


@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(options=options)
    yield driver


def test_login_successful(driver):
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


def test_login_with_incorrect_email(driver):
    # Scénario de tentative de connexion avec un email incorrect
    driver.get('http://localhost:5000/')

    # Identifie les éléments de la page (champ email et bouton)
    email_input = driver.find_element("name", "email")
    login_button = driver.find_element("xpath", "//button[text()='Enter']")

    # Saisie email incorrect
    email_input.send_keys("test@testemail.com")

    # Action de clique sur le bouton de connexion
    login_button.click()

    # Vérifie que le message d'erreur approprié est affiché
    error_message = driver.find_element("xpath", "//ul/li[contains(text(), 'Sorry, this email was not found.')]")
    assert error_message.text == "Sorry, this email was not found."

    # Vérifie que l'utilisateur reste sur la page de connexion
    assert driver.current_url == "http://localhost:5000/showSummary"
