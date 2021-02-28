import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.neighbors import NearestNeighbors
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from data_prepare import *

data_user_reviews_new = data_user_reviews
data_apps_new = data_apps

#chenges on data

data_apps_new['Size']=change_coll_only_num(data_apps_new['Size'])


data_apps_download_new = clean_install_coll(data_apps_new['Installs'])
data_apps_new["Installs"] = data_apps_download_new


data_apps_new['App'] = change_app_coll_nan(data_apps_new['App'])


data_apps_new['Rating'] = change_rating_coll_nan(data_apps_new['Rating'])


data_apps_new['Price']  = data_apps_new["Price"].str.replace('$','').astype(float)


data_user_reviews_new['Sentiment_Subjectivity'] = clean_nan_from_sentiment_subj(data_user_reviews_new['Sentiment_Subjectivity'])


data_user_reviews_new['Sentiment_Polarity'] = clean_nan_from_sentiment_pol(data_user_reviews_new['Sentiment_Polarity'])


data_user_reviews_new['Sentiment'] = insert_most_frequent_to_nan_sentiment(data_user_reviews_new['Sentiment'])

#changes for knn

ptc = pd.Series(data_user_reviews_new['Sentiment'])
ptc[ptc == 'Positive'] = 1
data_user_reviews_new['Sentiment'] = ptc

ptc = pd.Series(data_user_reviews_new['Sentiment'])
ptc[ptc == 'Negative'] = -1
data_user_reviews_new['Sentiment'] = ptc

ptc = pd.Series(data_user_reviews_new['Sentiment'])
ptc[ptc == 'Neutral'] = 0
data_user_reviews_new['Sentiment'] = ptc


data_apps_ml = data_apps_new[['App','Category','Rating','Size','Type','Price','Genres']].drop_duplicates()
data_user_reviews_new_ml = data_user_reviews_new[['App','Sentiment', 'Sentiment_Polarity','Sentiment_Subjectivity']]
data = pd.merge(data_apps_ml,data_user_reviews_new_ml,on='App')

apps_num_dict = {}
apps_name_no_dupli = set(data['App'])
num = 1
for i in apps_name_no_dupli:
    if i not in apps_num_dict.keys():
        apps_num_dict[i] = int(num)
        num += 1
def find_app_value(x,dict):
    return dict[x]

data['App'] = data["App"].apply(lambda x: find_app_value(str(x),apps_num_dict))
X = data[['App','Category','Rating','Size','Type','Price','Genres','Sentiment_Polarity','Sentiment_Subjectivity']].copy()
Y = data['Sentiment'].copy().astype(int)

x_ohv = pd.get_dummies(X)

X_train, X_test, y_train, y_test = train_test_split(x_ohv, Y, test_size=0.2)
Sc_X = StandardScaler()
X_train = Sc_X.fit_transform(X_train)
X_test = Sc_X.fit_transform(X_test)

k_range = range(1, 21)
accuracy = []
best_accuracy = 0
best_k = 0
for k in k_range:
    classifier = KNeighborsClassifier(n_neighbors= k , p = 3, metric='euclidean')
    classifier.fit(X_train,y_train)
    y_predict = classifier.predict(X_test)
    acureccy_k = accuracy_score(y_test, y_predict)
    accuracy.append(acureccy_k)
    if acureccy_k > best_accuracy:
        best_accuracy = acureccy_k
        best_k = k

print(("Best K: {0}, Best Accuracy: {1}".format(best_k, best_accuracy)))

plt.plot(k_range, accuracy)
plt.xlabel('Value of K for KNN')
plt.ylabel('Testing Accuracy')
plt.show()





