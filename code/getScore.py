from loadFile  import getDictionnaryOfCategoryComments
from analyseSentiment import rate_global
import os
from scrapingTripadvisor import getDataFromRestaurant


dataPath = "./../data/"
getDataFromRestaurant('https://www.tripadvisor.fr/Restaurant_Review-g60763-d424545-Reviews-Ellen_s_Stardust_Diner-New_York_City_New_York.html')
#Get the folder to treat
dossierATraiter = os.listdir(dataPath)
# Filtrer les dossiers uniquement (ignorer les fichiers)
sous_dossiers = [dossier for dossier in dossierATraiter if os.path.isdir(os.path.join(dataPath, dossier))]
for file_name in sous_dossiers:
    restaurant_comments = getDictionnaryOfCategoryComments(dataPath+file_name)
    rate_global(restaurant_comments,file_name)
