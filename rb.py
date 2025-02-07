# -*- coding: utf-8 -*-
"""RB.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1G4IwFwe4-3ffXb1iyNH3K6XaQlJyhBmu
"""

#imports
!pip install nfl_data_py
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
import nfl_data_py as nfl

years = [year for year in range(1999, 2023)]
data = nfl.import_seasonal_data(years)
#a.cols()

data = nfl.clean_nfl_data(data)
list(data)

cols = ['season','position', 'player_id','games','fantasy_points_ppr', 'receptions', 'targets', 'receiving_yards', 'receiving_tds', 'carries',
 'rushing_yards',
 'rushing_tds', "rushing_first_downs"]

dfRB = data[cols]
dfRB.head()

#kill nulls

dfRB = dfRB.replace(r'^\s*$', np.nan, regex=True)
dfRB = dfRB.dropna()
np.sum(dfRB.isnull())
dfRB.head()

#for item in position:
#dfWR.head()
#dfWR{}

#df = pd.DataFrame()
#df.loc[0] = dfWR.loc[0]
#d = {}
#for item in dfWR[1:]:
#  print(item)
  #if item["position"][0:3] == "WR":
    #df.loc[len(df)] = item

#df_filtered = dfWR.loc[dfWR['position'].str.contains('WR')]

dfRB = dfRB[dfRB["position"].str.contains("RB", na=False)]
#df_filtered
dfRB.drop("position", axis=1)

#make player id faster, map player id string to int
from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
le.fit(dfRB["player_id"])
dfRB["player_id"] = le.transform(dfRB["player_id"])
dfRB.shape
dfRB.head()

#this code block is just to look at correlation
dfRB2 = dfRB.drop(['position', "player_id"], axis=1)
#dfWR2 = dfWR.drop()
dfRB2.corr()[['fantasy_points_ppr']]
#dfWR2.head()

#possibly add a career average to add accuracy

#add a season number
#index_of_first_match = dfWR.index[0]
#index_of_first_match
#for

#start at the end
# if previous item[player id] has the same as


#another thing to figure out - can i input previous seasons as matrices
#can i make a previous seasons array?

#df.insert


#add next game
#for item in df:
#  if item.next[""]

#  df insert next season points
df = dfRB.drop("position", axis=1)
df.head()
df = df.reset_index()
df = df.drop(["index"], axis=1)
for i, row in df.iterrows():
    #add what number season it is
    index_of_first_match = df.loc[:i, "player_id"].ge(row["player_id"]).idxmax()
    count = i - index_of_first_match
    df.at[i, "Season #"] = count # 0 based

    #df.at[i, "Career total"] = np.sum() # 0 based

    #will give index out of bounds error
    if i < len(df) - 1:
      nextRow = df.iloc[i+1]
      #print(row["player_id"])
      #print(nextRow["player_id"])
      if row["player_id"] == nextRow["player_id"]:
        df.at[i, "next_season_fpts_ppr"] = nextRow["fantasy_points_ppr"]
        #print("goat")
      else:
        #df.drop(row)
        df.at[i, "next_season_fpts_ppr"] = np.NaN

'''
for i, row in df.iterrows():
if next(row)["player_id"] == row["player_id"]:
      df.at[i, "next_season_fpts_ppr"] = next(row)["fantasy_points_ppr"]
    else:
      #drop row
      df.drop(row)
'''
df.head()
#df.shape

#!!! ADD A PLAYER AGE TO CATEGORY

from sklearn.model_selection import train_test_split


#DONT FORGET TO DROP NAN ROWS
data = df.dropna()

