import os
from flask import Flask, jsonify,request
from flask_restful import Api, Resource

#Creating a flask template
#http://localhost:5000 is the url for this when run locally
app=Flask(__name__)
api=Api(app)
# Define the mock dialog to be returned as json
dialogTextToReturn = [ 
    { "samplePosition": 0, "character": "Ol Red", "fromUser": False, "textStatement": "I've been where I've been I reckon" },
    { "samplePosition": 0, "character": "Ol Red", "fromUser": True, "textStatement": "Well hello there Ol Red, how have you been?"}
]

@app.route('/api/getDialogText', methods=['GET'])
def get_data():
    # Return the dialog text as a JSON object
    return jsonify(dialogTextToReturn)


# Define the API's endpoints and methods
@app.route("/send_mp3", methods=["POST"])
def send_mp3():
    # Get the mp3 file from the request
    mp3_file = request.files["mp3_file"]
    # Save the mp3 file to the server
    mp3_file.save(os.path.join(app.config['UPLOAD_FOLDER'], mp3_file.filename))
    # Return the file name

    return mp3_file.filename
    
    #send the mp3 file to whisper
    response = whisper.send_audio_file(mp3_file)

    #return the text response from whisper as a text.
    return response.text
if __name__ == "__main__":
    app.run()