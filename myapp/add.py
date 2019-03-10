from langdetect import detect
from django.views.decorators.csrf import csrf_exempt
import simplejson as json
import pandas as pd
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseServerError
import os

@csrf_exempt
def add(request):
   if request.method == "POST":
    json_data = json.loads(request.body)
    try:
        data = json_data['Tweet']
    except KeyError:
        HttpResponseServerError("Malformed data!")
    lang = detect(data['text'])
    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    my_file = os.path.join(THIS_FOLDER, '.gitignore/data-'+lang+'.csv')
    if(not (os.path.isfile(my_file))):
        header = "id,Text,Label\n"
        with open(my_file, 'a',encoding="utf-8") as f:
            f.write(header)
    df = data['id']+','+u'"'+data['text']+ '"'+ ',' + data['class'] + '\n'
    with open(my_file, 'a',encoding="utf-8") as f:
        f.write(df)

   return HttpResponse({'true'})