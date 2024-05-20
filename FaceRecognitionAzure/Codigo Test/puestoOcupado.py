from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from msrest.authentication import ApiKeyCredentials
import time, requests, imageio, cv2, os

training_key = os.environ.get('VISION_TRAINING_KEY')
training_endpoint = os.environ.get('VISION_TRAINING_ENDPOINT')
prediction_key = os.environ.get('VISION_PREDICTION_KEY')
prediction_endpoint = os.environ.get('VISION_PREDICTION_ENDPOINT')
resource_id = os.environ.get('VISION_PREDICTION_RESOURCE_ID')

credentials = ApiKeyCredentials(in_headers={"Prediction-key":prediction_key})
predictor = CustomVisionPredictionClient(endpoint,credentials)

