#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 27 19:14:26 2018

@author: user
"""
# importing necessary libraries
import tweepy
import csv
import time
from tweet_analysis import prediction

#input credentials here
consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth,wait_on_rate_limit=True)

#emptying both the files at the starting
with open('prediction_files/output.txt','w+') as f:
    f.write("")
    
with open('prediction_files/prediction.txt','w+') as f:
    f.write("")
    
# Open/Create a file to append data    
csvFile = open('tweets/ua.csv', 'w+')
csvWriter = csv.writer(csvFile)
classes = ["positive","negative","neutral"]

#taking the inputs
count = int(input("enter the count of tweets to be scrapped --> "))
hashtag = input("Enter the hashtag to be scrapped ---> ")

#initialising necessary variables
pos = 0
neg = 0
neutral = 0
it = 0

if(hashtag[0] != '#'):
   hashtag = "#"+hashtag

#calling the twitter api
for tweet in tweepy.Cursor(api.search,q=hashtag,
                           lang="en",
                           since="2017-02-27").items(count):
    pred = prediction(tweet.text)
    pred_val = 0 # will be 0 for neutral , 1 positive and -1 for negative
    if(pred[0] == 0):
        neg+=1
        pred_val = -1
    elif(pred[0] == 1):
        neutral+=1
        pred_val = 0
    else:
        pos+=1
        pred_val = 1
        
    time.sleep(0.5)
    
    #writing to file for pie chart data 
    with open('prediction_files/output.txt','w+') as f:
        str1 = str(pos)+","+str(neg)+","+str(neutral)
        f.write(str1)
    
    #writing to file for line chart
    with open('prediction_files/prediction.txt','a+') as f:
        str1 = str(it)+","+str(pred_val)+"\n"
        it+=1
        f.write(str1)
        
    # writing the tweets to csv file   
    csvWriter.writerow([pred, tweet.text.encode('utf-8')])


