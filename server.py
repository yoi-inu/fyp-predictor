import os
import subprocess
import numpy as np
from sklearn import preprocessing
from sklearn.ensemble import RandomForestClassifier

from flask import Flask

app = Flask(__name__)

def classifier():
	dataset = np.loadtxt("normalized.csv", delimiter=",")

	train_X = dataset[1:10000,0:10]
	train_Y = dataset[1:10000,10]

	#print train_Y

	#train_normalized_X = preprocessing.normalize(train_X)

	#train_standardized_X = preprocessing.scale(train_X)

	model = RandomForestClassifier(n_estimators=200)
	model.fit(train_X,train_Y)

	test_X = dataset[10000:15121,0:10]
	test_Y = dataset[10000:15121,10]

	predictions = model.predict(test_X)

	i = 0
	num_correct = 0
	for prediction in predictions:
		if(prediction== test_Y[i]):
			num_correct += 1
		i += 1

	accuracy = float(num_correct)/float(i)
	return (accuracy*100)


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/RandomForest")
def randomForest():
	response = "I ran the random forest classifer and got"
	# retVal = subprocess.check_output(["python", "06.py"])
	retVal = classifer()
	response = response +  " and accuracy of " + str(retVal) + "%"
	return response

if __name__ == "__main__":
	port = int(os.environ.get("PORT", 5000))
	app.run(debug=True, host='0.0.0.0', port=port)