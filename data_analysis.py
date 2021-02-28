import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import re
import datetime
from scipy import stats
from data_prepare import *


save_original_gen = data_apps['Genres']

## Q1 ##

print('num of rows:' , data_apps.shape[0])
print('colum names:', list(data_apps.head(0)))
print('num of rows:', data_user_reviews.shape[0])
print('colum names:',list(data_user_reviews.head(0)))

print('__________________________________________________')


## Q2 ##

#1#

print('Total count of apps categories: {0}'.format(len(set(list(data_apps['Category'])))))

print('__________________________________________________')

#2#

data_apps['Size']=change_coll_only_num(data_apps['Size'])
x = max(data_apps['Size'])
z= data_apps[data_apps['Size']==x]['App']
print("Biggest App size are:  ",'\n',z)

print('__________________________________________________')

#3#

data_apps_download_new = clean_install_coll(data_apps['Installs'])
data_apps["Installs"] = data_apps_download_new
print('the Apps with most downloads are:' ,data_apps[data_apps["Installs"]== data_apps_download_new.max()])

print("__________________________________________________")

#4#

data_apps["Last Updated"] = data_apps["Last Updated"].apply(lambda x: change_time(str(x)))
most_recent_update = data_apps["Last Updated"].max()
coll_of_most_updat_app = data_apps[data_apps["Last Updated"]==most_recent_update]['App']
print('the most updated app is:' ,'\n',coll_of_most_updat_app)

print('_______________________________________________')

#5#

def split_genres(geners_coll):
    temp = geners_coll.str.split(pat=";", expand=True)
    data_apps['Genres'] = temp[0]
    geners_bar = data_apps[['Genres', 'Rating']]
    data_apps['Genres'] = temp[1]
    gener_bar_1 = data_apps[['Genres', 'Rating']]
    frames = [gener_bar_1, geners_bar]
    result = pd.concat(frames, ignore_index=True)
    return result

result = split_genres(data_apps['Genres'])
print('The most populer app genres is:' , result['Genres'].value_counts().head(1))
data_apps['Genres'] = save_original_gen


## Q3 ##

#1#

print(result['Genres'].value_counts())

print ('__________________________________________________')

#2#

app_free_charge = data_apps[data_apps['Type']=='Free']
print("The free Apps are:",'\n',list(app_free_charge['App']))

print('__________________________________________________')

#3#

app_paid_charge = data_apps[data_apps['Type'] == 'Paid']
print("The sum of free apps install is :",np.sum(app_free_charge['Installs']))
print("The sum of paid install is :",np.sum(app_paid_charge['Installs']))
if np.sum(app_free_charge['Installs'])>np.sum(app_paid_charge['Installs']) :
    print('Free apps are more popular')
elif np.sum(app_free_charge['Installs'])==np.sum(app_paid_charge['Installs']):
    print('Free apps and Paid apps have thr same popularity')
else:
    print('Paid apps are more popular')

print('__________________________________________________')
#4#

def get_app_details_by_letter(letter):
      x = data_apps[data_apps['App'].str.startswith(letter)]
      return x

data_apps['App'] = change_app_coll_nan(data_apps['App'])
print(get_app_details_by_letter('F'))

print ('__________________________________________________')

## Q4 ##

#1#

positive_clasifiied = data_user_reviews[data_user_reviews['Sentiment'] == 'Positive']
print("num of apps that were clasified positive:",positive_clasifiied['App'].drop_duplicates().shape[0])

print ('__________________________________________________')

#2#

negative_clasifiied = data_user_reviews[data_user_reviews['Sentiment'] == 'Negative']
print("num of apps that were clasified negative:",negative_clasifiied['App'].drop_duplicates().shape[0])
print('__________________________________________________')
neutral_clasifiied = data_user_reviews[data_user_reviews['Sentiment'] == 'Neutral']
print("num of apps that were clasified neutral:",neutral_clasifiied['App'].drop_duplicates().shape[0])

print ('__________________________________________________')

#3#


