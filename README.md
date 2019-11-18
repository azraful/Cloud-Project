# Random Country Info

## About

A python-flask based web app leveraging REST [API](https://restcountries.eu/rest/v2) design on google cloud platform (GCP), and using the Kubernetes engine for load scaling. The app implements user-based policies and hence requires users to sign up before it. It randomly chooses a country and queries the Apache Cassandra database, which is set up in GCP using the 3 letter unique country code to collect the position coordinates (latitude, longitude) of the country and displays it dynamically. It also compliments the functionality by using an external API to show the images of flags of the country, along with other information. 

Due to the recent increased prevelance of powerful hardware, such as modern GPUs, hashes have become increasingly easy to crack. A proactive solution to this is to use a hash that was designed to be "de-optimized". 

The user access system uses [flask-hashing](https://flask-hashing.readthedocs.io/en/latest/) for hashing of user passwords in a local database using SHA256 algorithm. It can also be extended to md5, sha1, sha224, sha256, sha384, and sha512. By default, HASHING_METHOD defaults to sha256 and HASHING_ROUNDS defaults to 1.

If you are using anything less than Python 2.7.9 you will only have the guaranteed functions provided by hashlib. Python 2.7.9 or higher allows access to OpenSSL hash functions. The name you supply to HASHING_METHOD must be valid to hashlib. To get a list of valid names, supply a random string to HASHING_METHOD and check the output when initializing your application (it raises and exception), or check hashlib.algorithms for Python 2.7.8 or less, or hashlib.algorithms_available if using Python 2.7.9+.


## Requirements

* python
* pip
* Flask
* Flask==0.11.1
* Flask-Login==0.3.2
* Flask-SQLAlchemy==2.1
* Flask-WTF==0.12
* WTForms==2.1
* Flask-hashing
* cassandra-driver

## How To Install and Run


* Install the Dependencies using `pip install -r requirements.txt`.

* Run the project using `python app.py`.

* App can be viewed at `http://0.0.0.0:8080/`

## Setting up the hash before you run the application

1. Create a file called config.py in the same directory as your app.py.
2. Create a variable with a strong secret hashing password for example
```python
password = `5dfsfadfha283256sdfgz`
```

## [HATEOAS](https://en.wikipedia.org/wiki/HATEOAS) (Hypermedia as the Engine of Application State) 

It is a constraint of the REST application architecture that keeps the RESTful style architecture unique from most other network application architectures. The term “hypermedia” refers to any content that contains links to other forms of media such as images, movies, and text.

This architectural style lets you use hypermedia links in the response contents so that the client can dynamically navigate to the appropriate resource by traversing the hypermedia links. This is conceptually the same as a web user navigating through web pages by clicking the appropriate hyperlinks in order to achieve a final goal.

When you try to make a get request like 
Based on the id, It queries the database and creates a dynamic JSON.

http://35.246.11.169/country/ARG

It will return JSON in the form

{
    'LATITUDE': -35.401338, 'LONGITUDE': -65.187877
}


## Docker image is available and you can run using the following command on gcloud:

```docker
kubectl run country --image=gcr.io/pivotal-trail-229309/countries --port 8080
```

