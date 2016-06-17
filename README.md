# Server Application for Cardia

Completed as part of course-work (final year project) for Semester 8 - Computer Science & Engineering @ [PESIT South Campus](http://pesitsouth.pes.edu/) (Affiliated to [VTU](http://vtu.ac.in/)).

A Python & Flask based server that receives request from the client (Cardia Mobile Application) to:

  1. Classify a set of inputs (user charactersitics) according to *Angiographic Disease Status*.
  2. Receives a request to send SMS messages to Emergency Contacts via the [Twilio Messaging API](https://www.twilio.com/sms).
  
You can see a demo [here](https://fyp-predictor.herokuapp.com). Note: Since it's a free-tier dyno, the app will probably be asleep & the first request will take some time to be served. Be patient =P

# Requirements

* Python 2.7
* Miniconda/Conda 3.19.0
  * nomkl, scipy, numpy, scikit-learn - [conda-requirements.txt](./conda-requirements.txt)
  * twilio, requests, httpbin, gunicorn - [requirements.txt](./requirements.txt)
  * Heroku (Toolbelt) for deployment. _Optional_.
  
# Routes & API

### 1. GET '/' - Home

The index route contains a basic web interface that elicits user input through a form and runs the classifier by performing a GET Request on '/svm'
Also displays certain sample inputs with known outputs. 

See '/svm' for more info.

### 2. GET '/svm' - Support Vector Classifier

**Parameters**:

|Key|Description|Value Type|Range|
|---|---|---|---|
|`age`|Age|Integer|`29` to `77` years|
|`sex`|Gender/Sex|Binary|`0` for Female and `1` for Male|
|`restbp`|Resting Blood Pressure|Integer|`90` to `200` in mm of Hg|
|`chol`|Blood Cholestrol Level|Integer|`125` to `560` mg/dl|
|`fbs`|Fasting Blood Sugar Level|Binary|`0` if `<120 mg/dl`; `1` if `>120 mg/dl`|
|`restecg`|Resting ECG State Characteristics|Ternary|`0`: Normal ECG<br />`1`: Having ST-T Wave Abnormality [[1][tw]], [[2][sw]], [[3][ste]] <br />`2`: Having Left Ventricular Hypertrophy according to Estes' Criteria [[4]][ec]|
|`maxhr`|Maximum Heart Rate Achieved|Integer|`70` to `200` bpm|

[tw]: https://en.wikipedia.org/wiki/T_wave
[sw]: https://en.wikipedia.org/wiki/ST_depression
[ste]: https://en.wikipedia.org/wiki/ST_elevation
[ec]: https://en.wikipedia.org/wiki/Left_ventricular_hypertrophy#ECG_criteria_for_LVH

**Functionality**:
Loads a [pickled](scikit-learn.org/stable/modules/model_persistence.html) [SVM Model](scikit-learn.org/stable/modules/svm.html
), parses and scales (normalizes) the input and runs the classifier and returns the prediction.

**Returns/Response**: 

| Value | Interpretation |
|---:|:---|
|0|Negative Angiographic Disease Status (No arterial blockage)|
|1|Positive Angiographic Disease Status (Arterial blockage)|

### 3. GET '/alertemg' - Emergency Alert SMS Sender

**Parameters**:
* latitude (latitude float value of User's (who's experiencing a heart attack) location
* longitude (longitude float value of User's (who's experiencing a heart attack) location

**Functionality**:
Uses the Twilio API to send an SMS to notify the _emergency_ contact of the individual under duress (experiencing heart attack).

**Returns/Response**:  

`String`

```
Emergency SMS Sent:  
To: <Number>  
Contents: Heart Attack! UserLocation: <latitude>,<longitude>,  
NearestHospital: <Hospital_Name>, <latitude_hospital>,<longitude_hospital>
```

# Configuration

### 1. Set-up Twilio

1. Create an account on [Twilio](https://www.twilio.com/try-twilio) and login.
2. Open [this](https://www.twilio.com/user/account/phone-numbers/verified) and add the phone number for demonstration, twilio will send you an SMS for verification. This is for the free version only. Save this number for use below.
3. Go [here](https://www.twilio.com/user/account/settings) and:  
	a. Copy AccountSID field for use below  
	b. Copy AuthToken field for use below  
4. Go [here](https://www.twilio.com/user/account/messaging/dev-tools/api-explorer/message-create)  
	a. Copy contents of ‘From Number’ for use below [6]

