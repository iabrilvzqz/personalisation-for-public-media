#import libraries
from mongo import find_diversity_level, find_all_interactions_history
from stopwords_nl import STOPWORDS

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from collections import Counter
import pandas as pd
import numpy as np
import string
import random
import nltk
import re

from nltk.corpus import stopwords
from nltk.stem.snowball import DutchStemmer

# Loading all users interaction data
full_data = pd.read_csv("full_data.csv")
#full_data = pd.read_csv("/home/iabrilvzqz/mysite/full_data.csv")

# Loading all content data
content = pd.read_csv("content_clean_new.csv")
#content = pd.read_csv("/home/iabrilvzqz/mysite/content_clean_new.csv")

# The descriptions of our dataset are in Dutch, so we need to use the stopwords in Dutch
nltk.download("stopwords")
dutch_stopwords = stopwords.words('dutch')
dutch_stopwords.extend(STOPWORDS)
dutch_stopwords = set(dutch_stopwords)

K_VALUES = {0: 3, 0.5: 5, 1: 7}

# Normalize a dataframe by subtracting the mean value
def norm(dfx):
  dfx["mean"] = dfx.mean(axis = 1)
  norm = dfx.sub(dfx["mean"], axis = 0)
  norm.drop("mean", axis = 1, inplace = True)
  return (norm)


def rename(dfx, string):
  cols = dfx.columns
  new_cols = []
  for col in cols:
    name = str(col) + string
    new_cols.append(name)
  dfx.columns = new_cols
  return dfx


# Tag list counter function
def type_counter(df_series, colab_recomend_df): 
  # Count the number of items by type and then order the colaborative recommendation list from "the most"  favourite 
  # content type to the least favourite content type
  top_tags = df_series.value_counts().sort_values(ascending=False)
  cat_order = pd.CategoricalDtype(categories=top_tags.index.tolist(), ordered=True)
  # Set "Type" column as categorical with defined order
  colab_recomend_df['Type'] = colab_recomend_df['Type'].astype(cat_order)
  # Sort dataframe by "Type" column
  return colab_recomend_df.sort_values('Type')


# Tag list counter function
def tag_counter(df_series, colab_recomend_df):
  colab_recomend_df = colab_recomend_df.copy()
  # Create a list of all tags in the dataframe
  tags = []
  for _, row in df_series.iteritems():
    tags.extend(eval(row))

  # Count the frequency of each tag
  tag_counts = pd.Series(tags).value_counts()
  tag_list = tag_counts.index.to_list()
  
  # create a weight variable that decreases as you move down the tag list
  tag_weight = {tag_list[i]: len(tag_list) - i for i in range(len(tag_list))}

  # count the number of common tags in each row and weight them
  colab_recomend_df['Tags'] = colab_recomend_df['Tags'].apply(lambda x: eval(x))
  colab_recomend_df['common_tags_weighted'] = colab_recomend_df['Tags'].apply(lambda x: sum([tag_weight[tag] for tag in x if tag in tag_list])/len(x))

  # sort the dataframe by the weighted number of common tags in descending order
  colab_recomend_df = colab_recomend_df.sort_values('common_tags_weighted', ascending=False)
  return colab_recomend_df


# Get set from series tags
def get_tag_sets(series):
  return series.str.replace("[\]\']", "", regex=True).str.replace(" ", "").str.split(",").apply(lambda x: set(x) if isinstance(x, list) else x)


# Get jaccard similarity
def get_jaccard_similarity(df, last_seen):
  df = df.copy()
  df["sets"] = get_tag_sets(df["Tags"])
  
  # Tags to compare
  tags = df.loc[df["item_id"]== last_seen, "sets"].iloc[0]
  df["jaccard_similarity"] = df["sets"].apply(lambda x: len(x.intersection(tags))/ len(x.union(tags)))
  
  return df


def clean_text(text):
  # Convert to lowercase
  text = text.lower()
  # Remove punctuation
  text = text.translate(str.maketrans('', '', string.punctuation))
  return text


def get_cosine_similarity(df, last_seen):
  # Descriptions to compare
  df = df.copy()

  stemmer = DutchStemmer()
  df['processed_description'] = df['Description'].apply(lambda x: ' '.join([stemmer.stem(word) for word in clean_text(x).split() if word not in dutch_stopwords]))

  # Calculate cosine similarity
  vectorizer = TfidfVectorizer(max_df=0.4, min_df=20)
  tfidf_matrix = vectorizer.fit_transform(df['processed_description'])

  selected_row_index = df[df['item_id'] == last_seen].index[0]

  df['cosine_similarity'] = cosine_similarity(tfidf_matrix[selected_row_index], tfidf_matrix).flatten()
  
  return df


def track_format(df):
  recs = [{
      "image": row["Small_Image"],
      "large_image": row["Large_Image"],
      "item_id": row["item_id"],
      "title": row["Name"],
      "description":  row["Description"],
      "tags": row["Tags"],
      "category": row["Type"]} for _, row in df.iterrows()]
  return recs


