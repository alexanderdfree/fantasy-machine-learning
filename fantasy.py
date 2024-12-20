# -*- coding: utf-8 -*-
"""Fantasy.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1tKlS8g-yJ-l0GGrgmqvlLfCouVlbsAlF
"""

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from google.colab import drive
drive.mount('/content/drive')
PATH = '/content/drive/My Drive/'
#data = pd.read_csv(PATH + "38274-0001-Data.csv")

#cell 1 - import, view, clean data

#reddit paid course w/ data https://www.fantasyfootballdatapros.com/course/purchase?discount=15OFF
#https://www.pro-football-reference.com/
#https://fantasydata.com/nfl/fantasy-football-leaders


#clean data, etc

#linear prediction of seasonal fantasy points (maybe per game to avoid injury issues) based on previous season performance
#function as a draft analyzer
#https://github.com/fantasydatapros/data

#split train test data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

#linear regression model

from sklearn.linear_model import LinearRegression
logistic_model = LinearRegression()
logistic_model.fit(X_train, y_train)
predictions = logistic_model.predict(X_test)


#figure out how to calculate accuracy

#TRANSFORM + DISCRETIZE DATA
from sklearn.preprocessing import LabelEncoder

le = LabelEncoder()
#discretize

le.fit(data["GENDER"])
print(le.classes_)
data["GENDER"] = le.transform(data["GENDER"])
#print(le.inverse_transform([1]))
le.fit(data["RACE_REC"])
print(le.classes_)
data["RACE_REC"] = le.transform(data["RACE_REC"])

le.fit(data["OFFENSE_TYPE"])
print(le.classes_)
data["OFFENSE_TYPE"] = le.transform(data["OFFENSE_TYPE"])
print(le.inverse_transform([1]))
le.fit(data["COUNTY"])
print(le.classes_)
data["COUNTY"] = le.transform(data["COUNTY"])

le.fit(data["CRIME_RECODE"])
print(le.classes_)
data["CRIME_RECODE"] = le.transform(data["CRIME_RECODE"])

#le.fit(data["CC_DOMCHARGETYPE_END"])
#print(le.classes_)
#data["CC_DOMCHARGETYPE_END"] = le.transform(data["CC_DOMCHARGETYPE_END"])

#drop missing data columns
data = data.drop(columns=["CC_DOMCHARGETYPE_END"])
data = data.drop(columns=["DC_ALLDROP"])
data = data.drop(columns=["CONV_CC"])
data = data.drop(columns=["NOCONV_CC"])
data = data.drop(columns=["END_IN_DC"])

#drop "answer" columns
data = data.drop(columns=["DC_CONV"])
data = data.drop(columns=["FEL_CONV"])
#data = data.drop(columns=["FEL_GJ"])
data = data.drop(columns=["MISD_CONV"])
data = data.drop(columns=["ANY_INC"])

#drop irrelevant
#data = data.drop(columns=["YEAR_DCDISP"])
#data = data.drop(columns=["COUNTY"])

#data.head()

