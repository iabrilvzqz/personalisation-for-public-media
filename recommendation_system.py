#import libraries
from mongo import find_diversity_level, find_all_interactions_history

import pandas as pd
import numpy as np
from numpy import dot
from collections import Counter

from random import shuffle
import random
import re

#Loading all users interaction data
pd.set_option('display.max_columns', None)
full_data = pd.read_csv("full_data.csv")
#full_data = pd.read_csv("/home/iabrilvzqz/mysite/full_data.csv")

#Loading all content data
content = pd.read_csv("df_content_clean.csv")
#content = pd.read_csv("/home/iabrilvzqz/mysite/df_content_clean.csv")
content.drop("Unnamed: 0", inplace = True, axis = 1)

# Function to get the cosine distance between two vectors
def cosine_distance(vectora, vectorb):
  up = dot(vectora, vectorb, out=None)
  down = len(vectora) * len(vectorb)
  return up/down


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


#Tag list counter function
def tag_counter(tags_list, df_series):
  for tags in df_series:
    tags = tags.replace("[", "")
    tags = tags.replace("]", "")
    tags = tags.replace("'", "")
    tags = tags.replace(" ", "")
    tags = tags.split(",")
    for t in tags:
      tags_list.append(t)
  return tags_list


def track_format(df):
  recs = []
  for _, row in df.iterrows():
    dic = {"image": row["img_link"],
      "title": row["Name"],
      "description":  row["Description"],
      "tags": row["Genres"],
      "category": row["Type"]}
    recs.append(dic)
  return recs


def collaborative_filtering(user_data, user_data_not_norm, id, div):
  k = 3
  if div == 0.5:
    k = 5
  if div == 1:
    k = 7

  target_user_info = np.squeeze(np.asarray(user_data.iloc[id].to_numpy()))
  distances = []
  
  for n in range(0,len(user_data)):
    if n != id:      
      user_info_2 = np.squeeze(np.asarray(user_data.iloc[n].to_numpy()))
      distances.append((n, cosine_distance(target_user_info, user_info_2)))
  # Get top K most similar users
  top_k_users = sorted(distances, key=lambda x: x[1], reverse=True)[:k]
    
  # Get list of items that the target user has not rated
  user = user_data_not_norm.iloc[id].to_frame().T.iloc[:, :562]
  cols_with_0 = [col for col in user.columns if user[col].all() == 0]
  items_to_rate = set(cols_with_0)
    
  # Calculate mean rating for each item from the group of similar users
  item_ratings = []
  for item in items_to_rate:
    ratings = []
    for user_id, _ in top_k_users:
      user_info = np.squeeze(np.asarray(user_data_not_norm.iloc[user_id].to_numpy()))
      rating = user_info[562 + list(user.columns).index(item)]
      if rating == 1:
        ratings.append(1)
    if len(ratings) > 0:
      item_ratings.append((item, sum(ratings)/len(ratings)))
    
  # Sort items by mean rating and return top recommendations
  item_ratings = sorted(item_ratings, key=lambda x: x[1], reverse=True)
  collab_recommendations = [item for item, _ in item_ratings]
    
  # User history
  cols_with_1 = [col for col in user.columns if user[col].any() == 1]
  user_history = set(cols_with_1)
    
  # Get list of positive interacted content
  user = user_data_not_norm.iloc[id].to_frame().T.iloc[:,562:]
  cols_with_1 = [col for col in user.columns if user.loc[id,col] == 1]
  tags_rated_pos = []
  for words in cols_with_1:
    words = re.sub( '([A-Z])', '', words)
    tags_rated_pos.append(words)
  positive_user = set(tags_rated_pos)
    
  return pd.DataFrame(collab_recommendations, columns=["Name"]), pd.DataFrame(user_history, columns=["Name"]), pd.DataFrame(positive_user, columns=["Name"] ), pd.DataFrame(user_history , columns = ["Name"]),pd.DataFrame( positive_user , columns = ["Name"])


# Content based recommendations
def content_based_filter(colab_recomend_df, user_history_df, positive_df):
  # Data content enrichment
  colab_recomend_df = colab_recomend_df.merge(content, how = "inner", on = "Name")
  user_history_df = user_history_df.merge(content, how = "inner", on = "Name")
  user_positive_df = positive_df.merge(content, how = "inner", on = "Name")

  # Rank by most common tag in the user history
  tags_list= []
  # Count and add tags in views
  tags_list = tag_counter(tags_list, user_history_df["Genres"])
  # Count and add tags in interactions
  tags_list = tag_counter(tags_list, user_positive_df["Genres"])

  # Counting top ocurrence tags
  dic = dict(Counter(tags_list))
  top_tags = pd.DataFrame(dic.items()).sort_values(by = 1, ascending = False).reset_index(drop=True)
  ranking = []
  
  # Make True/False columns of tags
  for index, row in top_tags.iterrows():
    colab_recomend_df["contains_top{}".format(index)] = colab_recomend_df["Genres"].str.contains(row[0])
    ranking.append("contains_top{}".format(index))
  
  return colab_recomend_df.sort_values(ranking, ascending = False).reset_index(drop = True)