def collaborative_filtering(user_data, user_data_not_norm, user_id, diversity_level):
  k = K_VALUES.get(diversity_level, 3)

  target_user_info = user_data.iloc[user_id].values
  distances = cosine_similarity(user_data, [target_user_info]).flatten()
  distances_with_indices = list(enumerate(distances))
  distances_with_indices.sort(key=lambda x: x[1], reverse=False)
  top_k_indices = [i for i, _ in distances_with_indices[1:k+1]]

  # Get list of items that the target user has not viewed
  target_user_row = user_data_not_norm["view"].iloc[user_id]
  items_to_rate = target_user_row[target_user_row == 0].index

  # Calculate mean interaction score for not viewed items from the group of similar users
  item_ratings = []
  for item in items_to_rate:
    ratings = []
    for user_id in top_k_indices:
      user_row = user_data_not_norm.iloc[user_id]
      rating1 = user_row["rating"][item]
      rating2 = user_row["shared"][item]
      rating3 = user_row["prev"][item]
      ratings.extend([rating1, rating2, rating3])
    
    ratings = [r for r in ratings if r > 0]
    if ratings:
      mean = sum(ratings) / len(ratings)
      item_ratings.append((item, mean))
    
  # Sort items by mean rating and return top recommendations
  item_ratings.sort(key=lambda x: x[1], reverse=True)
  collab_recommendations = [item for item, _ in item_ratings[:150]]

  return pd.DataFrame(collab_recommendations, columns=["item_id"])


# Content based recommendations
def content_based_filter(colab_recomend_df, user_data_not_norm, user_id):
  # Get list of positive interacted content
  target_user_row = user_data_not_norm.iloc[user_id]
  cols_with_1 = target_user_row[target_user_row == 1].index
  tags_rated_pos = [int(re.findall('\d+', str(col))[0]) for col in cols_with_1]
  positive_df = pd.DataFrame(set(tags_rated_pos), columns=["item_id"])

  # Data content enrichment
  colab_recomend_df = colab_recomend_df.merge(content, how = "inner", on = "item_id")
  positive_df = positive_df.merge(content, how = "inner", on = "item_id")
  
  colab_recomend_df = type_counter(positive_df["Type"], colab_recomend_df)
  
  colab_recomend_df = tag_counter(positive_df["Tags"], colab_recomend_df)

  return colab_recomend_df.sort_values(["Type", "common_tags_weighted"], ascending=[True, False])


def get_personalised_recommendations(id):
  # Get level of diversity
  diversity_level = find_diversity_level({"user_id": id})

  # Finding interactions by user id
  interactions = list(find_all_interactions_history({"user_id": id}))

  # Preparing DataFrame
  df = pd.pivot_table(full_data, index = "user_id", columns = "item_id").fillna(0)

  # Transform result to DataFrame
  if interactions:
    interactions = pd.DataFrame(interactions).drop("_id", axis = 1) 
    interactions = interactions.merge(content, on = "item_id")
    
    for _, row in interactions.iterrows():
      if row["type"] == "play":
        df["view"].loc[id, row["item_id"]] = row["value"]
      elif row["type"] == "review":
        df["rating"].loc[id, row["item_id"]] = row["value"]
      elif row["type"] == "share":
        df["shared"].loc[id, row["item_id"]] = row["value"]
      elif row["type"] == "preview":
        df["prev"].loc[id, row["item_id"]] = row["value"]

  # Normalizing ratings
  rating_norm = norm(df["rating"])
  # Normalizing shares
  shared_norm = norm(df["shared"])
  # Normalizing previews
  prev_norm = norm(df["prev"])

  # Union of all datasets
  user_data = pd.concat([df["view"], rating_norm, shared_norm, prev_norm], axis = 1)

  # Collaborative filtering part
  colab_recomend_df = collaborative_filtering(user_data, df, id, diversity_level)

  # Content based filtering part
  content_recomend_df = content_based_filter(colab_recomend_df, df, id)
  
  # Giving recommendations the correct format
  normal_recomendations = track_format(content_recomend_df)

  # Low diversity: List is not modified
  if diversity_level == 0:
    normal_recomendations = normal_recomendations[:15]
  
  # Medium diversity: Mix between random and ordered list
  elif diversity_level == 0.5:
    #Half random, Half not modified
    not_random = [1,2,3,4,5,6,7]
    yes_random = random.sample(range(8, len(normal_recomendations)), 8 if len(normal_recomendations) > 15 else len(normal_recomendations) - 8)
    
    list_ran = not_random + yes_random
    random.shuffle(list_ran)
    normal_recomendations = list(np.array(normal_recomendations)[list_ran])
  
  # High diversity: Order list randomly
  elif diversity_level == 1:
    normal_recomendations = list(np.array(normal_recomendations)[random.sample(range(len(normal_recomendations)), 15)])
  
  return normal_recomendations


def get_serendipity_recommendation(id):
  return get_personalised_recommendations(id)[-1]