data_apps['Rating'] = change_rating_coll_nan(data_apps['Rating'])
rate_new = (data_apps['Rating'])
rate_float = rate_new.astype(float).max()
only_max_rate_app = data_apps[data_apps['Rating']==rate_float]['App']
join = pd.merge(only_max_rate_app, data_user_reviews, on='App')
print(join['Sentiment'])

print ('__________________________________________________')

#4#

app_free_charge = (data_apps[data_apps['Type'] == 'Free']['App']).drop_duplicates()
join = pd.merge(app_free_charge, data_user_reviews, on='App')
print(' the average polarity of free apps is: ' ,join['Sentiment_Polarity'].mean())

print ('__________________________________________________')

 #5#
def get_average_polarity(app_name):
    if app_name in list(data_user_reviews['App']):
        return data_user_reviews[data_user_reviews['App']==app_name]['Sentiment_Polarity'].mean()
    else:
        return "App not in database"
print(get_average_polarity('10 Best Foods for You'))

print ('__________________________________________________')

#6#

def get_sentiment(app_name):
    average_pol=get_average_polarity(app_name)
    if str(average_pol)==average_pol:
        return average_pol
    else:
        if average_pol>0:
            return 'Average polarity is Positive'
        if average_pol<0:
            return 'Average polarity is Negitive'
        else:
            return 'Average polarity is Neutral'


print(get_sentiment('Facebook'))

print ('__________________________________________________')


## Q5 ##

#1#

data_user_reviews['Sentiment'].value_counts().plot(kind = 'bar')
plt.show()
#
print ('__________________________________________________')
#2#

result.groupby('Genres').mean().plot(kind = 'bar')
plt.show()
data_apps['Genres'] = save_original_gen

print ('__________________________________________________')
#3#

app_free_charge = (data_apps[data_apps['Type'] == 'Free']['App']).drop_duplicates()
join_free = pd.merge(app_free_charge, data_user_reviews, on='App')
join_free[join_free['Sentiment_Polarity'].isnull()] = join_free['Sentiment_Polarity'].mean()
x_1 = join_free['Sentiment_Polarity']

app_paid_charge = (data_apps[data_apps['Type'] == 'Paid']['App']).drop_duplicates()
join_paid = pd.merge(app_paid_charge, data_user_reviews, on='App')
join_paid[join_paid['Sentiment_Polarity'].isnull()] = join_paid['Sentiment_Polarity'].mean()
x_2 = join_paid['Sentiment_Polarity']

y0 = np.array(x_1)
y1 = np.array(x_2)
all_data = [y0 , y1]
labels = ['free', 'paid']

fig, (ax1) = plt.subplots(nrows=1, ncols=1)

bplot1 = ax1.boxplot([y0,y1],
                     vert=True,  # vertical box alignment
                     patch_artist=True,  # fill with color
                     labels=labels)  # will be used to label x-ticks
ax1.set_title('sentiment polarity boxplot between free/paid apps')
colors = ['pink', 'lightblue']
for patch, color in zip(bplot1['boxes'], colors):
        patch.set_facecolor(color)

ax1.yaxis.grid(True)
ax1.set_xlabel('free/paid')
ax1.set_ylabel('polarity')
plt.ylim(-1,1)

plt.show()

print ('__________________________________________________')

#4#

new_df = pd.DataFrame(data_apps[['Category', 'Rating']])
print(new_df.groupby('Category').mean())
print(new_df.groupby('Category').std())
print(new_df.groupby('Category').median())
print(new_df.groupby('Category').agg(lambda x:x.value_counts().index[0]))

#The most stable category for our opinion is entertament

print ('__________________________________________________')

#5#

def cheak_normal_disrbution(x):
    k2, p = stats.normaltest(x, nan_policy = 'omit')

    if p < 0.05 and p>=0:
       print("The category does not distributos normal for sure " '\n')
    else:
         print("The category does distributos normal " '\n')

rate_list_norm = new_df.groupby('Category')['Rating']
for i in rate_list_norm:
    print('the catagory:' ,i[0])
    list_of_cat = list(i[1])
    if len(list_of_cat)>7:
        cheak_normal_disrbution(list_of_cat)
    else: print('not enough data to determent if normal distirbute''\n')