def get_personalised_recommendations(id):
  # Get level of diversity
  div = find_diversity_level({"user_id": id})

  # Finding interactions by user id
  interactions = list(find_all_interactions_history({"user_id": id}))

  # Preparing DataFrame
  df = pd.pivot_table(full_data, index = "user_id", columns = "Name")
  df = df.fillna(0)

  # View dataset
  view = df["view"].reset_index(drop = True)
  # Rating dataset
  rating = df["rating"].reset_index(drop = True)
  # Shared dataset
  shared= df["shared"].reset_index(drop = True)
  # Preview dataset
  prev = df["prev"].reset_index(drop = True)
  
  # Transform result to DataFrame
  if interactions:
    interactions = pd.DataFrame(interactions).drop("_id", axis = 1) 
    interactions = interactions.merge(content, left_on = 'title', right_on = 'Name')
    
    for _, row in interactions.iterrows():
      # New play
      if row["type"] == "play":
        view.loc[(view.index == id),  row["Name"]] = row["value"]
      
      # New rating
      if row["type"] == "review":
        rating.loc[(rating.index == id),  row["Name"]] = row["value"]
      
      # New share
      if row["type"] == "share":
        shared.loc[(shared.index == id),  row["Name"]] = row["value"]

      # New preview
      if row["type"] == "preview":
        prev.loc[(prev.index == id),  row["Name"]] = row["value"]

  # Renaming ratings columns
  rename(rating, "RATING")
  # Renaming shared columns
  rename(shared, "SHARED")
  # Renaming preview columns
  rename(prev, "PREV")

  # Getting df with user data not normalized
  user_data_not_norm = pd.concat([view, rating, shared, prev], axis = 1)
  # Normalizing ratings
  rating_norm = norm(rating)
  # Normalizing shares
  shared_norm = norm(shared)
  # Normalizing previews
  prev_norm = norm(prev)

  # Union of all datasets
  user_data = pd.concat([view, rating_norm, shared_norm, prev_norm], axis = 1)
  
  # Collaborative filtering part
  colab_results = collaborative_filtering(user_data, user_data_not_norm, id, div)
  colab_recomend_df, user_history_df, positive_df = colab_results[0], colab_results[1], colab_results[2]

  # Content based filtering part
  content_recomend_df = content_based_filter(colab_recomend_df, user_history_df, positive_df)
  
  # Giving recommendations the correct format
  normal_recomendations = track_format(content_recomend_df)

  # Low diversity: List is not modified
  if div == 0:
    normal_recomendations = normal_recomendations[:15]
  
  # Medium diversity: Mix between random and ordered list
  elif div == 0.5:
    #Half random, Half not modified
    not_random = [1,2,3,4,5,6,7]
    yes_random = random.sample(range(8,len(normal_recomendations)), 8)
    list_ran = not_random + yes_random
    shuffle(list_ran)
    normal_recomendations = list(np.array(normal_recomendations)[list_ran])
  
  # High diversity: Order list randomly
  elif div == 1:
    normal_recomendations = list(np.array(normal_recomendations)[random.sample(range(len(normal_recomendations)), 15)])

  return normal_recomendations


def get_serindipity_recommendation(id):
  return get_personalised_recommendations(id)[-1]


def get_recommendations_by_interactions(id):
  # Finding interactions by user id
  interactions = list(find_all_interactions_history({"user_id": id}))

  # Preparing DataFrame
  df = pd.pivot_table(full_data, index = "user_id", columns = "Name")
  df = df.fillna(0)

  # View dataset
  view = df["view"].reset_index(drop = True)

  # Get lists of shows viewed
  cols_with_1 = [col for col in view.columns if view[col].any() == 1]
  cols_user = set(cols_with_1)
  
  #Get last show view if there is not data in db
  last_seen = random.sample(cols_user, 1)[0]

  # Searching for last seen in db
  # Transform result to DataFrame
  
  if interactions:
    interactions = pd.DataFrame(interactions).drop("_id", axis = 1) 
    interactions = interactions.merge(content, left_on = 'title', right_on = 'Name')
    last = interactions.loc[interactions["type"] == "play"].sort_values(by = "time", ascending = False)
    
    if len(last) > 0:
      last.reset_index(inplace =True, drop=True)
      last_seen = last.loc[0,"title"] # Variable with element name

  # Start content similarity based recom
  last_df = pd.DataFrame(data={'Name': [last_seen]}).merge(content, how = "inner", on = "Name")
  
  # Rank by most common tag in the user history
  tags_list= []
  # Count and add tags in views
  tags_list = tag_counter(tags_list,last_df["Genres"])
  dic = dict(Counter(tags_list))
  top_tags = pd.DataFrame(dic.items()).sort_values(by=1, ascending = False).reset_index(drop=True)
  con = content.copy()
  ranking = []

  for index, row in top_tags.iterrows():
    # Make True/False columns of all tags to rank them
    con["contains_top{}".format(index)] = con["Genres"].str.contains(row[0])
    ranking.append("contains_top{}".format(index))
  
  sel = con.sort_values(ranking, ascending = False).reset_index(drop=True)
  
  # Removing same item
  sel = sel.loc[sel["Name"]!= last_seen]
  view_recomendations = track_format(sel)

  div = find_diversity_level({"user_id": id})

  # Low diversity: List is not modified
  if div == 0:
    view_recomendations = view_recomendations[:15]
  
  # Medium diversity: Mix between random and ordered list
  elif div == 0.5:
    view_recomendations = view_recomendations[35:50]
  
  # High diversity: Order list randomly
  elif div == 1:
    view_recomendations = view_recomendations[100:115]

  return {"recommendations": view_recomendations, "item": last_seen}