def get_last_item_by_interaction(id, interaction_type, filter_type):
  # Finding interactions by user id
  interactions = list(find_all_interactions_history({"user_id": id}))
  
  # Preparing DataFrame
  df = pd.pivot_table(full_data, index="user_id", columns="item_id")
  df = df.fillna(0)
  
  # View dataset
  review = df[interaction_type].reset_index(drop=True)
  
  # Get lists of shows reviewed positive
  cols_with_1 = [col for col in review.columns if review.loc[id, col] == 1]
  cols_user = set(cols_with_1)
  
  # Get last show viewed if there is not data in db
  last_rev = random.sample(cols_user, 1)[0]

  # Searching for last seen in db
  if interactions:
    interactions = pd.DataFrame(interactions).drop("_id", axis=1)
    interactions = interactions.merge(content, left_on="item_id", right_on="item_id")
    
    last = interactions.loc[interactions["type"] == filter_type].sort_values(by="time",ascending=False)
    
    if len(last) > 0:
      last.reset_index(inplace=True, drop=True)
      last_rev = last.loc[0, "item_id"] # Variable with element name
  
  # Frequently review together recommendations
  # Check columns with last element rated
  review_filter = review.loc[review[last_rev] == 1]

  return last_rev, review_filter



def get_recommendations_by_interactions(id):
  last_seen, _= get_last_item_by_interaction(id, "view", "play")
  
  # Get jaccard distance between tags
  content_dis = get_jaccard_similarity(content,last_seen)
  
  # Get cosine distance between descriptions
  content_lev = get_cosine_similarity(content_dis, last_seen).sort_values(by=["jaccard_similarity", "cosine_similarity"], ascending = [False, False])
  
  # Removing same item 
  content_lev = content_lev.loc[content_lev["item_id"] != last_seen]
  
  # Getting recommendations in format
  view_recomendations = track_format(content_lev)[:200]

  # Importing diversity
  diversity_level = find_diversity_level({"user_id": id})

  # Low diversity: List is not modified
  if diversity_level == 0:
    view_recomendations = view_recomendations[:15]
  
  # Medium diversity: Mix between random and ordered list
  elif diversity_level == 0.5:
    view_recomendations = view_recomendations[85:100]
  
  # High diversity: Order list randomly
  elif diversity_level == 1:
    view_recomendations = view_recomendations[180:195]

  return {"recommendations": view_recomendations, "item": content[content["item_id"] == last_seen]["Name"].values[0]}


def get_top_ten_recommendation():
  # Preparing DataFrame
  df = full_data.copy()

  # Order content by number of views and rating
  grouped_df = df.groupby('item_id').agg({'view': ['sum'], 'rating': ['mean']})
  C = grouped_df[('rating', 'mean')].mean()
  m = grouped_df[('view', 'sum')].quantile(0.70)

  R = grouped_df[('rating', 'mean')].values
  v = grouped_df[('view', 'sum')].values
  weights = (R + C) / (v + m)

  grouped_df["weight"] = weights

  grouped_df = grouped_df.sort_values("weight", ascending=False)

  # Get content information to return recommendations to front
  grouped_df = grouped_df.merge(content, how = "inner", on = "item_id")
  normal_recommendations = track_format(grouped_df.head(10))

  return normal_recommendations


def get_recommendations_by_last_reviewed(id):
  last_rev, review_filter = get_last_item_by_interaction(id, "rating", "review")
    
  # Get positive rated items
  items_rated = []
  for col in review_filter:
    for n in review_filter[col]:
      if n == 1:
        items_rated.append(col)
  
  # Count elements
  dic = dict(Counter(items_rated))
  top_tags = pd.DataFrame(dic.items()).sort_values(by=1, ascending=False).reset_index(drop=True)
  
  # Removing the first element (same item)
  top_tags = top_tags.iloc[1:]
  
  # Getting show info
  top_tags = top_tags.merge(content, left_on=0, right_on='item_id')
  
  # Formatting to track
  review_recommendations = track_format(top_tags)
  print("*****", len(review_recommendations))
  # Diversity implementation
  # Getting slider value
  diversity_level = find_diversity_level({"user_id": id}) # call function to get div from id
  print("*****", len(review_recommendations))

  # Low diversity: List is not modified
  if diversity_level == 0:
    review_recommendations = review_recommendations[:15]
  
  # Medium diversity: Mix order
  elif diversity_level == 0.5:
    # Half random, Half not modified
    not_random = [1, 2, 3, 4, 5, 6, 7]
    yes_random = random.sample(range(8, len(review_recommendations)), 8 if len(review_recommendations) > 15 else len(review_recommendations) - 8)
    list_ran = not_random + yes_random
    random.shuffle(list_ran)
    review_recommendations = list(np.array(review_recommendations)[list_ran])
  
  # High diversity: random order
  elif diversity_level == 1:
    review_recommendations = list(np.array(review_recommendations)[random.sample(range(len(review_recommendations)), 15)])
  
  return {"recommendations": review_recommendations, "item": content[content["item_id"] == last_rev]["Name"].values[0]}


def main_recommendations_by_npo():
  normal_recommendations = track_format(content.sample())
  return normal_recommendations