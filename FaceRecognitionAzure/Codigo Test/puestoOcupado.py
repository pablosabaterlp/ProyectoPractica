from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient
from msrest.authentication import ApiKeyCredentials
import os, time, uuid, requests, cv2

training_key ='dc04ada586134feaa1fdaa543c592fdd'
training_endpoint ='https://chls1zu1cvbpocaaicrit001.cognitiveservices.azure.com/'
prediction_key = 'f97fa93036b5479da5f70f31150d6f0d'
prediction_endpoint = 'https://chls1zu1cvbpocaaicrit001-prediction.cognitiveservices.azure.com/'
project_id = 'a86b8252-af12-4a18-a3aa-171e87725305'
publish_iteration_name = "Iteration1"

# Now there is a trained endpoint that can be used to make a prediction
prediction_credentials = ApiKeyCredentials(in_headers={"Prediction-key": prediction_key})
predictor = CustomVisionPredictionClient(prediction_endpoint, prediction_credentials)

# Function to analyze the image
def analyze_image(image_path):
    with open(image_path, "rb") as test_data:
        # Get the prediction results
        results = predictor.detect_image(project_id, publish_iteration_name, test_data)

    occupied_list = []
    occupied_prob_total = 0
    unoccupied_list = []
    unoccupied_prob_total = 0

    # Display the results
    for prediction in results.predictions:
        if prediction.tag_name == "Occupied":
            occupied_list.append(prediction)
            occupied_prob_total += prediction.probability
        elif prediction.tag_name == "Unoccupied":
            unoccupied_list.append(prediction)
            unoccupied_prob_total += prediction.probability
        print(f"\t{prediction.tag_name}: {prediction.probability * 100:.2f}% "
              f"bbox.left = {prediction.bounding_box.left:.2f}, "
              f"bbox.top = {prediction.bounding_box.top:.2f}, "
              f"bbox.width = {prediction.bounding_box.width:.2f}, "
              f"bbox.height = {prediction.bounding_box.height:.2f}")

    occupied_count = len(occupied_list)
    unoccupied_count = len(unoccupied_list)

    print(f"# of Occupied Spots: {occupied_count}")
    if occupied_count > 0:
        occupied_avg_prob = occupied_prob_total / occupied_count
        print(f"Average Occupied Probability: {occupied_avg_prob:.2f}")
    else:
        occupied_avg_prob = 0
        print("No occupied spots detected.")

    print(f"# of Unoccupied Spots: {unoccupied_count}")
    if unoccupied_count > 0:
        unoccupied_avg_prob = unoccupied_prob_total / unoccupied_count
        print(f"Average Unoccupied Probability: {unoccupied_avg_prob:.2f}")
    else:
        unoccupied_avg_prob = 0
        print("No unoccupied spots detected.")

    return {
        "occupied_count": occupied_count,
        "unoccupied_count": unoccupied_count,
        "occupied_avg_prob": occupied_avg_prob,
        "unoccupied_avg_prob": unoccupied_avg_prob
    }

# Example usage
image_path = r'C:\Users\psaba\Downloads\infsoft-occupancy-workspaces.jpg' # Replace with your image path
results = analyze_image(image_path)
print(results)
