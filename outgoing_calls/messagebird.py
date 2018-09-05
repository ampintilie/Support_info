#!/usr/bin/python
from flask import Flask,request
import messagebird

ACCESS_KEY = 'xxxxxxxxxxxxxxxxxxx'

def send_voice(message):
    #Initialize the client.
    client = messagebird.Client(ACCESS_KEY)
    #Send message to phone number
    msg = client.message_create('FromMe', 'mynumber', message, { 'reference' : 'Foobar' })
    #Send voice message to phone number
    voice_message = client.voice_message_create('mynumber', 'New issue created,' + message, { 'language' : 'en-gb', 'voice': 'male' })

# Create the application instance
app = Flask(__name__)

# Create a URL route in our application for "/"
@app.route('/',methods=['GET','POST'])
def response():
    #Receive data from jira service desk webhook
    data = request.get_json(force=True)
    print data['issue']['fields']
    print "**********"
    a=str(data['issue']['key']) + str(data['issue']['fields']['summary'])
    send_voice(a)
    return "Call ended"

# If we're running in stand alone mode, run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)