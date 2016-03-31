import os
import subprocess
import numpy as np
from flask import render_template
from sklearn import preprocessing
from sklearn.ensemble import RandomForestClassifier

from flask import Flask
from flask import request

app = Flask(__name__)

def classifier():

	age = request.args.get("age")
	gender = request.args.get("gender")
	rest_bp = request.args.get("rest_bp")
	fbs = request.args.get("fbs")

	print age, gender, rest_bp, fbs

	clevelandCSV = np.loadtxt("cleveland-4.csv", delimiter=";")

	trainingFeatures = clevelandCSV[:, 0:4]
	trainingLabels = clevelandCSV[:, 4]

	testingFeatures = []
	testingFeatures.append(float(age))
	testingFeatures.append(float(gender))
	testingFeatures.append(float(rest_bp))
	testingFeatures.append(float(fbs))

	print testingFeatures

	testingFeatures = [testingFeatures]
	testingFeatures_X = []
	testingFeatures_X = np.array(testingFeatures)

	testingFeatures = testingFeatures_X
	# trainingFeatures = preprocessing.scale(trainingFeatures)
	# testingFeatures = preprocessing.scale(testingFeatures)

	model = RandomForestClassifier(n_estimators=200)
	model = model.fit(trainingFeatures, trainingLabels)

	predictedLabels = model.predict(testingFeatures)

	return int(predictedLabels[0])


@app.route("/")
def hello():
    return render_template('home.html')


@app.route("/RandomForest")
def randomForest():
	response = "I ran the random forest classifer and got"
	# retVal = subprocess.check_output(["python", "06.py"])
	retVal = classifier()
	#response = response +  " and accuracy of " + str(retVal) + "%"
	response = response + str(retVal)
	return str(retVal)

if __name__ == "__main__":
	port = int(os.environ.get("PORT", 5000))
	app.run(debug=True, host='0.0.0.0', port=port)








