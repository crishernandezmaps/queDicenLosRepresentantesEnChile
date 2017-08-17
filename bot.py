#!/usr/bin/python3
import tweepy
import time
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from collections import Counter
import re
import pandas as pd
from wordcloud import WordCloud
from PIL import Image
import numpy as np
import random
from os import path
import matplotlib.pyplot as plt

#Twitter credentials
auth = tweepy.OAuthHandler('API Key', 'API Secret')
auth.set_access_token('Access Token', 'Access Token Secret')
api = tweepy.API(auth, wait_on_rate_limit=True)

# printing with less effort
p = print

# dics to remove unnecesary words
stopES = set(stopwords.words('spanish'))
stopCustom = ['co','n°','http','...','//t.co/','¿','?','!','/',"''",'tan','https','jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec','.',',','1','2','3','4','5','6','7','8','9','0','1h','2h','3h','4h','5h','6h','7h','8h','9h','0h','replies','retweets','likes','reply','retweet','retweeted','like','liked','copy','link','tweet','embed','verified','account','@','#',':','…','``']

# cuantos tweets?
num_tweets = 100

# optiones para la visualización
d = path.dirname(__file__)
mask = np.array(Image.open(path.join(d, "bandera.png")))
def grey_color_func(word, font_size, position, orientation, random_state=None,**kwargs):
    return "hsl(0, 0%%, %d%%)" % random.randint(60, 100)

# getting last three original tweets to create a word frequency
def getLastTweets():
    list_of_words = []
    df = pd.read_csv('users.csv',sep=',')

    for i, row in df.iterrows():
        try:
            search = api.user_timeline(screen_name = row['users'],count = num_tweets,include_rts = False)
            for t in search:
                text = t.text
                words = word_tokenize(text)
                for word in words:
                    y = re.sub('[0-9]+', '', word)
                    x = y.lower()
                    if(x not in stopES) and (x not in stopCustom):
                        if(len(x) > 0):
                            p(i)
                            list_of_words.append(x)
        except Exception:
            pass

    text = " ".join(list_of_words)

    wc = WordCloud(max_words=100, mask=mask, stopwords=stopCustom, margin=10,random_state=1).generate(text)
    # store default colored image
    default_colors = wc.to_array()
    plt.title("¿Qué dicen los representantes?")
    plt.imshow(wc.recolor(color_func=grey_color_func, random_state=3),interpolation="bilinear")
    wc.to_file("representantes_palabras.png")
    plt.axis("off")
    plt.figure()
    plt.title("¿Qué dicen los representantes?")
    plt.imshow(default_colors, interpolation="bilinear")
    plt.axis("off")
    plt.show()


getLastTweets()
