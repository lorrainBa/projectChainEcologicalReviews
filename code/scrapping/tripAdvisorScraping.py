from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup
import re
import os

driver = webdriver.Firefox()
driver.get('https://www.tripadvisor.fr/Restaurant_Review-g60763-d425787-Reviews-Katz_s_Deli-New_York_City_New_York.html')

cookie_button_clicked = False

with open('comments.txt', 'w', encoding='utf-8') as file:
    
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
    
    content = driver.page_source.encode('utf-8').strip()
    soup = BeautifulSoup(content, "html.parser")
    
    #On récupère le titre du restaurant
    title_element = soup.find('h1', {'data-test-target': 'top-info-header'})
    restaurant_title = title_element.text.strip()

    # Boucle Tant que le bouton "Suivant" est clickable
    while True:
        
        if not cookie_button_clicked:
            try:
                cookie_button = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, '//button[text()="Tout refuser"]'))
                    )
                cookie_button.click()
                cookie_button_clicked = True

            except Exception as e:
                print("Pas de fenêtre contextuelle des cookies ou impossible de la traiter.")
        
        try:
            next_page_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.LINK_TEXT, 'Suivant'))
            )
            next_page_button.click()
            
            time.sleep(2)
            
            # On récupère le contenu des avis
            content = driver.page_source.encode('utf-8').strip()
            soup = BeautifulSoup(content, "html.parser")
    
            quotes = soup.find_all(class_="noQuotes")
            comments = soup.find_all(class_="prw_rup prw_reviews_text_summary_hsx")
            
            for quote, comment in zip(quotes, comments):
                file.write(quote.text + '\n')
                file.write(comment.text + '\n\n')
            
        except Exception as e:
            # Le bouton "Suivant" n'est plus clickable, sortir de la boucle
            break

    # Récupérer les données de la dernière page
    content = driver.page_source.encode('utf-8').strip()
    soup = BeautifulSoup(content, "html.parser")
    
    quotes = soup.find_all(class_="noQuotes")
    comments = soup.find_all(class_="prw_rup prw_reviews_text_summary_hsx")

    for quote, comment in zip(quotes, comments):
        file.write(quote.text + '\n')
        file.write(comment.text + '\n\n')

driver.quit()

with open('comments.txt', 'r', encoding='utf-8') as input_file:
    comments_content = input_file.read()

# Utiliser une expression régulière pour rechercher des termes liés à "health conscious", "no pesticide", "no antibiotics", etc.
pattern = re.compile(r'\b(organic|organique|health conscious|soucieux de la santé|no pesticide|pas de pesticide|no antibiotics|pas d\'antibiotiques|frais|fresh|non-OGM|sans OGM|pesticide-free|bio|free-range|élevage en plein air)\b', flags=re.IGNORECASE)
matches = pattern.finditer(comments_content)

folder_path = restaurant_title
if not os.path.exists(folder_path):
    os.makedirs(folder_path)
    
with open(os.path.join(folder_path,'Organic.txt'), 'w', encoding='utf-8') as output_file:
    # Écrire les commentaires correspondant aux critères dans le fichier Organic.txt
    for match in matches:
        # Récupérer le commentaire entier en utilisant le span du match
        start, end = match.span()
        comment_start = max(comments_content.rfind('\n', 0, start), 0)
        comment_end = comments_content.find('\n', end)
        comment = comments_content[comment_start:comment_end].strip()

        # Écrire le commentaire dans le fichier Organic.txt
        output_file.write(comment + '\n\n')
        
pattern = re.compile(r'\b(vegan|végan|renewable|renouvelable|low energy|énergie faible|local|compost|composte|sustainable|durable|zero-waste|zéro déchet|carbon-neutral|carbone neutre|plant-based|à base de plantes|eco-conscious|écologique|green practices|pratiques écologiques)\b', flags=re.IGNORECASE)
matches = pattern.finditer(comments_content)

with open(os.path.join(folder_path,'Climate.txt'), 'w', encoding='utf-8') as output_file:
    for match in matches:
        start, end = match.span()
        comment_start = max(comments_content.rfind('\n', 0, start), 0)
        comment_end = comments_content.find('\n', end)
        comment = comments_content[comment_start:comment_end].strip()

        output_file.write(comment + '\n\n')
        
pattern = re.compile(r'\b(water pollution|pollution de l\'eau|waste of water|gaspillage d\'eau|treated|traité|plastic bottle|bouteille en plastique|tap water|robinet)\b', flags=re.IGNORECASE)
matches = pattern.finditer(comments_content)

with open(os.path.join(folder_path,'Water.txt'), 'w', encoding='utf-8') as output_file:
    for match in matches:
        start, end = match.span()
        comment_start = max(comments_content.rfind('\n', 0, start), 0)
        comment_end = comments_content.find('\n', end)
        comment = comments_content[comment_start:comment_end].strip()

        output_file.write(comment + '\n\n')

pattern = re.compile(r'\b(socially responsible|socialement responsable|conscious|conscient|diverse|divers|ethical|éthique)\b', flags=re.IGNORECASE)
matches = pattern.finditer(comments_content)

with open(os.path.join(folder_path,'Social.txt'), 'w', encoding='utf-8') as output_file:
    for match in matches:
        start, end = match.span()
        comment_start = max(comments_content.rfind('\n', 0, start), 0)
        comment_end = comments_content.find('\n', end)
        comment = comments_content[comment_start:comment_end].strip()

        output_file.write(comment + '\n\n')

pattern = re.compile(r'\b(diverse|divers|responsible|responsable|reliable|fiable|committed|engagé|integrous|intègre)\b', flags=re.IGNORECASE)
matches = pattern.finditer(comments_content)

with open(os.path.join(folder_path,'Governance.txt'), 'w', encoding='utf-8') as output_file:
    for match in matches:
        start, end = match.span()
        comment_start = max(comments_content.rfind('\n', 0, start), 0)
        comment_end = comments_content.find('\n', end)
        comment = comments_content[comment_start:comment_end].strip()

        output_file.write(comment + '\n\n')

pattern = re.compile(r'\b(plastic free|sans plastique|reused|réutilisé|circular|circulaire|compost|composte|recycled|recyclé|sustainable|durable)\b', flags=re.IGNORECASE)
matches = pattern.finditer(comments_content)

with open(os.path.join(folder_path,'Waste.txt'), 'w', encoding='utf-8') as output_file:
    for match in matches:
        start, end = match.span()
        comment_start = max(comments_content.rfind('\n', 0, start), 0)
        comment_end = comments_content.find('\n', end)
        comment = comments_content[comment_start:comment_end].strip()

        output_file.write(comment + '\n\n')

pattern = re.compile(r'\b(greenwashing|écoblanchiment|misleading environmental marketing|marketing environnemental trompeur|pseudosustainable|pseudodurable)\b', flags=re.IGNORECASE)
matches = pattern.finditer(comments_content)

with open(os.path.join(folder_path,'Adverse.txt'), 'w', encoding='utf-8') as output_file:
    for match in matches:
        start, end = match.span()
        comment_start = max(comments_content.rfind('\n', 0, start), 0)
        comment_end = comments_content.find('\n', end)
        comment = comments_content[comment_start:comment_end].strip()

        output_file.write(comment + '\n\n')
