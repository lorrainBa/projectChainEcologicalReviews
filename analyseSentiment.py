from textblob import TextBlob

def analyse_sentiment(commentaire):
    # Utilisation de TextBlob pour l'analyse de sentiment
    blob = TextBlob(commentaire)
    return blob.sentiment.polarity

def noter_site(commentaires):
    # Initialiser la somme des polarités
    somme_polarites = 0.0

    # Analyser chaque commentaire
    for commentaire in commentaires:
        polarite = analyse_sentiment(commentaire)
        somme_polarites += polarite

    # Calculer la moyenne des polarités
    moyenne_polarites = somme_polarites / len(commentaires)

    # Convertir la polarité moyenne en note de 0 à 5
    note = (moyenne_polarites + 1) * 2.5

    return note

def noter_global(restaurant):
    # Initialiser la somme des notes des sites
    somme_notes_sites = 0.0

    # Analyser chaque site
    for site, commentaires in restaurant.items():
        note_site = noter_site(commentaires)
        somme_notes_sites += note_site
        print(f"Site {site}: Note {note_site:.2f}")

    # Calculer la moyenne des notes des sites
    moyenne_notes_sites = somme_notes_sites / len(restaurant)

    print(f"\nNote Globale du Restaurant: {moyenne_notes_sites:.2f}")

# Charger les commentaires depuis le fichier
def charger_commentaires(fichier):
    restaurant = {}
    with open(fichier, 'r', encoding='utf-8') as file:
        for ligne in file:
            site, commentaire = ligne.strip().split(": ", 1)
            if site not in restaurant:
                restaurant[site] = []
            restaurant[site].append(commentaire)
    return restaurant

# Exemple d'utilisation
nom_fichier = "nomRestaurant.txt"
commentaires_restaurant = charger_commentaires(nom_fichier)
noter_global(commentaires_restaurant)
