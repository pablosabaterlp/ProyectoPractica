from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from msrest.authentication import ApiKeyCredentials
import os, time, uuid, requests, cv2

training_key ='key'
training_endpoint ='endpoint'
prediction_key = 'key'
prediction_endpoint = 'endpoint'
project_id = 'id'
publish_iteration_name = 'Iteration3'

# Now there is a trained endpoint that can be used to make a prediction
prediction_credentials = ApiKeyCredentials(in_headers={"Prediction-key": prediction_key})
predict = CustomVisionPredictionClient(prediction_endpoint, prediction_credentials)

# Function to analyze the image
def analyze_image(file_path):
    response = requests.get(file_path)
    response.raise_for_status()
    image_data = response.content

    #with open(file_path, "rb") as f:
        #image_data = f.read()

    results = predict.detect_image(project_id, publish_iteration_name, image_data)

    occupied_list = []
    occupied_prob_total = 0
    unoccupied_list = []
    unoccupied_prob_total = 0
    total_spots = 0

    # Display the results
    for prediction in results.predictions:
        if prediction.tag_name == "Occupied":
            if prediction.probability > 0.8:
                occupied_list.append(prediction)
                occupied_prob_total += prediction.probability
        elif prediction.tag_name == "Unoccupied":
            if prediction.probability > 0.8:
                unoccupied_list.append(prediction)
                unoccupied_prob_total += prediction.probability
        elif prediction.tag_name == "Chair":
            if prediction.probability > 0.9:
                total_spots += 1
        #if prediction.probability > 0.8:
            #print(f"\t{prediction.tag_name}: {prediction.probability * 100:.2f}% "
                #f"bbox.left = {prediction.bounding_box.left:.2f}, "
                #f"bbox.top = {prediction.bounding_box.top:.2f}, "
                #f"bbox.width = {prediction.bounding_box.width:.2f}, "
                #f"bbox.height = {prediction.bounding_box.height:.2f}")

    occupied_count = len(occupied_list)
    unoccupied_count = len(unoccupied_list)
    print(f"# of Spaces: {total_spots}")
    print(f"# of Occupied Spots: {occupied_count}")
    if occupied_count > 0:
        occupied_avg_prob = occupied_prob_total / occupied_count * 100
        print(f"Average Occupied Probability: {occupied_avg_prob:.2f}")
    else:
        occupied_avg_prob = 0
        print("No occupied spots detected.")

    print(f"# of Unoccupied Spots: {unoccupied_count}")
    if unoccupied_count > 0:
        unoccupied_avg_prob = unoccupied_prob_total / unoccupied_count * 100
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
image_url = 'https://www.infsoft.com/wp-content/uploads/infsoft-occupancy-workspaces.jpg' # Replace with your image url
file_path = '/Users/pablosabater/Downloads/IMG_5443.jpeg'
results = analyze_image(image_url)
