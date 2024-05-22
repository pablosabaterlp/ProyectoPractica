from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient
from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from azure.cognitiveservices.vision.customvision.training.models import ImageFileCreateBatch, ImageFileCreateEntry, Region
from msrest.authentication import ApiKeyCredentials
import os, time, uuid, requests, cv2

training_key = os.environ.get('VISION_TRAINING_KEY') dc04ada586134feaa1fdaa543c592fdd
training_endpoint = os.environ.get('VISION_TRAINING_ENDPOINT') https://chls1zu1cvbpocaaicrit001.cognitiveservices.azure.com/
prediction_key = os.environ.get('VISION_PREDICTION_KEY') f97fa93036b5479da5f70f31150d6f0d
prediction_endpoint = os.environ.get('VISION_PREDICTION_ENDPOINT') https://chls1zu1cvbpocaaicrit001-prediction.cognitiveservices.azure.com/
resource_id = os.environ.get('VISION_PREDICTION_RESOURCE_ID') /subscriptions/a86b8252-af12-4a18-a3aa-171e87725305/resourceGroups/chls1zu1rsgpocaaicrit001/providers/Microsoft.CognitiveServices/accounts/chls1zu1cvbpocaaicrit001-Prediction
ad3068fd-6464-4f6c-a02f-890a94d96707
# Now there is a trained endpoint that can be used to make a prediction
prediction_credentials = ApiKeyCredentials(in_headers={"Prediction-key": prediction_key})
predictor = CustomVisionPredictionClient(prediction_endpoint, prediction_credentials)

# Open the sample image and get back the prediction results.
with open(os.path.join (base_image_location, "test", "test_image.jpg"), mode="rb") as picture:
    results = predictor.detect_image(project.id, publish_iteration_name, test_data)

occupiedlist = []
occupiedprobtotal = 0
unoccupiedlist = []
unoccupiedprobtotal = 0
# Display the results.    
for prediction in results.predictions:
    if prediction.tag_name == "Occupied":
        occupiedlist.append(prediction)
        occupiedprobtotal += prediction.probability
    elif prediction.tage_name == "Unoccupied":
        unoccupiedlist.append(prediction)
        unoccupiedprobtotal += prediction.probability
    print("\t" + prediction.tag_name + ": {0:.2f}% bbox.left = {1:.2f}, bbox.top = {2:.2f}, bbox.width = {3:.2f}, bbox.height = {4:.2f} \n".format(prediction.probability * 100, prediction.bounding_box.left, prediction.bounding_box.top, prediction.bounding_box.width, prediction.bounding_box.height))

print("# of Occupied Spots:" + len(occupiedlist) + "\n Probability:" + occupiedprobtotal/len(occupiedlist) + "\n # of Unoccupied Spots:" + len(unoccupiedlist) + "\n Probability:" + unoccupiedprobtotal/len(unoccupiedlist))
