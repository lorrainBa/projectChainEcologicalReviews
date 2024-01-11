from textblob import TextBlob
from saveGraph import createBarChart
import matplotlib.pyplot as plt
import os 

def analyze_sentiment(comment):
    # Use TextBlob for sentiment analysis
    blob = TextBlob(comment)
    return blob.sentiment.polarity

 

def rate_site(comments):
    # Initialize the sum of polarities
    sum_polarities = 0.0

    # Analyze each comment
    for comment in comments:
        polarity = analyze_sentiment(comment)
        sum_polarities += polarity

    # Calculate the average polarities
    average_polarities = sum_polarities / len(comments)

    # Convert the average polarity to a rating from 0 to 5
    rating = (average_polarities + 1) * 2.5

    return rating







def rate_global(dictionarryOfCategories):
    # Initialize the sum of site ratings and a dictionary to store individual site ratings
    finalScore = 0.0
    categoryScore = {}
    siteCategoryScore = {}
    
    # Analyze each category.txt
    for category in dictionarryOfCategories:
        #Each site will have a mean score for the category
        sum_site_ratings = 0.0
        
        for site, comments in dictionarryOfCategories[category].items():
            site_rating = rate_site(comments)
            sum_site_ratings += site_rating

            print(f"Site {site}: Rating {site_rating:.2f}")
            
            #Add the score link to the category of a certain website
            if site in siteCategoryScore:
                siteCategoryScore[site][category] = site_rating

            else:
                siteCategoryScore[site] = {}
                siteCategoryScore[site][category] = site_rating

        # Calculate the category ratings
        average_site_ratings = sum_site_ratings / len(dictionarryOfCategories[category])

        categoryScore[category] = average_site_ratings
        finalScore += average_site_ratings
        print(f"\nOverall Restaurant Rating for category {category} is: {average_site_ratings:.2f}\n\n")
    
    
    finalScore = finalScore / len(dictionarryOfCategories)
    print("Final mean score is",finalScore)
    print(categoryScore,"-___-")
    createBarChart(categoryScore,"everyApp")

    for site in siteCategoryScore:
        print(siteCategoryScore[site],"--")
        createBarChart(siteCategoryScore[site],site)


    return categoryScore


