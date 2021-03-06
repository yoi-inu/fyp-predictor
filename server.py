# Generic libs:
import os
import time
import subprocess
import random
import csv
import math

# Flask related libs
from flask import Flask
from flask import request
from flask import render_template
from flask import send_from_directory
# from flask.ext.cors import CORS, cross_origin

# ML Libs
import numpy as np
from sklearn import preprocessing
# from sklearn.ensemble import RandomForestClassifier
from sklearn.externals import joblib


from datetime import timedelta
from flask import make_response, request, current_app
from functools import update_wrapper

from twilio.rest import TwilioRestClient 

app = Flask(__name__, static_url_path='')
# CORS(app)

def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator

# Static Files for UI
@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)

@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('css', path)

@app.route('/font/<path:path>')
def send_font(path):
    return send_from_directory('font', path)

@app.route('/fonts/<path:path>')
def send_fonts(path):
    return send_from_directory('fonts', path)

def classify(age,sex,restbp,chol,fbs,restecg,maxhr):

	min_age = 29 
	max_age = 77 
	avg_age = 54.4389438944

	# sex not normalized - binary

	min_restbp = 94 
	max_restbp = 200 
	avg_restbp = 131.689768977

	min_chol = 126 
	max_chol = 564 
	avg_chol = 246.693069307

	# fbs - not normalized - binary, but if missing using avg
	avg_fbs = 0.148514851485

	min_restecg = 0 
	max_restecg = 2 
	avg_restecg = 0.990099009901

	min_maxhr = 72 
	max_maxhr = 202 
	avg_maxhr = 149.607260726

	# Assuming exang to be missing from input
	avg_exang = 0.326732673267


	# First, normalize each of them
	n_age = float(age - min_age) / float(max_age-min_age)
	n_sex = sex # Leave as is!

	if(restbp<0):
		n_restbp = avg_restbp
	else:
		n_restbp = float(restbp - min_restbp) / float(max_restbp-min_restbp)

	if(chol<0):
		n_chol = avg_chol
	else:
		n_chol = float(chol - min_chol) / float(max_chol-min_chol)

	if(fbs<0):
		n_fbs = avg_fbs
	else:
		n_fbs = fbs

	if(restecg<0):
		n_restecg = avg_restecg
	else:
		n_restecg = float(restecg - min_restecg) / float(max_restecg-min_restecg)

	if(maxhr<0):
		n_maxhr = avg_maxhr
	else:
		n_maxhr = float(maxhr - min_maxhr) / float(max_maxhr-min_maxhr)

	n_exang = avg_exang

	# Build the feature row
	row = [];
	row.append(n_age)
	row.append(n_sex)
	row.append(n_restbp)
	row.append(n_chol)
	row.append(n_fbs)
	row.append(n_restecg)
	row.append(n_maxhr)
	row.append(n_exang)

	inp = [row]

	# Make it a NumPy array
	inp_set = np.array(inp)
	# print "NP Array: ", inp_set
	print "Classifying: ", inp
	# Load the pickled predictor
	model = joblib.load('trainedModel/pickled_svm.pkl')
	prediction = model.predict(inp_set)
	print prediction
	return int(prediction[0])

@app.route("/")
def hello():
    return render_template('home.html')
def hold():
	print "Holding for "
	s = random.uniform(3, 5)
	print s , " units (s)"
	time.sleep(int(s))

@app.route('/svm', methods=['GET'])
@crossdomain(origin='*')
def svm():

	age = float(request.args.get("age"))
	sex = int(request.args.get("sex"))
	restbp = float(request.args.get("restbp"))

	chol = float(request.args.get("chol"))
	
	fbs = float(request.args.get("fbs"))
	restecg = float(request.args.get("restecg"))
	maxhr = float(request.args.get("maxhr"))

	prediction = classify(age,sex,restbp,chol,fbs,restecg,maxhr)
	hold()
	if(prediction<1):
		return str(0)
	else:
		return str(1)

@app.route('/alertemg', methods=['GET'])
@crossdomain(origin='*')
def alertemg():

	print "Received an alert!"

	latitude =  float(request.args.get("latitude"))
	longitude =  float(request.args.get("longitude"))

	with open('locations.csv', 'r') as f:
	  reader = csv.reader(f, delimiter=',', quotechar="'")
	  locations = list(reader)		

	min_dist = 1000
	min_i = -1
	i = 0

	for location in locations:
		location[0] = float(location[0])
		location[1] = float(location[1])
		this_dist = math.pow( ( latitude - location[0] ) , 2 ) + math.pow( ( longitude - location[1] ) , 2 )
		print this_dist, location
		this_dist = math.sqrt(this_dist)
		if( this_dist < min_dist ):
			min_dist = this_dist
			min_i = i
		i = i + 1


	SMSBody = "HeartAttack! UserLocation: " + str(latitude)
	SMSBody = SMSBody + "," + str(longitude)

	SMSBody = SMSBody + ", NearestHospital: " + str(locations[min_i][2]) + " " + str(locations[min_i][0]) + "," + str(locations[min_i][1])


	SMSTo = "<SMS-To-Unconfigured>"
	SMSFrom = "<SMS-From-Unconfigured>"
	retVal = "Emergency SMS Sent:\n\"To: " + SMSTo + "\nContents: " + SMSBody + "\""
	print retVal

	# put your own credentials here 
	ACCOUNT_SID = "<ACCOUNT_SID_FROM_TWILIO>" 
	AUTH_TOKEN = "<AUTHENTICATION_TOKEN_FROM_TWILIO>" 

	# <start> Uncomment this section to enable actual SMS Sending Once Connected to Twilio Account
	# client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN) 
	 
	# client.messages.create(
	# 	to=SMSTo, 
	# 	from_=SMSFrom, 
	# 	body=SMSBody,  
	# )
	# <end> Comment this section to disble the texts during debugging 

	return retVal


if __name__ == "__main__":
	port = int(os.environ.get("PORT", 5000))
	app.run(debug=True, host='0.0.0.0', port=port)