#dropping columns that are irrelevant to model
X = data.drop(columns=["next_season_fpts_ppr", "season", "player_id"])
y = data["next_season_fpts_ppr"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

from sklearn.metrics import mean_squared_error
from sklearn.linear_model import LinearRegression
#reg = LinearRegression().fit(X, y)
linear_model = LinearRegression()
linear_model.fit(X_train, y_train)
predictions = linear_model.predict(X_test)

#Sklearn's LinearRegression also provides various attributes such as coef_ and intercept_
#that allow you to access the slope and intercept of the linear regression line respectively.

# ^ those above allow me to see the impact of each input feature

import matplotlib.pyplot as plt #MUST REMOVE
from sklearn.metrics import mean_absolute_error #should be mean squared error
errors = []

X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=.2)
X_train, X_val, y_train, y_val = train_test_split(X_train,y_train,test_size=.1)
'''
for iter in np.arange(250, 2000, 250):
  # STEP 1: Initialization
  linear_model = LinearRegression() #there is no hyperparameter here to tune
  linear_model.fit(X_train, y_train)
  predictions = linear_model.predict(X_val)

  # STEP 4: Evaluation
  errors.append(mean_squared_error(y_val, predictions))
'''
linear_model = LinearRegression() #there is no hyperparameter here to tune
linear_model.fit(X_train, y_train)
predictions = linear_model.predict(X_val)
print(mean_squared_error(y_val, predictions))
#plt.plot(np.arange(250, 2000, 250),errors)
#plt.show

#mean squared error is around 3500-4000 and changes every time, which is a good sign because of my validation set
#+/- 60 fantasy points... per WR... the highest WR how do i contextualize this?

X_test.head()

#next step - model makes a prediction for real players that we know in 2022 season

#testData =
#predictions = linear_model.predict(X_val)
cols = ['player_name', 'season','position', 'player_id','games','fantasy_points_ppr', 'receptions', 'targets', 'receiving_yards', 'receiving_tds', 'carries',
 'rushing_yards',
 'rushing_tds', "rushing_first_downs"]

data2 = nfl.import_seasonal_data([year for year in range(1999, 2023)])
#a.cols()

data = nfl.clean_nfl_data(data2)

df = data[cols]
df = df.replace(r'^\s*$', np.nan, regex=True)
df = df.dropna()

le = LabelEncoder()
le.fit(df["player_id"])
df["player_id"] = le.transform(df["player_id"])


#  df insert next season points
df = df[df["position"].str.contains("RB", na=False)]
df.drop("position", axis=1)

df = df.reset_index()
df = df.drop(["index"], axis=1)

#season number is still broken
for i, row in df.iterrows():
    #add what number season it is
    index_of_first_match = df.loc[:i, "player_id"].ge(row["player_id"]).idxmax()
    count = i - index_of_first_match
    df.at[i, "Season #"] = count # 0 based
#print(df['season'])

#df2 = df.

df2 = df[df['season'] == 2022] #THIS IS GIVING A LIST NOT PANDAS DATAFRAME
df = df2
#df.head()
#df = pd.DataFrame(df2)
#df = df[df['season']==2022] #this might be broken. i need to import more than 2022 data to get season working

cols2 = ['games','fantasy_points_ppr', 'receptions', 'targets', 'receiving_yards', 'receiving_tds', 'carries',
 'rushing_yards',
 'rushing_tds', "rushing_first_downs", "Season #"]

subset = df[cols2]
#create a new subset of cols
#create a lookup table that maps player id to name. will be printed later
#need to create a new map function that


predictions = linear_model.predict(subset)
df['Prediction']=predictions
#mydict = {'Prediction': predictions}
#newdf = pd.DataFrame.from_dict(mydict)
#final = pd.concat([df, newdf], axis=1)
#final = final.dropna()

df = df.sort_values(by='Prediction', ascending=False)
df = df.reset_index()
df.head(100)


#add the strength of quarterback
#here's what i'm going to do next is a totally valid part of presentaiton, don't go down the wrong rabbit holes
#3 graphs - bar chart, fantasy points predictive actual easy to digest for fantasy points
#outline for presentation
#dcectent theme, outlines for slides, start to put title slides
#be mindful of not many words on the slide
# positions, qb, rb, wr
# 1minute per slide, 30 slides
#start making the bar chart now
#df2.head()
#only major error is that the season # isn't working