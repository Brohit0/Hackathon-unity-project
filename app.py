from flask import Flask, jsonify
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

if __name__ == "__main__":
    app.run(debug=True)