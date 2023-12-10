import pytest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()


def test_purchase_successful(driver):
    # Accéder à la page de connexion
    driver.get("http://localhost:5000/")

    # Identifie les éléments de la page (champ email et bouton)
    email_input = driver.find_element("name", "email")
    login_button = driver.find_element("xpath", "//button[text()='Enter']")

    # Saisie les informations de connexion
    email_input.send_keys("john@simplylift.co")

    # Soumet le formulaire de connexion
    login_button.click()

    # Attend la présence du texte "Welcome, john@simplylift.co" dans le corps de la page
    welcome_message_locator = (By.XPATH, "//h2[contains(text(), 'Welcome, john@simplylift.co')]")
    WebDriverWait(driver, 20).until(EC.text_to_be_present_in_element(welcome_message_locator,
                                                                     "Welcome, john@simplylift.co"))

    # Récupérer tous les liens à l'intérieur des balises <li>
    all_book_places_links = driver.find_elements(By.XPATH, "//li/a")

    # Vérifier s'il y a des liens trouvés
    if all_book_places_links:
        # Cliquer sur le premier lien "Book Places"
        all_book_places_links[0].click()
    else:
        print("Aucun élément 'Book Places' trouvé.")

    # Achat des places (simuler le processus d'achat)
    places_input = driver.find_element("name", "places")
    places_input.send_keys("2")

    purchase_button = driver.find_element("xpath", "//button[text()='Book']")
    purchase_button.click()

    # Vérifie que le redirection a été faite correctement
    assert "Welcome, john@simplylift.co" in driver.page_source
    # Vérifie que les places sont réservées correctement et le message en retour
    assert "Great-booking complete!" in driver.page_source


def test_purchase_select_competition_past(driver):
    # Accéder à la page de connexion
    driver.get("http://localhost:5000/")

    # Identifie les éléments de la page (champ email et bouton)
    email_input = driver.find_element("name", "email")
    login_button = driver.find_element("xpath", "//button[text()='Enter']")

    # Saisie les informations de connexion
    email_input.send_keys("john@simplylift.co")

    # Soumet le formulaire de connexion
    login_button.click()

    # Attend la présence du texte "Welcome, john@simplylift.co" dans le corps de la page
    welcome_message_locator = (By.XPATH, "//h2[contains(text(), 'Welcome, john@simplylift.co')]")
    WebDriverWait(driver, 20).until(EC.text_to_be_present_in_element(welcome_message_locator,
                                                                     "Welcome, john@simplylift.co"))

    # Récupérer tous les liens à l'intérieur des balises <li>
    all_book_places_links = driver.find_elements(By.XPATH, "//li/a")

    # Vérifier s'il y a des liens trouvés
    if all_book_places_links:
        # Cliquer sur le premier lien "Book Places"
        all_book_places_links[1].click()
    else:
        print("Aucun élément 'Book Places' trouvé.")

    # Vérifie que le redirection a été faite correctement
    assert "Welcome, john@simplylift.co" in driver.page_source
    # Vérifie que les places sont réservées correctement et le message en retour
    assert "You can't book places for a past competition." in driver.page_source


def test_purchase_places_insufficient_seats(driver):
    # Accéder à la page de connexion
    driver.get("http://localhost:5000/")

    # Identifie les éléments de la page (champ email et bouton)
    email_input = driver.find_element("name", "email")
    login_button = driver.find_element("xpath", "//button[text()='Enter']")

    # Saisie les informations de connexion
    email_input.send_keys("john@simplylift.co")

    # Soumet le formulaire de connexion
    login_button.click()

    # Attend la présence du texte "Welcome, john@simplylift.co" dans le corps de la page
    welcome_message_locator = (By.XPATH, "//h2[contains(text(), 'Welcome, john@simplylift.co')]")
    WebDriverWait(driver, 20).until(EC.text_to_be_present_in_element(welcome_message_locator,
                                                                     "Welcome, john@simplylift.co"))

    # Récupérer tous les liens à l'intérieur des balises <li>
    all_book_places_links = driver.find_elements(By.XPATH, "//li/a")

    # Vérifier s'il y a des liens trouvés
    if all_book_places_links:
        # Cliquer sur le premier lien "Book Places"
        all_book_places_links[3].click()
    else:
        print("Aucun élément 'Book Places' trouvé.")

    # Achat des places (simuler le processus d'achat)
    places_input = driver.find_element("name", "places")
    places_input.send_keys("10")

    purchase_button = driver.find_element("xpath", "//button[text()='Book']")
    purchase_button.click()

    # Vérifie que le redirection a été faite correctement
    assert "Booking for" in driver.page_source
    # Vérifie que les places sont réservées correctement et le message en retour
    assert "Not enough places available for booking." in driver.page_source


def test_purchase_insufficient_points(driver):
    # Accéder à la page de connexion
    driver.get("http://localhost:5000/")

    # Identifie les éléments de la page (champ email et bouton)
    email_input = driver.find_element("name", "email")
    login_button = driver.find_element("xpath", "//button[text()='Enter']")

    # Saisie les informations de connexion
    email_input.send_keys("admin@irontemple.com")

    # Soumet le formulaire de connexion
    login_button.click()

    # Attend la présence du texte "Welcome, john@simplylift.co" dans le corps de la page
    welcome_message_locator = (By.XPATH, "//h2[contains(text(), 'Welcome, admin@irontemple.com')]")
    WebDriverWait(driver, 20).until(EC.text_to_be_present_in_element(welcome_message_locator,
                                                                     "Welcome, admin@irontemple.com"))

    # Récupérer tous les liens à l'intérieur des balises <li>
    all_book_places_links = driver.find_elements(By.XPATH, "//li/a")

    # Vérifier s'il y a des liens trouvés
    if all_book_places_links:
        # Cliquer sur le premier lien "Book Places"
        all_book_places_links[0].click()
    else:
        print("Aucun élément 'Book Places' trouvé.")

    # Achat des places (simuler le processus d'achat)
    places_input = driver.find_element("name", "places")
    places_input.send_keys("6")

    purchase_button = driver.find_element("xpath", "//button[text()='Book']")
    purchase_button.click()

    # Vérifie que le redirection a été faite correctement
    assert "Booking for" in driver.page_source
    # Vérifie que les places sont réservées correctement et le message en retour
    assert "Not enough points to make the booking." in driver.page_source
