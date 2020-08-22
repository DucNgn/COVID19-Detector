from classifier import getPredictionByPATH, getPredictionByURL
from dataInfo import extractTrainedData
import secrets
from hashlib import md5
from time import localtime
import os
import re

from flask import (Flask,
                   flash,
                   redirect,
                   request,
                   render_template,
                   send_from_directory)
from werkzeug.utils import secure_filename

# Config environment variables
os.environ['PORT'] = '5000'
os.environ['IMAGE_UPLOAD'] = "./static/temp"
app = Flask(__name__, static_folder="static")
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["JPEG", "JPG", "PNG"]
app.config["MAX_IMAGE_SIZE"] = 50 * 1024 * 1024
app.config["CUSTOM_STATIC_PATH"] = "data/CT_COVID"

# Extract all detailed data at the start
detailedData = extractTrainedData()


@app.errorhandler(404)
def not_found(e):
    return redirect("/")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/index", methods=["GET", "POST"])
def upload_image():
    if request.method == "POST" and request.form['img-url'] != "":
        inputURL = request.form['img-url']
        # Regex to check if it's a valid image url
        checkLink = re.search(
            "(http(s?):)([/|.|\w|\s|-])*\.(?:jpg|png|jpeg|bmp)", inputURL)
        if checkLink is None:
            flash("Invalid Image URL", "warning")
            return redirect(request.url)

        (result, probs) = getPredictionByURL(inputURL)
        if result is None:
            flash(
                "Could not detect a chest CT scan "
                + "in the provided image", "info")
            return redirect(request.url)
        else:
            if result is True:
                claimer = "Positive with COVID-19 with precision of: " + \
                    "{0:.2f}%".format(probs['Positive'] * 100)
            else:
                claimer = "Negative with COVID-19 with precision of: " + \
                    "{0:.2f}%".format(probs['Negative'] * 100)
            return render_template("index.html", claimer=claimer, provided_img=inputURL, isReturn="true")

    # Upload file from local for prediction
    tempLoc = str(os.environ.get('IMAGE_UPLOAD'))
    if request.method == "POST":
        if not os.path.exists(tempLoc):
            os.makedirs(tempLoc)

        if request.files:
            if "filesize" in request.cookies:
                image = request.files['image']

                if not imageSize_is_allowed(request.cookies["filesize"]):
                    # Check for file size limit
                    flash("File size exceeds maximum limit", "warning")
                    return redirect(request.url)

                if image.filename == "":
                    # Check if it is not empty file
                    flash("Please upload an image to begin", "warning")
                    return redirect(request.url)

                if not image_is_allowed(image.filename):
                    # Check extension of the file
                    flash("File extension is not allowed", "warning")
                    return redirect(request.url)
                else:
                    filename = secure_filename(image.filename)
                    imgPath = os.path.join(tempLoc, filename)
                    image.save(imgPath)
                    print("[INFO] Image saved")
                    (result, probs) = getPredictionByPATH(imgPath)
                    if result is None:
                        flash(
                            "Could not detect a chest CT scan"
                            + " in the provided image",
                            "info")
                        clean_Tempdir(tempLoc, filename)
                        return redirect(request.url)
                    else:
                        tempImgPath = generateImgPath(tempLoc, filename)
                        os.rename(imgPath, tempImgPath)
                        if result is True:
                            claimer = "Positive with COVID-19 with precision of: " + \
                                "{0:.2f}%".format(probs['Positive'] * 100)
                        else:
                            claimer = "Negative with COVID-19 with precision of: " + \
                                "{0:.2f}%".format(probs['Negative'] * 100)
                        return render_template("index.html", claimer=claimer, provided_img=tempImgPath, isReturn = "true")
    return render_template("index.html")


def image_is_allowed(image_name):
    if "." not in image_name:
        return False
    ext = image_name.rsplit(".", 1)[1]
    return (ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"])


def imageSize_is_allowed(image_size):
    return (int(image_size) <= app.config['MAX_IMAGE_SIZE'])


def clean_Tempdir(tempLocation, filename):
    dirPath = os.path.join(tempLocation, filename)
    os.remove(dirPath)


def generateImgPath(tempLocation, filename):
    prefix = "tempImg." + md5(str(localtime()).encode('utf-8')).hexdigest()
    tempImgName = f"{prefix}__{filename}"
    return os.path.join(tempLocation, tempImgName)

# Custom static data


@app.route('/data/<path:filename>')
def custom_static(filename):
    return send_from_directory(app.config['CUSTOM_STATIC_PATH'], filename)


@app.route("/presentdata", methods=['GET'])
def presentdata():
    return render_template("presentData.html", data=detailedData)


if __name__ == '__main__':
    secret_key = secrets.token_hex(16)
    app.config['SECRET_KEY'] = secret_key
    port = int(os.environ['PORT'])
    app.run(debug=True, host='0.0.0.0', port=port)
