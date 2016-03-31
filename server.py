import os
import subprocess
from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"


@app.route("/RandomForest")
def randomForest():
	response = "I ran the random forest classifer and got"
	retVal = subprocess.check_output(["python", "06.py"])
	response = response +  " and accuracy of " + str(retVal) + "%"
	return response

if __name__ == "__main__":
	port = int(os.environ.get("PORT", 5000))
	app.run(debug=True, host='0.0.0.0', port=port)