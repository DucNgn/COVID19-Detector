import os
import json
import requests

with open("credentials.json") as json_file:
    data = json.load(json_file)
    os.environ['predictByURL_endpoint'] = data['predictByURL_endpoint']
    os.environ['predictByPath_endpoint'] = data['predictByPath_endpoint']
    os.environ['Prediction-Key'] = data['Prediction-Key']


def getPredictionByURL(url):
    endpoint = os.environ.get('predictByURL_endpoint')
    headers = {
        'Prediction-Key':
            os.environ.get('Prediction-Key'),
            'Content-Type': 'application/json'
            }
    data = {'url': url}
    response = requests.post(endpoint, headers=headers, json=data)
    response.raise_for_status()
    analysis = response.json()
    return getResult(analysis)


def getPredictionByPATH(img_path):
    print("Received request from path: ", img_path)
    endpoint = os.environ.get('predictByPath_endpoint')
    img_data = open(img_path, "rb").read()
    headers = {'Prediction-Key': os.environ.get(
        'Prediction-Key'), 'Content-Type': 'application/octet-stream'}
    response = requests.post(endpoint, headers=headers, data=img_data)
    response.raise_for_status()
    analysis = response.json()
    return getResult(analysis)


def getResult(data):
    probs = dict()
    probs[data['predictions'][0]['tagName']] = data['predictions'][0]['probability']
    probs[data['predictions'][1]['tagName']] = data['predictions'][1]['probability']
    # discard unrelevant input
    if probs['Positive'] <= 0.5 and probs['Negative'] <= 0.5:
        return (None, probs)
    # legit result
    return (True, probs) if (probs['Positive'] > probs['Negative']) else (False, probs)

print(getPredictionByURL("https://upload.wikimedia.org/wikipedia/commons/d/dc/Alpha_1-antitrypsine_deficiency_lung_CT_scan.JPEG"))