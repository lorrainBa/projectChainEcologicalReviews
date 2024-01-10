from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup

driver = webdriver.Firefox()
#un exemple de page
driver.get('https://www.tripadvisor.fr/Restaurant_Review-g187156-d3901925-Reviews-V_B-Perpignan_Pyrenees_Orientales_Occitanie.html')

current_page = 1
cookie_button_clicked = False

#Boucle Tant que le bouton "Suivant" est clickable
while True:
    
    # Gérer la fenêtre contextuelle des cookies s'il y en a une
    if not cookie_button_clicked:
        
        try:
            cookie_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//button[text()="Tout refuser"]'))
            )
            cookie_button.click()
            cookie_button_clicked = True
            
        except Exception as e:
            print("Pas de fenêtre contextuelle des cookies ou impossible de la traiter.")
        
    print(current_page)
    
    #On essaie de cliquer sur le bouton "suivant"
    try:
        next_page_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, 'Suivant'))
        )
        next_page_button.click()
        
        #On récupère le contenu des avis
        content = driver.page_source.encode('utf-8').strip()
        soup = BeautifulSoup(content, "html.parser")

        quotes = soup.find_all(class_="noQuotes")
        comments = soup.find_all(class_="prw_rup prw_reviews_text_summary_hsx")
        
        for quote in quotes:
            print(quote.text)
            
        for comment in comments:
            print(comment.text)
            
        current_page = current_page + 1
        
    except Exception as e:
        # Le bouton "Suivant" n'est plus clickable, sortir de la boucle
        break
        
# Récupérer les données de la dernière page
content = driver.page_source.encode('utf-8').strip()
soup = BeautifulSoup(content, "html.parser")

quotes = soup.find_all(class_="noQuotes")
comments = soup.find_all(class_="prw_rup prw_reviews_text_summary_hsx")

for quote in quotes:
    print(quote.text)

for comment in comments:
    print(comment.text)

# Fermer le navigateur à la fin
driver.quit()
