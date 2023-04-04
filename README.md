# Personalisation for (Public) Media: Final Project
This repository contains the final project for the Personalisation of (Public) Media course. The project is about implementing diversity and serendipity in the recommendation algorithm from NPO, a Dutch public broadcaster that heavily relies on government funding and feedback from the Dutch population.

As NPO is responsible for creating and distributing content, it is crucial to ensure the satisfaction of the general audience while respecting laws regarding content creation, diffusion, and consumption safety. Although achieving general public satisfaction on a traditional broadcasting medium such as television is challenging due to the lack of control from the user's perspective, a web platform that offers all the content can be accessible for all and at any time, thus fixing the issue with control and boosting satisfaction.

To achieve this goal, we have created a webpage that displays diverse and serendipitous recommendations. A live preview can be accessed in the following link: http://iabrilvzqz.pythonanywhere.com/. However, it can also be run locally by following the steps below.

## Installation
To run this project, follow these steps:

1. Clone this repository in your computer by running `git clone https://github.com/iabrilvzqz/personalisation-for-public-media.git`
1. Install the required packages by running `pip install -r requirements.txt`
1. Run the Flask application by executing `python flask_app.py`
1. Open your web browser and go to `http://127.0.0.1:5000/`

## Data Scraping
Additionally, there is a script to scrape all the content from NPO Start platform by type (Programma, Film, Serie, Documentaire). Then, MovieMeter website is scraped to complete information on the items that were not found at NPO Start. Finally, the data is cleaned and prepared to be used in the recommendation algorithm. 

## Data Generation
Also, there is a script to generate synthetic data for the recommendation system. The script creates four user personas identified on a survey and generates a total of 1000 users. The script generates synthetic data for each user based on their user type and preferences, including information about the content they interacted with, such as whether they viewed or previewed it, and what rating and sharing values they assigned to it. This data id used to train the recommendation algorithms.

## Recommendation Algorithms
There are four different recommendation algorithms:

### Hybrid algorithm to provide personalised recommendations
This algorithm utilizes **collaborative filtering** and **content-based filtering** techniques to provide personalized recommendations to users based on their previous interactions with items. The collaborative_filtering function identifies users with similar interaction histories to the target user by calculating cosine similarity and selecting the top K similar users, where the value of K depends on the diversity level specified by the user. The algorithm then finds candidate items for the user based on the average interaction score of the selected users and eliminates items that the target user has already viewed. The result is a list of top candidate items that is returned as a dataframe.

The content_based_filter function identifies items that the user has positively interacted with and takes into account the user's media type and category preferences. The function ranks candidate recommendations according to these preferences and returns them in sorted order. The final recommendation set is ordered based on the diversity level selected by the user. For low diversity, the recommendation list maintains the same order, and the top 15 items are returned. For medium diversity, a balanced mix of the original top item order and a random selection from the candidate list is used. For high diversity, only the top 25% of the items are retained, and the remaining items are replaced with random items from the user's candidate list.

### Serendipitous recommendations
The personalized recommendation algorithm includes a feature that suggests the last item in the set of recommendations. This last item is chosen based on two factors: its relevance to the user's interests and its potential to be unexpected. The algorithm takes into account the user's tolerance for diversity, ensuring that the last recommended item is not too dissimilar from the user's previous interactions.

### Top-ten content from all the platform.
The code constitutes a basic recommendation engine that leverages a weighted average to provide a list of top recommended items to any user. To do so, the code first creates a DataFrame of all the content available on the platform, which is then sorted based on the number of views and ratings. Subsequently, the function assigns a weight to each item based on its average rating and the number of views it has received. Finally, the DataFrame is sorted again based on the calculated weights, and the top ten items are returned to the user as recommendations.

### Content-based recommendations to find similar content to the last viewed item.
The procedure identifies a group of potential options that closely resemble the most recently observed item. The items are ordered by tags and descriptions, and their level of likeness is measured using the Jaccard and Cosine similarity methods, respectively. The resulting list of recommendations is adjusted depending on the user's preference for diversity. If the user has a low diversity level, the top 15 items from the sorted list are presented as recommendations. For medium diversity, the list includes a combination of the first ordered items and randomly selected items from the first 100 elements of the sorted list. Finally, for high diversity, the list contains a mix of a few first ordered items and the remaining recommendations are randomly selected from the first 200 elements of the sorted list.

### Collaborative-based recommendations to find frequently liked together items.
This piece of code generates suggestions by considering the user's previous liked item. The program searches for other users who also liked that item and then examines which other items those users liked. Based on the frequency of those items being liked together, the program generates a list of top recommendations.

To make the recommendations more personalized, the list is adjusted according to the user's diversity level. For low diversity users, the program returns the top 15 items from the sorted list. For medium diversity users, the program mixes the top ordered items with random items from the original list. Finally, for high diversity users, the program mixes a few top ordered items with the rest being random items from the original list.