#split into train and test data
from sklearn.model_selection import train_test_split
X = data.drop(columns=["ANY_CONVICT"])
y = data["ANY_CONVICT"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
#data.shape
data.head()
data.shape

#visualization
import matplotlib.pyplot as plt
import seaborn as sns

#plt.figure(figsize=(12,10))
#sns.scatterplot(data['RACE_REC'], data['ANY_CONVICT'], hue=data['GENDER'])
#plt.show()
print(data['OFFENSE_TYPE'].value_counts())
plt.figure(figsize=(10,6))
plt.hist(data['OFFENSE_TYPE'], edgecolor = 'black')
plt.xlabel('Offense Type')
#plt.show()
#data.describe()
data_na = data.replace(r'^\s*$', np.nan, regex=True)
np.sum(data_na.isnull())

#true_b = y_test[np.where(np.array(X_test["RACE_REC"])==0)[0]]
#true_w = y_test[np.where(np.array(X_test["RACE_REC"])==1)[0]]
np.where(np.array(X_test["RACE_REC"])==0)[0]
y_test

#logistic regression preliminary model
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
logistic_model = LogisticRegression(max_iter=1000)
logistic_model.fit(X_train, y_train)
predictions = logistic_model.predict(X_test)

from sklearn.metrics import accuracy_score

score = accuracy_score(y_test, predictions)
print('Logistic Regression Model Accuracy: {:.2%}'.format(score))

true_b = np.array(y_test)[np.where(np.array(X_test["RACE_REC"])==0)[0]]
true_w = np.array(y_test)[np.where(np.array(X_test["RACE_REC"])==1)[0]]

pred_b = predictions[np.where(np.array(X_test["RACE_REC"]==0))[0]]
pred_w = predictions[np.where(np.array(X_test["RACE_REC"]==1))[0]]

score = accuracy_score(true_b, pred_b)
print('Black Model Accuracy: {:.2%}'.format(score))

score = accuracy_score(true_w, pred_w)
print('White Model Accuracy: {:.2%}'.format(score))

#Combined stats
cm = confusion_matrix(y_test, predictions)
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=["not convicted", "convicted"])
disp.plot(cmap='Purples');
#Black
cm1 = confusion_matrix(true_b, pred_b)
disp1 = ConfusionMatrixDisplay(confusion_matrix=cm1, display_labels=["not convicted", "convicted"])
disp1.plot(cmap='Blues');
#White
cm2 = confusion_matrix(true_w, pred_w)
disp2 = ConfusionMatrixDisplay(confusion_matrix=cm2, display_labels=["not convicted", "convicted"])
disp2.plot(cmap='Reds');

#fp/(tp+tn+fp+fn) #% false positives
fpB = cm1[0][1]/len(true_b)
#fn/(tp+tn+fp+fn) #% false negatives
fnB = cm1[1][0]/len(true_b)

#fp/(tp+tn+fp+fn) #% false positives
fpW = cm2[0][1]/len(true_w)
#fn/(tp+tn+fp+fn) #% false negatives
fnW = cm2[1][0]/len(true_w)

print("Black FP %: " + str(fpB * 100) + "%")
print("Black FN %: " + str(fnB * 100) + "%")
print("White FP %: " + str(fpW * 100) + "%")
print("White FN %: " + str(fnW * 100) + "%")

#random forest preliminary model
from sklearn.ensemble import RandomForestClassifier

classifier = RandomForestClassifier(max_depth=11, random_state=0)
classifier.fit(X_train, y_train)
y_pred = classifier.predict(X_test)

score = accuracy_score(y_test, y_pred)
print('Random Forest Model Accuracy: {:.2%}'.format(score))

true_b = np.array(y_test)[np.where(np.array(X_test["RACE_REC"])==0)[0]]
true_w = np.array(y_test)[np.where(np.array(X_test["RACE_REC"])==1)[0]]

pred_b = y_pred[np.where(np.array(X_test["RACE_REC"]==0))[0]]
pred_w = y_pred[np.where(np.array(X_test["RACE_REC"]==1))[0]]

score = accuracy_score(true_b, pred_b)
print('Black Model Accuracy: {:.2%}'.format(score))

score = accuracy_score(true_w, pred_w)
print('White Model Accuracy: {:.2%}'.format(score))

#Combined stats
cm = confusion_matrix(y_test, y_pred)
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=["not convicted", "convicted"])
disp.plot(cmap='Purples');
#Black
cm1 = confusion_matrix(true_b, pred_b)
disp1 = ConfusionMatrixDisplay(confusion_matrix=cm1, display_labels=["not convicted", "convicted"])
disp1.plot(cmap='Blues');
#White
cm2 = confusion_matrix(true_w, pred_w)
disp2 = ConfusionMatrixDisplay(confusion_matrix=cm2, display_labels=["not convicted", "convicted"])
disp2.plot(cmap='Reds');

