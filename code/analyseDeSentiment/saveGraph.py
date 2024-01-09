import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap


def color_based_on_rating(rating):
    # Define a custom colormap from red to dark green
    cmap = LinearSegmentedColormap.from_list('rating_cmap', [(1, 0, 0), (1, 1, 0), (0, 0.5, 0)])

    # Normalize the rating to the range [0, 1]
    norm_rating = min(1, max(0, rating / 5.0))

    # Map the normalized rating to the colormap
    color_code = cmap(norm_rating)

    return color_code
    




def createBarChart(site_ratings):
    # Sort the sites based on ratings (from low to high)
    sorted_sites = sorted(site_ratings, key=site_ratings.get, reverse=False)
    sorted_ratings = [site_ratings[site] for site in sorted_sites]

    # Round the ratings to one decimal place
    sorted_ratings = [round(r, 1) for r in sorted_ratings]

    # Create a horizontal bar chart for better readability
    colors = [color_based_on_rating(r) for r in sorted_ratings]
    plt.barh(sorted_sites, sorted_ratings, color=colors)

    # Add labels and title
    plt.xlabel('Ratings')
    plt.ylabel('Restaurant Sites')
    plt.title('Overall Ratings for Each Site (Sorted)')

    # Display rounded ratings on the bars for better clarity
    for i, v in enumerate(sorted_ratings):
        plt.text(v, i, str(v), color='black', va='center')

    # Add a grid for better readability
    plt.grid(axis='x', linestyle='--', alpha=0.6)

    # Save the image
    plt.savefig('output/graph/scoreBarChart.png', bbox_inches='tight')

