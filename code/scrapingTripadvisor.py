#!/usr/bin/env python
# coding: utf-8

# In[4]:


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import os
import re

def handle_cookies(driver, cookie_button_clicked):
    if not cookie_button_clicked:
        try:
            cookie_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//button[text()="Tout refuser"]'))
            )
            cookie_button.click()
            cookie_button_clicked = True
        except Exception as e:
            print("Pas de fenêtre contextuelle des cookies ou impossible de la traiter.")
    return cookie_button_clicked

def get_page_content(driver):
    content = driver.page_source.encode('utf-8').strip()
    return BeautifulSoup(content, "html.parser")

def scrape_comments(driver, file):
    cookie_button_clicked = False

    cookie_button_clicked = handle_cookies(driver, cookie_button_clicked)

    soup = get_page_content(driver)
    
    title_element = soup.find('h1', {'data-test-target': 'top-info-header'})
    restaurant_title = title_element.text.strip()

    while True:
        cookie_button_clicked = handle_cookies(driver, cookie_button_clicked)

        try:
            next_page_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.LINK_TEXT, 'Suivant'))
            )
            next_page_button.click()

            time.sleep(2)

            soup = get_page_content(driver)
            quotes = soup.find_all(class_="noQuotes")
            comments = soup.find_all(class_="prw_rup prw_reviews_text_summary_hsx")

            for quote, comment in zip(quotes, comments):
                file.write(quote.text + '\n')
                file.write(comment.text + '\n\n')

        except Exception as e:
            break

    soup = get_page_content(driver)
    quotes = soup.find_all(class_="noQuotes")
    comments = soup.find_all(class_="prw_rup prw_reviews_text_summary_hsx")

    for quote, comment in zip(quotes, comments):
        file.write(quote.text + '\n')
        file.write(comment.text + '\n\n')

    return restaurant_title

def read_comments(file_path='tripAdvisorComments.txt'):
    with open(file_path, 'r', encoding='utf-8') as input_file:
        return input_file.read()

def write_matching_comments(matches, output_file_path, comments_content):
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        for match in matches:
            start, end = match.span()
            comment_start = max(comments_content.rfind('\n', 0, start), 0)
            comment_end = comments_content.find('\n', end)
            comment = comments_content[comment_start:comment_end].strip()
            output_file.write(comment + '\n\n')

def process_comments(comments_content, folder_path, patterns, output_file_names):
    for pattern, output_file_name in zip(patterns, output_file_names):
        matches = pattern.finditer(comments_content)
        output_file_path = os.path.join(folder_path, output_file_name)
        write_matching_comments(matches, output_file_path, comments_content)

def getDataFromRestaurant():
    driver = webdriver.Firefox()
    driver.get('https://www.tripadvisor.fr/Restaurant_Review-g60763-d424545-Reviews-Ellen_s_Stardust_Diner-New_York_City_New_York.html')

    with open('tripAdvisorComments.txt', 'w', encoding='utf-8') as file:
        restaurant_title = scrape_comments(driver, file)

    driver.quit()

    comments_content = read_comments()

    # Patterns for different categories
    organic_pattern = re.compile(r'\b(organic|organique|health conscious|soucieux de la santé|no pesticide|pas de pesticide|no antibiotics|pas d\'antibiotiques|non-OGM|sans OGM|pesticide-free|bio|free-range|élevage en plein air)\b', flags=re.IGNORECASE)
    climate_pattern = re.compile(r'\b(climate|climat|vegan|végan|renewable|renouvelable|low energy|énergie faible|local|compost|composte|sustainable|durable|zero-waste|zéro déchet|carbon-neutral|carbone neutre|plant-based|à base de plantes|eco-conscious|écologique|green practices|pratiques écologiques)\b', flags=re.IGNORECASE)
    water_pattern = re.compile(r'\b(water|eau|water pollution|pollution de l\'eau|waste of water|gaspillage d\'eau|treated|traité|plastic bottle|bouteille en plastique|tap water|robinet)\b', flags=re.IGNORECASE)
    social_pattern = re.compile(r'\b(social|social|socially responsible|socialement responsable|conscious|conscient|diverse|divers|ethical|éthique)\b', flags=re.IGNORECASE)
    governance_pattern = re.compile(r'\b(governance|gouvernance|diverse|divers|responsible|responsable|reliable|fiable|committed|engagé|integrous|intègre)\b', flags=re.IGNORECASE)
    waste_pattern = re.compile(r'\b(waste|gaspillage|plastic free|sans plastique|reused|réutilisé|circular|circulaire|compost|composte|recycled|recyclé|sustainable|durable)\b', flags=re.IGNORECASE)
    adverse_pattern = re.compile(r'\b(adverse|défavorable|greenwashing|écoblanchiment|misleading environmental marketing|marketing environnemental trompeur|pseudosustainable|pseudodurable)\b', flags=re.IGNORECASE)

    patterns = [organic_pattern, climate_pattern, water_pattern, social_pattern, governance_pattern, waste_pattern, adverse_pattern]
    output_file_names = ['Organic.txt', 'Climate.txt', 'Water.txt', 'Social.txt', 'Governance.txt', 'Waste.txt', 'Adverse.txt']

    folder_path = '../../data/' + restaurant_title

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    process_comments(comments_content, folder_path, patterns, output_file_names)

