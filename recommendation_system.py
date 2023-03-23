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
def cosine_distance(vectora, vectorb ):
  up = dot(vectora, vectorb, out=None)
  down = len(vectora) * len(vectorb)
  return up/down

#Normalize df function
def norm(dfx):
  dfx["mean"] = dfx.mean(axis = 1)
  # Normalizing by substracting the mean
  norm = dfx.sub(dfx["mean"], axis = 0)
  norm.drop("mean", axis = 1, inplace = True)
  return (norm)

#rename_columns function
def rename(dfx,string):
  cols = dfx.columns
  new_cols = []
  for col in cols:
    name = str(col) + string
    new_cols.append(name)
  dfx.columns = new_cols
  return dfx

#Tag list countes function
def tag_counter(tags_list,df_series):
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

#Colaborative filtering function
def colab(user_data, user_data_not_norm, id):
  distance,user_id_number, user_info = [], [], np.squeeze(np.asarray(user_data.iloc[id].to_numpy()))
  #Create cosine distances
  for n in range(0,len(user_data)):
    if n != id:      
      user_info_2 = np.squeeze(np.asarray(user_data.iloc[n].to_numpy()))
      #If cosine distance is bigger, objects are similar
      distance.append(cosine_distance(user_info,user_info_2 ))
      user_id_number.append(n)
  df = pd.DataFrame(zip(distance,user_id_number), columns = ["distance", "user_id"])
  #Getting the most similar user id
  sorted = df.sort_values(by="distance",ascending = False)
  sorted = sorted.reset_index()
  similar = sorted.loc[0,"user_id"]
  user = user_data.iloc[id].to_frame().T.iloc[:,:562]

  # get the names of the columns that have a 1 in the value
  cols_with_1 = [col for col in user.columns if user[col].any() == 1]
  cols_user = set(cols_with_1)
  
  #Get list of similar user
  user_sim = user_data.iloc[similar].to_frame().T.iloc[:,:562]
  
  # get the names of the columns that have a 1 in the value
  cols_with_1 = [col for col in user_sim.columns if user_sim[col].any() == 1]
  cols_sim = set(cols_with_1)
  dif = cols_sim - cols_user 
  
  #Getting diference with similar user
  colab_recomend = dif
  
  #User history
  user_history = cols_user 

  #Get list of positive interacted content
  user = user_data_not_norm.iloc[id].to_frame().T.iloc[:,562:]
  # get the names of the columns that have a 1 in the value
  cols_with_1 = [col for col in user.columns if user.loc[id,col] == 1]
  
  #removing capital letters and appending positive interactions
  tags_rated_pos = []
  for words in cols_with_1:
    words = re.sub( '([A-Z])', '', words )
    tags_rated_pos.append(words)
  positive_user = set(tags_rated_pos)

  #Making df with the collab recomendations
  return pd.DataFrame(colab_recomend, columns = ["Name"] ), pd.DataFrame(user_history , columns = ["Name"]),pd.DataFrame( positive_user , columns = ["Name"])


#Content based recoms
def content_filter(colab_recomend_df, user_history_df, positive_df):
  #Data content enrichment
  colab_recomend_df = colab_recomend_df.merge(content, how = "inner", on = "Name")
  user_history_df = user_history_df.merge(content, how = "inner", on = "Name")
  user_positive_df = positive_df.merge(content, how = "inner", on = "Name")

  #Rank by most common tag in the user history
  tags_list= []
  #Counta and add tags in views
  tags_list = tag_counter(tags_list,user_history_df["Genres"])
  #Count and add tags in interactions
  tags_list = tag_counter(tags_list,user_positive_df["Genres"])

  # Counting top ocurrence tags
  dic = dict(Counter(tags_list))
  top_tags = pd.DataFrame(dic.items()).sort_values(by=1, ascending = False).reset_index(drop=True)
  ranking = []
  
  # Make True/False columns of tags
  for index, row in top_tags.iterrows():
    colab_recomend_df["contains_top{}".format(index)] = colab_recomend_df["Genres"].str.contains(row[0])
    ranking.append("contains_top{}".format(index))
  
  return colab_recomend_df.sort_values(ranking,
              ascending = False).reset_index(drop=True)


def get_recommendations(id):
  # Finding interactions by user id
  interactions = list(find_all_interactions_history({"user_id": id}))

  # Preparing DataFrame
  df = pd.pivot_table(full_data, index="user_id", columns = "Name")
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
    interactions = pd.DataFrame(interactions).drop("_id", axis=1) 
    interactions = interactions.merge(content, left_on='title', right_on='Name')
    
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
  rename(rating,"RATING")
  # Renaming shared columns
  rename(shared,"SHARED")
  # Renaming preview columns
  rename(prev,"PREV")

  #Getting df with user data not normalized
  user_data_not_norm = pd.concat([view,rating,shared,prev, ], axis = 1)
  #Normalizing ratings
  rating_norm = norm(rating)
  #Normalizing shares
  shared_norm = norm(shared)
  #Normalizing previews
  prev_norm = norm(prev)

  #Union of all datasets
  user_data = pd.concat([view, rating_norm, shared_norm, prev_norm], axis = 1)
  
  # Collaborative filtering part
  colab_recomend_df,user_history_df,positive_df = colab(user_data,user_data_not_norm,id)[0], colab(user_data,user_data_not_norm,id)[1],colab(user_data,user_data_not_norm,id)[2]

  # Content based filtering part
  content_recomend_df = content_filter(colab_recomend_df,user_history_df,  positive_df)
  
  #Giving recommendations the correct format
  normal_recomendations = track_format(content_recomend_df)
  div = find_diversity_level({"user_id": id})

  #LOW DIV.- List is not modified
  if div == 0:
    normal_recomendations = normal_recomendations[:15]
  
  #MEDIUM DIV.- Mix order
  if div == .5:
    #Half random, Half not modified
    not_random = [1,2,3,4,5,6,7]
    yes_random = random.sample(range(8,len(normal_recomendations)), 8)
    list_ran = not_random + yes_random
    shuffle(list_ran)
    normal_recomendations = list(np.array(normal_recomendations)[list_ran])
  
  if div == 1:
    normal_recomendations = list(np.array(normal_recomendations)[random.sample(range(len(normal_recomendations)), 15)])

  return normal_recomendations