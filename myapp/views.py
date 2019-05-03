from django.shortcuts import render
from django.http import HttpResponse, HttpResponseServerError
from django.views.decorators.csrf import csrf_exempt
import simplejson as json
import pickle
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
import os
from sklearn.model_selection import train_test_split
import langid
import re
import nltk

def hello(request):
   text = "<h1>welcome to my app number %s!</h1>"
   return HttpResponse(text)
@csrf_exempt
def classifiy(request):
   if request.method == "POST":
      json_data = json.loads(request.body)
      try:
         data = json_data['Tweet']
      except KeyError:
          HttpResponseServerError("Malformed data!")
      THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
      my_file = os.path.join(THIS_FOLDER, 'stemm.csv')
      df = pd.read_csv(my_file)
      col = ['Label', 'Text']
      df = df[col]
      def cleanText(text):
        text = re.sub(r'\|\|\|', r' ', text)
        text = re.sub(r'http\S+', r'<URL>', text)
        text = text.lower()
        text = text.replace('x', '')
        return text
      def stemming(text):
         tokenizer = nltk.tokenize.TreebankWordTokenizer()
         tokens = tokenizer.tokenize(text)
         stemmer = nltk.stem.WordNetLemmatizer()
         stemmed = " ".join(stemmer.lemmatize(token) for token in tokens)
         return stemmed
      def generalzing(text):
         genderReplacment = {
            'girl',
            'female',
            'male',
            'men',
            'boy',
            'he',
            'she',
            'guy',
             }
         religionReplacment = {
            'jainism',
            'buddhism',
            'hinduism',
            'sikhism',
            'christianity',
            'catholicism',
            'protestantism',
            'restorationism',
            'gnosticism',
            'shiism',
            'sunnism',
            'judaism',
         }
         followerReplacment = {
            'christian',
            'atheist',
            'hindu',
            'buddhist',
            'taoists',
            'confucianist',
            'jew',
            'sikhs'
         }
         THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
         my_file = os.path.join(THIS_FOLDER, 'nationalities.csv')
         df = pd.read_csv(my_file)
         nationaitiesGenralizing = re.sub('|'.join(r'\b%s\b' % re.escape(s) for s in df.apply(cleanText)),'muslim',text)
         genderGenralizing = re.sub('|'.join(r'\b%s\b' % re.escape(s) for s in genderReplacment),'woman',nationaitiesGenralizing)
         religionGenralizing = re.sub('|'.join(r'\b%s\b' % re.escape(s) for s in religionReplacment),'islam',genderGenralizing)
         followerGenralizing =  re.sub('|'.join(r'\b%s\b' % re.escape(s) for s in followerReplacment),'muslim',religionGenralizing)
         return followerGenralizing
      df['Text'] = df['Text'].apply(cleanText)
      X_train, X_test, y_train, y_test = train_test_split(df['Text'], df['Label'], random_state = 0,test_size=0.2)
      count_vect = CountVectorizer()
      X_train_counts = count_vect.fit_transform(X_train)
      filename = os.path.join(THIS_FOLDER, 'finalized_model.sav')
      loaded_model = pickle.load(open(filename, 'rb'))
      new = []
      for index, tweet in enumerate(data):
          if(tweet['text'] != ''):
              tweetCleaned = cleanText(tweet['text'])
              tweetStemed = stemming(tweetCleaned)
              tweetGeneralized = generalzing(tweetStemed)
              if((langid.classify(tweet['text']) == 'ar') or (langid.classify(tweet['text']) == 'en') or (langid.classify(tweet['text']) == 'tr')):
                 new.append({'class':loaded_model.predict(count_vect.transform([tweetGeneralized]))[0],'id':tweet['id']})
              else:
                  new.append({'class':loaded_model.predict(count_vect.transform([tweetGeneralized]))[0],'id':tweet['id']})

      return HttpResponse(json.dumps(new))
