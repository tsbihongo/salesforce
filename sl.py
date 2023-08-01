pip install twilio
import requests 
from twilio.rest import Client
import json
import sys
account_sid = 'AC2802e17c9821414649ae4f0500824697'
auth_token = 'b4c696463193bb5f9b355915f1baf1b8'
client = Client(account_sid, auth_token)

message = client.messages.create(
  from_='whatsapp:+14155238886',
  body="message received", 
  to='whatsapp:+85292097959'
)



#process using API
endpoint = 'https://pwcai.openai.azure.com/openai/deployments/GPT35/chat/completions?api-version=2023-03-15-preview'
api_key = 'f379af432a914d87a79c86c41ce3b765'
  
request_body = {
    'messages': [
        {
            'role': 'user',
            'content':message_body #change here
        }
    ]
}
 
headers = {
    'Content-Type': 'application/json',
    'api-key': api_key
}
 
response = requests.post(endpoint, headers=headers, json=request_body)
strresponse = response.text
# Parse the JSON response into a Python dictionary
response_dict = json.loads(strresponse)
# Extract the content from the response dictionary and print it
content = response_dict['choices'][0]['message']['content']
#content is my final response from API
#SENDING TO CLIENT FROM TWILIO RECORD
#send the message
message = client.messages.create(
  from_='whatsapp:+14155238886',
  body=content, 
  to='whatsapp:+85292097959'
)
# Send a request to endpoint (query answered)
headers = {'Content-Type': 'application/x-www-form-urlencoded'}  
data = {  
    "from": message.from_,  
    "body": content,  
    "to": message.to,  
    "message_sid": message.sid  
}  
response = requests.post('https://whatsapplogic.azurewebsites.net:443/api/whatsapp/triggers/When_a_HTTP_request_is_received/invoke?api-version=2022-05-01&sp=%2Ftriggers%2FWhen_a_HTTP_request_is_received%2Frun&sv=1.0&sig=LT-HSoWcDtUGnAPuoJEEtF8f5077ZwhNDQ9CrdaVyXs', data=data, headers=headers)
