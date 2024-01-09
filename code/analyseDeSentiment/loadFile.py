from  analyseSentiment import rate_global
import os 



# Load comments from the file
def load_comments(file):
    restaurant = {}
    with open("data/"+ file, 'r', encoding='utf-8') as f:
        for line in f:
            lineSplitted = line.strip().split(": ")
            site, comment = lineSplitted[0], lineSplitted[1]
            if site not in restaurant:
                restaurant[site] = []
            restaurant[site].append(comment)
    return restaurant

