# Tweet-classifier
multiclass classifier using machine learning API
Classify text into there categories neutral, sexism, racism
##Usage
by pulling the app to a server

then for:

1-classifying 
POST request with the url serverUrl/myapp/classifiy
in the request body, there should be an array of objects 'tweet'
each object has to have two attributes id and text
the response will be similar to the request but instead of text there will be the class

2-add classified text to the data set
POST request with the url serverUrl/myapp/add
in the request body, there should be an object 'tweet'
and object has to have three attributes  id, class, and text

## Built With

* [Django](https://www.djangoproject.com/) - Django is a Python-based free and open-source web framework.

## Authors

* **Muhammed Akkad** - [linkedIn](https://www.linkedin.com/in/mohamad-akkad-5a923a149/)
* **Dzeneta Hajdarpasic** - [linkedIn](https://www.linkedin.com/in/dzeneta-hajdarpasic-a2290a18a)

## References
Data set was collected by 
[Waseem, Zeerak  and  Hovy, Dirk](https://github.com/ZeerakW/hatespeech)
