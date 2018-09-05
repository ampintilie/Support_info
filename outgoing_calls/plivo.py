#!/usr/bin/python

import plivo
from flask import Flask,request

def make_call(message):
    #Set your account ID and authentication token.
    a_id = "xxxxxxxxxxxxxxxxxxxx"
    a_token = "xxxxxxxxxxxxxxxxxxxxxx"
    #Create response
    response = plivo.plivoxml.ResponseElement()
    response.add_speak(message)

    #Initialize the Plivo client.
    p = plivo.RestClient(auth_id=a_id, auth_token=a_token)
    #Make the call
    call_made = p.calls.create(
        to_ = 'my_number',
        from_ = 'my_plivo_number',
        answer_url = 'http://urlecho.appspot.com/echo?status=200&Content-Type=text%2Fxml&body=' + response.to_string())

    print call_made

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