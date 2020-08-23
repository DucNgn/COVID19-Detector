# COVID-19 Detector
[Try here](http://covid19-detector.azurewebsites.net/)

<p align="center">
    <img src="./front_page.png">
</p>

COVID-19 detector is a website that uses machine learning to give tentative predictions about an user's probability of contracting COVID-19 by looking at their chest CT-scan.

## How Our Project Aids Health Care Providers
* Help doctors and healthcare workers in diagnosing patients.
* Reduce the load on testing facilities, give priority access to testing kits for people who needed it.

## The Tech We Are Using
* **Flask** : A lightweight Python web application framework
* **Jinja**: for rendering templates from Flask
* **Bootstrap**: A front-end framework
* **Docker**: For containerizing and deploying our service
* A full list of dependencies in the project can be found in `requirements.txt`

#### Our machine learning model:
* Trained with Microsoft Azure Custom Vision AI
* Data set provided by [COVID-CT](https://github.com/UCSD-AI4H/COVID-CT)
    + 329 Chest CT Scan Images of positive COVID-19 patients 
    + 387 Chest CT Scan Images of negative COVID-19 patients 

#### Web Host Service:
* Web hosted on Microsoft Azure Web Service

## Important Project Structure:
+ `data`: folder contains the training image data for the ML model
+ `test_data`: folder contains the images that are separated from training data , for testing purpose.
+ `upload_train.py`: Python script for creating, labelling, uploading, and training model on Azure.
+ `dataInfo.py`: Script uses `pandas` to read `.xlsx` file and extract information 

## Hosting A Local Instance Of Our Website

1. Clone our repository
2. (Optional) Create a virtual python environment
3. Run ```pip install -r requirements.txt``` inside the project root directory
4. Set up your Azure Custom Vision project and create a `credentials.json` file similar to our `credentials_example.json` file.
5. Run ```flask run```
6. The website should be up and running at `localhost:5000`

## Credit:
+ Data set from [COVID-CT](https://github.com/UCSD-AI4H/COVID-CT)
