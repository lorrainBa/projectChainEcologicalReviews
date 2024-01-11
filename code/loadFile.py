from  analyseSentiment import rate_global
import os 



# Load comments from the file
def load_comments(file):
    restaurant = {}
    with open(file, 'r', encoding='utf-8') as f:
        for line in f:
            lineSplitted = line.strip().split(": ")
            site, comment = lineSplitted[0], lineSplitted[1]
            if site not in restaurant:
                restaurant[site] = []
            restaurant[site].append(comment)
    return restaurant

# Create a dictionary of dictionaries
def getDictionnaryOfCategoryComments(directory):
    main_dictionary = {}
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            file_path = os.path.join(directory, filename)
            comments_dict = load_comments(file_path)
            main_dictionary[filename] = comments_dict
    return main_dictionary
