import numpy as np
from sklearn import preprocessing
from sklearn.ensemble import RandomForestClassifier

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
print(accuracy*100)