#fp/(tp+tn+fp+fn) #% false positives
fpB = cm1[0][1]/len(true_b)
#fn/(tp+tn+fp+fn) #% false negatives
fnB = cm1[1][0]/len(true_b)

#fp/(tp+tn+fp+fn) #% false positives
fpW = cm2[0][1]/len(true_w)
#fn/(tp+tn+fp+fn) #% false negatives
fnW = cm2[1][0]/len(true_w)

print("Black FP %: " + str(fpB * 100) + "%")
print("Black FN %: " + str(fnB * 100) + "%")
print("White FP %: " + str(fpW * 100) + "%")
print("White FN %: " + str(fnW * 100) + "%")

#knn preliminary model

from sklearn.neighbors import KNeighborsClassifier

knn = KNeighborsClassifier(n_neighbors = 15)

knn.fit(X_train, y_train)
y_pred = knn.predict(X_test)

# Predictions and Evaluations
# Let's evaluate our KNN model !
#from sklearn.metrics import classification_report, confusion_matrix
#print(confusion_matrix(y_test, pred))
#print(classification_report(y_test, pred))

score = accuracy_score(y_test, y_pred)
print('KNN Model Accuracy: {:.2%}'.format(score))

true_b = np.array(y_test)[np.where(np.array(X_test["RACE_REC"])==0)[0]]
true_w = np.array(y_test)[np.where(np.array(X_test["RACE_REC"])==1)[0]]

pred_b = y_pred[np.where(np.array(X_test["RACE_REC"]==0))[0]]
pred_w = y_pred[np.where(np.array(X_test["RACE_REC"]==1))[0]]

score = accuracy_score(true_b, pred_b)
print('Black Model Accuracy: {:.2%}'.format(score))

score = accuracy_score(true_w, pred_w)
print('White Model Accuracy: {:.2%}'.format(score))

#Combined stats
cm = confusion_matrix(y_test, y_pred)
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=["not convicted", "convicted"])
disp.plot(cmap='Purples');
#Black
cm1 = confusion_matrix(true_b, pred_b)
disp1 = ConfusionMatrixDisplay(confusion_matrix=cm1, display_labels=["not convicted", "convicted"])
disp1.plot(cmap='Blues');
#White
cm2 = confusion_matrix(true_w, pred_w)
disp2 = ConfusionMatrixDisplay(confusion_matrix=cm2, display_labels=["not convicted", "convicted"])
disp2.plot(cmap='Reds');

#fp/(tp+tn+fp+fn) #% false positives
fpB = cm1[0][1]/len(true_b)
#fn/(tp+tn+fp+fn) #% false negatives
fnB = cm1[1][0]/len(true_b)

#fp/(tp+tn+fp+fn) #% false positives
fpW = cm2[0][1]/len(true_w)
#fn/(tp+tn+fp+fn) #% false negatives
fnW = cm2[1][0]/len(true_w)

print("Black FP %: " + str(fpB * 100) + "%")
print("Black FN %: " + str(fnB * 100) + "%")
print("White FP %: " + str(fpW * 100) + "%")
print("White FN %: " + str(fnW * 100) + "%")

import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error
errors = []

X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=.2)
X_train, X_val, y_train, y_val = train_test_split(X_train,y_train,test_size=.1)

for iter in np.arange(250, 2000, 250):
  # STEP 1: Initialization
  logistic_model = LogisticRegression(max_iter=iter)
  logistic_model.fit(X_train, y_train)
  predictions = logistic_model.predict(X_val)

  # STEP 4: Evaluation
  errors.append(mean_absolute_error(y_val, predictions))

plt.plot(np.arange(250, 2000, 250),errors)
plt.show

names = ["newton-cg", "lbfgs", "liblinear", "sag", "saga"]
errors = []

for s in names:
  # STEP 1: Initialization
  logistic_model = LogisticRegression(solver=s)
  logistic_model.fit(X_train, y_train)
  predictions = logistic_model.predict(X_val)

  # STEP 4: Evaluation
  errors.append(mean_absolute_error(y_val, predictions))

