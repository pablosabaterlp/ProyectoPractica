from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from msrest.authentication import ApiKeyCredentials
import time, requests, imageio, cv2, os

prediction_key = "predicition key"
endpoint = "endpoint"
project_id = "custom vis project id"

credentials = ApiKeyCredentials(in_headers={"Prediction-key":prediction_key})
predictor = CustomVisionPredictionClient(endpoint,credentials)