def get_top_ten_recommendation():
  # Preparing DataFrame
  df = full_data.copy()

  # Order content by number of views and rating
  grouped_df = df.groupby('Name').agg({'view': ['sum'], 'rating': ['mean']})
  C = grouped_df[('rating', 'mean')].mean()
  m = grouped_df[('view', 'sum')].quantile(0.70)

  weights = []

  for _, row in grouped_df.iterrows():
    R = row[('rating', 'mean')]
    v = row[('view', 'sum')]
    weights.append( (R + C) / (v + m) )
    
  grouped_df["weight"] = weights

  grouped_df = grouped_df.sort_values("weight", ascending=False)

  # Get content information to return recommendations to front
  grouped_df = grouped_df.merge(content, how = "inner", on = "Name")
  normal_recommendations = track_format(grouped_df.head(10))

  return normal_recommendations


def get_recommendations_by_last_reviewed(id):
  # Finding interactions by user id
  interactions = interactions = list(find_all_interactions_history({"user_id": id}))
  # Preparing DataFrame
  df = pd.pivot_table(full_data, index="user_id", columns = "Name")
  df = df.fillna(0)
  
  # View dataset
  review = df["rating"].reset_index(drop = True)
  
  #Get lists of shows reviewed positive
  cols_with_1 = [col for col in review.columns if review.loc[id,col] == 1]
  cols_user = set(cols_with_1)
  
  # Get last show viewed if there is not data in db
  last_rev = random.sample(cols_user, 1)[0]
  
  # Searching for last seen in db
  if interactions:
    interactions = pd.DataFrame(interactions).drop("_id", axis=1) 
    interactions = interactions.merge(content, left_on='title', right_on='Name')
    
    last = interactions.loc[interactions["type"] == "review"].sort_values(by="time",ascending=False)
    
    if len(last)>0:
      last.reset_index(inplace =True, drop=True)
      last_rev = last.loc[0,"title"] # Variable with element name

  
  # Frequently review together recommendations
  # Check columns with last element rated
  review_filter = review.loc[review[last_rev] == 1]
  
  # Get positive rated items
  items_rated = []
  for col in review_filter:
    for n in review_filter[col]:
      if n == 1:
        items_rated.append(col)
  
  # Count elements
  dic = dict(Counter(items_rated))
  top_tags = pd.DataFrame(dic.items()).sort_values(by=1, ascending = False).reset_index(drop=True)
  # Removing the first element (same item)
  top_tags = top_tags.iloc[1:]
  
  # Getting show info
  top_tags = top_tags.merge(content, left_on=0, right_on='Name')
  
  # Formating to track
  review_recomendations = track_format(top_tags )

  # Diversity implementation
  # Getting slider value
  div = div = find_diversity_level({"user_id": id}) #call function to get div from id
  
  # Low diversity: List is not modified
  if div == 0:
    review_recomendations = review_recomendations[:15]
  
  # Medium diversity: Mix order
  if div == .5:
    #Half random, Half not modified
    not_random = [1,2,3,4,5,6,7]
    yes_random = random.sample(range(8,len(review_recomendations)), 8)
    list_ran = not_random + yes_random
    shuffle(list_ran)
    review_recomendations = list(np.array(review_recomendations)[list_ran])

  # High diversity: random order
  if div == 1:
    review_recomendations = list(np.array(review_recomendations)[random.sample(range(len(review_recomendations)), 15)])
  

  return {"recommendations": review_recomendations, "item": last_rev}


def main_track_format(df):
  recs = []
  for _, row in df.iterrows():
    dic = {"image": row["img_link"],
      "title": row["Name"],
      "description":  row["Description"],
      "tags": row["Genres"],
      "category": row["Type"],
      "large_image": row["large_image"]}
    recs.append(dic)
  return recs

def main_recommendations_by_npo():
  names = ["downton abbey", "sanditon", "bloedbroeders", "project rembrandt", "gevoel voor tumor"]
  images = ["downton_abbey.jpeg", "sanditon.jpeg", "bloedbroeders.jpeg", "project_rembrandt.png", "gevoel_voor_tumor.png"]

  df = pd.DataFrame(list(zip(names, images)), columns=["Name", "large_image"])
  df = df.merge(content, how = "inner", on = "Name")

  normal_recommendations = main_track_format(df.sample())

  return normal_recommendations

