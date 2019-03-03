from langdetect import detect


def classifiy(request):
   if request.method == "POST":
    json_data = json.loads(request.body)
    try:
        data = json_data['Tweet']
    except KeyError:
        HttpResponseServerError("Malformed data!")
    lang = detect(data[0]['text'])
    df = data[0]['text'] + ',' + data[0]['class']
    with open('data-'+lang+'.csv', 'a') as f:
        df.to_csv(f, header=False)

   return HttpResponse(json.dumps({'ture'}))