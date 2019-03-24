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
      df['Text'] = df['Text'].apply(cleanText)
      X_train, X_test, y_train, y_test = train_test_split(df['Text'], df['Label'], random_state = 0,test_size=0.2)
      count_vect = CountVectorizer()
      X_train_counts = count_vect.fit_transform(X_train)
      filename = os.path.join(THIS_FOLDER, 'finalized_model.sav')
      loaded_model = pickle.load(open(filename, 'rb'))
      new = []
      for index, tweet in enumerate(data):
          if(tweet['text'] != ''):
              if((langid.classify(tweet['text'])[0] == 'ar') or (langid.classify(tweet['text'])[0] == 'en') or (langid.classify(tweet['text'])[0] == 'tr')):
                 new.append({'class':loaded_model.predict(count_vect.transform([tweet['text']]))[0],'id':tweet['id']})
              else:
                  new.append({'class':'notSupported','id':tweet['id']})

      return HttpResponse(json.dumps(new))
