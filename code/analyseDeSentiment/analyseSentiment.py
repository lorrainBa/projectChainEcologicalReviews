from textblob import TextBlob
from saveGraph import createBarChart
import matplotlib.pyplot as plt
import numpy as np

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







def rate_global(restaurant):
    # Initialize the sum of site ratings and a dictionary to store individual site ratings
    sum_site_ratings = 0.0
    site_ratings = {}

    # Analyze each site
    for site, comments in restaurant.items():
        site_rating = rate_site(comments)
        sum_site_ratings += site_rating
        site_ratings[site] = site_rating
        print(f"Site {site}: Rating {site_rating:.2f}")

    # Calculate the average site ratings
    average_site_ratings = sum_site_ratings / len(restaurant)

    print(f"\nOverall Restaurant Rating: {average_site_ratings:.2f}")

    createBarChart(site_ratings)

    return site_ratings