plt.plot(names,errors)
plt.show

errors = []

X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=.2)
X_train, X_val, y_train, y_val = train_test_split(X_train,y_train,test_size=.1)

for depth in range(1,16):
  # STEP 1: Initialization
  random_forest_model = RandomForestClassifier(max_depth=depth, random_state=0)

  # STEP 2: Training
  random_forest_model.fit(X_train, y_train)

  # STEP 3: Prediction
  predictions = random_forest_model.predict(X_val)

  # STEP 4: Evaluation
  errors.append(mean_absolute_error(y_val, predictions))

plt.plot(range(1,16),errors)
plt.show

errors = []

X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=.2)
X_train, X_val, y_train, y_val = train_test_split(X_train,y_train,test_size=.1)

for e in np.arange(50, 150, 10):
  # STEP 1: Initialization
  random_forest_model = RandomForestClassifier(max_depth = 11, n_estimators=e, random_state=0)

  # STEP 2: Training
  random_forest_model.fit(X_train, y_train)

  # STEP 3: Prediction
  predictions = random_forest_model.predict(X_val)

  # STEP 4: Evaluation
  errors.append(mean_absolute_error(y_val, predictions))

plt.plot(np.arange(50, 150, 10),errors)
plt.show

errors = []

for neighbors in range(1,30):
  # STEP 1: Initialization
  knn = KNeighborsClassifier(n_neighbors = neighbors)

  knn.fit(X_train, y_train)
  predictions = knn.predict(X_val)

  # STEP 4: Evaluation
  errors.append(mean_absolute_error(y_val, predictions))

plt.plot(range(1,30),errors)
plt.show

#random forest minimize false positives and negative, equalize across race
errors = []

X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=.2)

classifier = RandomForestClassifier(max_depth=11, random_state=0)
classifier.fit(X_train, y_train)
y_pred = classifier.predict(X_test)

score = accuracy_score(y_test, y_pred)
print('Random Forest Model Accuracy: {:.2%}'.format(score))

true_b = np.array(y_test)[np.where(np.array(X_test["RACE_REC"])==0)[0]]
true_w = np.array(y_test)[np.where(np.array(X_test["RACE_REC"])==1)[0]]

pred_b = y_pred[np.where(np.array(X_test["RACE_REC"]==0))[0]]
pred_w = y_pred[np.where(np.array(X_test["RACE_REC"]==1))[0]]

score = accuracy_score(true_b, pred_b)
print('Black Model Accuracy: {:.2%}'.format(score))

score = accuracy_score(true_w, pred_w)
print('White Model Accuracy: {:.2%}'.format(score))

#Combined stats
cm = confusion_matrix(y_test, y_pred)
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=["not convicted", "convicted"])
disp.plot(cmap='Purples');
#Black
cm1 = confusion_matrix(true_b, pred_b)
disp1 = ConfusionMatrixDisplay(confusion_matrix=cm1, display_labels=["not convicted", "convicted"])
disp1.plot(cmap='Blues');
#White
cm2 = confusion_matrix(true_w, pred_w)
disp2 = ConfusionMatrixDisplay(confusion_matrix=cm2, display_labels=["not convicted", "convicted"])
disp2.plot(cmap='Reds');

#fp/(tp+tn+fp+fn) #% false positives
fpB = cm1[0][1]/len(true_b)
#fn/(tp+tn+fp+fn) #% false negatives
fnB = cm1[1][0]/len(true_b)

#fp/(tp+tn+fp+fn) #% false positives
fpW = cm2[0][1]/len(true_w)
#fn/(tp+tn+fp+fn) #% false negatives
fnW = cm2[1][0]/len(true_w)

print("Black FP %: " + str(fpB * 100) + "%")
print("Black FN %: " + str(fnB * 100) + "%")
print("White FP %: " + str(fpW * 100) + "%")
print("White FN %: " + str(fnW * 100) + "%")