from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from msrest.authentication import ApiKeyCredentials
import os, time, uuid, requests, cv2

training_key = 'dc04ada586134feaa1fdaa543c592fdd'
training_endpoint ='https://chls1zu1cvbpocaaicrit001.cognitiveservices.azure.com/'
prediction_key = 'f97fa93036b5479da5f70f31150d6f0d'
prediction_endpoint = 'https://chls1zu1cvbpocaaicrit001-prediction.cognitiveservices.azure.com/'
project_id = '7459c025-eac8-4078-ab8a-5407dee1987f'
publish_iteration_name = 'Iteration4'

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
            if prediction.probability > 0.95:
                total_spots += 1
        #if prediction.probability > 0.8:
            #print(f"\t{prediction.tag_name}: {prediction.probability * 100:.2f}% "
                #f"bbox.left = {prediction.bounding_box.left:.2f}, "
                #f"bbox.top = {prediction.bounding_box.top:.2f}, "
                #f"bbox.width = {prediction.bounding_box.width:.2f}, "
                #f"bbox.height = {prediction.bounding_box.height:.2f}")

    occupied_count = len(occupied_list)
    unoccupied_count = len(unoccupied_list)
    if total_spots > occupied_count and total_spots > unoccupied_count:
        print(f"# de Puestos: {total_spots}")
    elif total_spots < occupied_count or total_spots < unoccupied_count:
        print(f"# de Puestos: {occupied_count + unoccupied_count}")
    
    print(f"# de Puestos Occupados: {occupied_count}")
    if occupied_count > 0:
        occupied_avg_prob = occupied_prob_total / occupied_count * 100
        print(f"Probabilidad de Acertaje: {occupied_avg_prob:.2f}")
    else:
        occupied_avg_prob = 0
        print("No se detectan sitios ocupados.")

    print(f"# de Puestos Desocupados: {unoccupied_count}")
    if unoccupied_count > 0:
        unoccupied_avg_prob = unoccupied_prob_total / unoccupied_count * 100
        print(f"Probabilidad de Acertaje: {unoccupied_avg_prob:.2f}")
    else:
        unoccupied_avg_prob = 0
        print("No se detectan sitios desocupados.")

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
