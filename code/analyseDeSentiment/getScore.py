from loadFile  import getDictionnaryOfCategoryComments
from analyseSentiment import rate_global




dataPath = "data/"
file_name = "quickArgenteuil"
restaurant_comments = getDictionnaryOfCategoryComments(dataPath+file_name)
rate_global(restaurant_comments)
