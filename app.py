import os
from flask import Flask, jsonify,request
import asyncio
import aiohttp
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
whisperUrl = "https://whisper.lablab.ai/asr"

@app.route('/api/getDialogText', methods=['GET'])
def get_data():
    # Return the dialog text as a JSON object
    unityJson = {"list": dialogTextToReturn}
    return jsonify(unityJson)

# Recieves a user's dialog in terms of audio that is wav encoded, along with the audio sequence and character information.
@app.route("/processWithAI", methods=["POST"])
async def processData():
    # Get the JSON payload containing the audio data
    wavDialogJson = request.get_json()
    # Send the audio data to the OpenAI Whisper API
    asyncio.run(sendToWhisper(wavDialogJson))
    return "processing"

async def sendToWhisper(wavDialogJson):
    async with aiohttp.ClientSession() as session:
        async with session.post(whisperUrl,
                                data=wavDialogJson['audio'],
                                headers={
                                'Content-Type': 'application/octet-stream',
                                #'Authorization': 'Bearer YOUR_OPENAI_API_KEY'
                                }) as resp:
            if resp.status == 200:
                whisperText = await resp.text()
                #Format the dialogObjectForUser
                userDialog = {
                    "samplePosition": wavDialogJson["samplePosition"],
                    "character":  wavDialogJson["character"],
                    "fromUser": True,
                    "textStatement": whisperText
                }
                await dialogTextToReturn.append(userDialog)
                #return the text response from whisper as a text.
                asyncio.run(talkToGPT3(userDialog))
            else:
                raise ValueError(f'Received non-200 status code: {resp.status}')

async def talkToGPT3(userDialog):
    async with aiohttp.ClientSession() as session:
        async with session.get('https://api.openai.com/v1/completions', params={
            'prompt': userDialog["textStatement"],
            'model': 'gpt-3',
            'max_tokens': 512,
            'temperature': 0.5,
        }) as response:
            if response.status == 200:
                gptText = await response.text()
                gptDialog = {
                        "samplePosition": userDialog["samplePosition"],
                        "character":  userDialog["character"],
                        "fromUser": False,
                        "textStatement": gptText
                }
                await dialogTextToReturn.append(gptDialog)
            else:
                raise ValueError(f'Received non-200 status code: {response.status}')

if __name__ == "__main__":
    app.run()