# Generic libs:
import os
import subprocess

# Flask related libs
from flask import Flask
from flask.ext.cors import CORS
from flask import request
from flask import render_template

# ML Libs
import numpy as np
from sklearn import preprocessing
from sklearn.ensemble import RandomForestClassifier
from sklearn.externals import joblib


app = Flask(__name__)
CORS(app)

def classify(age,gender,restbp,chol,fbs,restecg,maxhr):

	min_age = 29 
	max_age = 77 
	avg_age = 54.4389438944

	# gender not normalized - binary

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
	n_gender = gender # Leave as is!

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
	row.append(n_gender)
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
	return prediction

@app.route("/")
def hello():
    return render_template('home.html')


@app.route('/svm')
def svm():

	age = float(request.args.get("age"))
	gender = int(request.args.get("gender"))
	restbp = float(request.args.get("restbp"))

	chol = float(request.args.get("chol"))
	
	fbs = float(request.args.get("fbs"))
	restecg = float(request.args.get("restecg"))
	maxhr = float(request.args.get("maxhr"))

	prediction = classify(age,gender,restbp,chol,fbs,restecg,maxhr)
	return str(prediction)


if __name__ == "__main__":
	port = int(os.environ.get("PORT", 5000))
	app.run(debug=True, host='0.0.0.0', port=port)








