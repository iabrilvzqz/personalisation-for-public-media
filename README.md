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

### 1. Personalised Recommendations
This algorithm provides personalized recommendations to users based on their interaction history with items. It is a combination of two different filtering techniques: **collaborative filtering** and **content-based filtering**.

1. The **collaborative_filtering** function is responsible for finding similar users to the target user based on their interaction history with items. It calculates cosine similarity between users, finds the top K similar users, and then recommends items to the target user based on the items that the target user has not viewed. The function returns a dataframe with the top recommended items.
1. The **content_based_filter** function is responsible for enriching the recommendations from the collaborative_filtering function with content-based recommendations. It finds the items that the user has positively interacted with in the non-normalized user data, counts the number of items by type (Programma, Film, Serie, Documentaire), sorts the collaborative recommendations by the ranking of content type of the target, and returns the sorted recommendations.

The final results are retrieved depending on the diversity level chosen by the user.

## 2. Serendipity
This algorithm provides one item that is diverse and relevant to the user. It uses the personalised recommendations function to retrieve the most recommended item based on user interaction history, and then checks if it is diverse enough by comparing the item's content type to the user's preferred content types. If the item is not diverse enough, it looks for the second most recommended item and repeats the process until it finds an item that is both diverse and relevant. The function returns the diverse and relevant item.

## 3. Top-ten content from all the platform
This code implements a recommendation engine that returns the top ten recommended items to any user by using a weighted average. It prepares a DataFrame of all the content on the platform and orders it by the number of views and rating. The function calculates a weight for each item based on the average rating and the number of views. The resulting DataFrame is sorted by weight, and the top ten items are returned.

## 4. Recommendations based on viewed content by the user
This code generates personalized recommendations for a user based on their past interactions with the platform. The function calculates the similarity between the tags of the last item the user interacted with and the tags of all other items in the dataset using the Jaccard similarity metric. It also calculates the cosine similarity between the descriptions of the last item the user interacted with and the descriptions of all other items in the dataset.

The resulting list of recommendations is modified based on the user's diversity level. If the user has low diversity, the top 15 items from the sorted list are returned. If the user has medium diversity, a mix of random and ordered items from the list are returned. Finally, if the user has high diversity, a randomly ordered list of items from the bottom of the sorted list are returned.

## 5. Frequently liked together items
This code generates recommendations based on the last item that the user liked. The function searches for other users who liked the same item and then looks for the other items that those users also liked. The function returns a list of the top recommended items based on how frequently they are liked together.
