from loadFile  import load_comments
from analyseSentiment import rate_global




dataPath = "data/"
file_name = "mcdo.txt"
restaurant_comments = load_comments(file_name)
rate_global(restaurant_comments)
