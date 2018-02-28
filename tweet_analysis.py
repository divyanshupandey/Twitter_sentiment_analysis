#necessary packages import
import pandas as pd
import numpy as np
import re
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn import svm

#reading the excel file containing the dataset
df = pd.read_excel("corpus/sentiment_data.xlsx",encoding = "ISO-8859-1",names=['label','data'])
df = df[['label','data']]

#data cleansing
def cleansing(x):
    x = x.lower()
    x = re.sub(r"http\S+", "", x)
    x = re.sub(r'[^\w\s]', '', x)
    x = " ".join(filter(lambda x: x[0] != '@' and x[0]!= '#', x.split()))
    x = " ".join(filter(lambda x: x.isalpha() , x.split()))
    x = re.sub(' +', ' ', x)
    return x.strip()
df['data'] = df['data'].apply(lambda x: cleansing(x))

#separate the feature set and label
df_x = df['data']
df_y = df['label']

#using TFIDF vectorizer for word to vector conversion
cv=TfidfVectorizer(min_df=1,stop_words='english')

#splitting the training and testing set
x_train,x_test,y_train,y_test=train_test_split(df_x,df_y,test_size=0.15,random_state=4)

#scaling the feature vectors for optimization
x_traincv = cv.fit_transform(x_train)
x_testcv = cv.transform(x_test)
y_train=y_train.astype('int')
 
#defining the model
svm_clf=svm.SVC(kernel='linear', C = 1.0)   

#loading the data to the model with the label and training
def training():
    global x_traincv,y_train,svm_clf
    svm_clf.fit(x_traincv,y_train)

#accuracy prediction
def testing():
    global svm_clf
    clf1 = open('model/svm.pickle','rb')
    svm_clf = pickle.load(clf1)
    pred=svm_clf.predict(x_testcv)
    actual=np.array(y_test)
    count=0
    for i in range (len(pred)):
      if int(pred[i]) == int(actual.item(i)):
          count=count+1
    print("The number of samples in the test set is",len(pred))
    print("The accuracy on the test set is---> ")      
    print(count*100/len(pred))

#save the model using pickle
def model_saving():
    global svm_clf
    clf = open('model/svm.pickle','wb')
    pickle.dump(svm_clf,clf)
    clf.close()

#prediction for random data
def prediction(text1 = "i did not like the product"):
    global cv
    list1 = []
    list1.append(text1)
    df_x = pd.DataFrame({"data": list1})
    df_x['data'] = df_x['data'].apply(lambda x: cleansing(x))
    df_x = df_x['data']
    x_testcv = cv.transform(df_x)
    clf1 = open('model/svm.pickle','rb')
    svm_clf1 = pickle.load(clf1)
    
    pred=svm_clf1.predict(x_testcv)
    clf1.close()
    return (pred)
#training()
#model_saving()
#testing()
#print(prediction())