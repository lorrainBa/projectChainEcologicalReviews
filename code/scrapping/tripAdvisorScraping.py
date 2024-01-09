from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup

driver = webdriver.Firefox()
#un exemple de page
driver.get('https://www.tripadvisor.fr/Restaurant_Review-g187156-d3901925-Reviews-V_B-Perpignan_Pyrenees_Orientales_Occitanie.html')

while True:
    # Récupérer les données de la page
    content = driver.page_source.encode('utf-8').strip()
    soup = BeautifulSoup(content, "html.parser")

    quotes = soup.find_all(class_="quote")
    for quote in quotes:
        print(quote.text)

    comments = soup.find_all(class_="prw_rup prw_reviews_text_summary_hsx") 
    for comment in comments:
        print(comment.text)

    # Essayer de cliquer sur le bouton "suivant"
    try:
        next_page_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, 'Suivant'))
        )
        next_page_button.click()

        # Attendre que la page se charge
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "quote"))
        )

    except Exception as e:
        # Le bouton "suivant" n'est plus clickable, sortir de la boucle
        print("Fin de la pagination.")
        break

# Fermer le navigateur à la fin
driver.quit()
