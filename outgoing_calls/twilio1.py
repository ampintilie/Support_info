#!/usr/bin/python
from flask import Flask,request
from urllib import urlencode
from twilio.rest import Client

def make_call(message):
    #Set your account ID and authentication token.
    account_sid = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    auth_token = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

    #The number of the phone initiating the call.
    #This should either be a Twilio number or a number that you've verified
    from_number = "xxxxxxxxxxxx"

    #The number of the phone receiving call.
    to_number = "xxxxxxxxxxxxx"

    #Use the Twilio-provided site for the TwiML response.
    url = "http://twimlets.com/message?"

    #Initialize the Twilio client.
    client = Client(account_sid, auth_token)

    #Make the call.
    call = client.calls.create(to=to_number,
                               from_=from_number,
                               url=url + urlencode({'Message': message}))
    print(call.sid)

# Create the application instance
app = Flask(__name__)

# Create a URL route in our application for "/"
@app.route('/',methods=['GET','POST'])
def response():
    #Receive data from jira service desk webhook
    data = request.get_json(force=True)
    #The phone message text.
    message = "New issue created:" + data['issue']['key']
    make_call(message)
    return "Call ended"

# If we're running in stand alone mode, run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)