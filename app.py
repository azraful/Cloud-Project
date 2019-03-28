#!/usr/bin/python
# -*- coding: utf-8 -*-

#Import library dependencies

from flask import Flask, flash, redirect, render_template, request, session, abort  #General html rendering, navigation
import os, sys
import random
import json
import requests     #To obtain api get or post requests
from flask_hashing import Hashing
from flask import Flask, request, jsonify  #To create json from data
from flask_restful import Resource, Api     #Hashing tool
from cassandra.cluster import Cluster 
import config

#Connecting to Cassandra Cluster
cluster = Cluster(['cassandra'])
sesion = cluster.connect()

#Custom error messages
errors = {
    'Country DOES NOT EXIST': {
        'message': "Sorry. Country DOES NOT EXIST. Try different number",
        'status': 404,
        'For more info': "Visit support docs"
    },
    'ResourceDoesNotExist': {
        'message': "A resource with that ID no longer exists.",
        'status': 410,
        'extra': "Any extra information you want.",
    },
}

app = Flask(__name__)
api = Api(app, errors=errors)

salt = config.password    #Set salt/key
password = 'password'
hashing = Hashing(app)
h = hashing.hash_value('password', salt)   #Generate hash

#Home page

@app.route('/')
def home():
#List of Countries
    coun = ['Morocco', 'Paraguay', 'Palau', 'Zimbabwe', 'El Salvador', 'Portugal', 'France', 'Japan', 'Mauritania', 
			'Sweden', 'Trinidad and Tobago', 'Uzbekistan', 'United Kingdom of Great Britain and Northern Ireland', 
			'Sri Lanka', 'Mauritius', 'Libya', 'Belarus', 'Saint Vincent and the Grenadines', 'Yemen', 'Uganda', 
			'Faroe Islands', 'Bhutan', 'Panama', 'Honduras', 'Bosnia and Herzegovina', 'Greenland', 'Azerbaijan', 
			'South Georgia and the South Sandwich Islands', 'British Indian Ocean Territory', 'Christmas Island', 
			'Sao Tome and Principe', 'Mongolia', 'Latvia', 'Turks and Caicos Islands', 'Saint Kitts and Nevis', 
			'Bolivia', 'Netherlands', 'New Zealand', 'Colombia', 'Tunisia', 'Jordan', 'Korea (Republic of)', 
			'Saint Pierre and Miquelon', 'Russian Federation', 'Kazakhstan', 'Niger', 'Georgia', 'Nicaragua', 
			'Isle of Man', 'Bermuda', 'Cook Islands', 'Costa Rica', 'Algeria', 'Argentina', 'Bahrain', 'Zambia', 
			'Mozambique', 'Ethiopia', 'Haiti', 'Somalia', 'Guatemala', 'Iran (Islamic Republic of)', 'Romania', 
			'Guinea-Bissau', 'Antarctica', 'Lebanon', 'Saint Martin (French part)', 'Tanzania, United Republic of', 
			'Macao', 'Cameroon', 'Singapore', 'Slovenia', 'Central African Republic', 'Timor-Leste', 'Lithuania', 
			'Nauru', 'South Sudan', 'Wallis and Futuna', 'Brunei Darussalam', 'Viet Nam', 'Grenada', 'China', 'Congo', 
			'Burundi', 'Chad', 'Egypt', 'Congo (Democratic Republic of the)', 'Benin', 'Jersey', 'Senegal', 'Nigeria', 
			'Tonga', 'Cyprus', 'Togo', 'Macedonia (the former Yugoslav Republic of)', 'Pakistan', 'Mexico', 'Angola', 
			'Sierra Leone', 'Micronesia (Federated States of)', 'Canada', 'Gambia', 'Ukraine', 'Finland', 'Aruba', 
			'Madagascar', 'Pitcairn', 'Malta', 'Afghanistan', 'Liberia', 'Equatorial Guinea', 'Austria', 'Western Sahara']

#Random Select Country from List    
    random_coun = (random.choice(coun))
#External API	
    coun_url = 'https://restcountries.eu/rest/v2/name/{name}'
#Filtering API response	
    coun_url = coun_url.format(name=random_coun)
    resp = requests.get(coun_url)
    content = resp.json()
#Assign variables to Country Info	
    cname = (content[0]['name'])        #Country Name
    cflag = (content[0]['flag'])        #Link to Country Flag
    creg = (content[0]['subregion'])    #Subregion of Country
    ccap = (content[0]['capital'])      #Capital of Country
    ccode = (content[0]['callingCodes'])#Calling Code of Country
    ctime = (content[0]['timezones'])   #Timezones of Country
    cpop = (content[0]['population'])   #Population of Country
    alpha = (content[0]['alpha3Code'])  #Unique 3 Letter Country Code
    alpha = str(alpha)             
#CQL Query
    rows = sesion.execute("""select * from nav.stats where iso3 = '{}' ALLOW FILTERING""".format(alpha))
#Storing database response
    for country in rows:
        lat = country.lat
        long1 = country.long
        description = country.description
#Checking authentication
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('home.html', cname=cname, cflag=cflag, creg=creg, ccap=ccap, ctime=ctime, cpop=cpop, ccode=ccode, alpha=alpha, lat=lat, long=long1)

#Login Page
@app.route('/login', methods=['POST'])
def do_admin_login():
    
    if hashing.check_value(h, request.form['password'], salt) == True and request.form['username'] == 'admin':
        print('Correct Password')
        session['logged_in'] = True
    else:
        flash('wrong password!')
    return home()

#Logout Action
@app.route("/logout")
def logout():
    session['logged_in'] = False
    return home()

#Generate JSON for Internal API
class multi(Resource):
    def get(self, alpha):       
        rows = sesion.execute("""select * from nav.stats where iso3 = '{}' ALLOW FILTERING""".format(alpha))
        for country in rows:
                lat = country.lat
                long1 = country.long
        if country.lat is None:
            return errors['Country DOES NOT EXIST']
        else:
            return jsonify({'LATITUDE': lat, 'LONGITUDE': long1})
#Resource Identifier for Internal API
api.add_resource(multi, '/country/<alpha>')

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(host='0.0.0.0', port=8080)

