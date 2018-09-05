#!/usr/bin/python
from flask import Flask,request
from twilio.twiml.voice_response import VoiceResponse, Say
from twilio.rest import Client
import urllib

def makeCall(message):
    #Set your account ID and authentication token.
    account_sid = 'xxxxxxxxxxxxxxxxxxxxxx'
    auth_token = 'xxxxxxxxxxxxxxxxxxxxxxx'

    #Use the Twilio-provided site for the TwiML response and add the message
    answer_url = 'http://twimlets.com/echo?Twiml=' + urllib.quote_plus(message.to_xml())

    #Initialize the Twilio client.
    client = Client(account_sid, auth_token)
    #Make the call
    call = client.calls.create(
        url=answer_url,
        to='my_number',
        from_='my_twilio_number')
    print(call.sid)

# Create the application instance
app = Flask(__name__)

# Create a URL route in our application for "/"
@app.route('/',methods=['GET','POST'])
def response():
    #Receive data from jira service desk webhook
    data = request.get_json(force=True)
    print data['issue']['fields']['summary']
    print data['issue']['fields']['description']
    print data['issue']['key']

    #The phone message text.
    message = VoiceResponse()
    say = Say("New issue created: " + data['issue']['key'])
    message.append(say)
    say.ssml_break(strength='x-weak', time='100ms')
    message.say("Description:" + data['issue']['fields']['description'])
    print message

    makeCall(message)
    return "Call ended"

# If we're running in stand alone mode, run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)