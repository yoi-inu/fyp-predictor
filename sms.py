from twilio.rest import TwilioRestClient 
 
# put your own credentials here 
ACCOUNT_SID = "AC7f0d7576b171275eeb549176f0a889a3" 
AUTH_TOKEN = "a8cbf4b14e6453a0594256b7d3702d81" 
 
client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN) 
 
client.messages.create(
	to="+919916101013", 
	from_="+12023354404", 
	body="Testing123",  
)