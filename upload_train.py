import time
import json
from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient
from azure.cognitiveservices.vision.customvision.training.models import ImageFileCreateBatch, ImageFileCreateEntry
from msrest.authentication import ApiKeyCredentials
import argparse
import os

# Start by `python3 upload_train.py --covid data/CT_COVID --noncovid data/CT_NonCOVID`
ap = argparse.ArgumentParser()
ap = argparse.ArgumentParser()
ap.add_argument("-c", "--covid", required=True,
                help="path to base directory for COVID-19 dataset")
ap.add_argument("-o", "--noncovid", required=True,
                help="path to base directory for normal people dataset")
args = vars(ap.parse_args())

with open("credentials.json") as json_file:
    data = json.load(json_file)
    os.environ['resource_endpoint'] = data['resource_endpoint']
    os.environ['training_key'] = data['training_key']
    os.environ['prediction_resource_id'] = data['prediction_resource_id']


# All the keys will be put in a credentials file later
ENDPOINT = os.environ.get('resource_endpoint')
training_key = os.environ.get('training_key')
prediction_resource_id = os.environ.get('prediction_resource_id')

publish_iteration_name = "classifyModel"

credentials = ApiKeyCredentials(in_headers={"Training-key": training_key})
trainer = CustomVisionTrainingClient(ENDPOINT, credentials)

# Create a new project
print("[INFO] Creating project")
project = trainer.create_project("COVID19-detector-based-on-CTscan-img")

positive_tag = trainer.create_tag(project.id, "Positive")
negative_tag = trainer.create_tag(project.id, "Negative")

print("[INFO] Uploading data")
image_list = []

for filename in os.listdir(args["covid"]):
    img_path = os.path.sep.join([args["covid"], filename])
    with open(img_path, "rb") as image_contents:
        image_list.append(ImageFileCreateEntry(
            name=filename, contents=image_contents.read(), tag_ids=[positive_tag.id]))

for filename in os.listdir(args["noncovid"]):
    img_path = os.path.sep.join([args["noncovid"], filename])
    with open(img_path, "rb") as image_contents:
        image_list.append(ImageFileCreateEntry(
            name=filename, contents=image_contents.read(), tag_ids=[negative_tag.id]))

# Azure allows uploading 64 images per batch at once
for i in range(0, len(image_list), 64):
    print("[INFO] Uploading batch: ", i)
    batch = image_list[i:i+64]
    upload_result = trainer.create_images_from_files(
        project.id, ImageFileCreateBatch(images=batch))
    if not upload_result.is_batch_successful:
        print("Image batch upload failed.")
        for image in upload_result.images:
            print("Image status: ", image.status)

# Train model and publish
print("[INFO] Training...")
iteration = trainer.train_project(project.id)
while (iteration.status != "Completed"):
    iteration = trainer.get_iteration(project.id, iteration.id)
    print("[INFO] Training status: " + iteration.status)
    time.sleep(1)

# The iteration is now trained. Publish it to the project endpoint
trainer.publish_iteration(project.id, iteration.id,
                          publish_iteration_name, prediction_resource_id)
print("Done training. Published!")
