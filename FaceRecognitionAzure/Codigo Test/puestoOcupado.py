from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from msrest.authentication import ApiKeyCredentials
from read_line import read_line
from captureAndUpload import captureAndUpload, getmostrecentblob, downloadImage
from draw_image import draw_results
import numpy as np
import pandas as pd
import os, time, uuid, requests, cv2

# Definir 
prediction_key = read_line('/Users/pablosabater/Desktop/Santander/Scripts/customVisionKeys.txt', 2)
prediction_endpoint = read_line('/Users/pablosabater/Desktop/Santander/Scripts/customVisionKeys.txt', 3)
project_id = read_line('/Users/pablosabater/Desktop/Santander/Scripts/customVisionKeys.txt', 4)
publish_iteration_name = 'Iteration4'

# Inicializar el modelo de Custom Vision entrenado manualmente 
prediction_credentials = ApiKeyCredentials(in_headers={"Prediction-key": prediction_key})
predict = CustomVisionPredictionClient(prediction_endpoint, prediction_credentials)


# Funcion para analizar una imagen y representarla en power BI
def analyze_image():
    # Codigo para utilizar foto del internet
    #response = requests.get(file_path)
    #response.raise_for_status()
    #image_data = response.content

    # Codigo para utilizar foto guardada en local
    #with open(file_path, "rb") as f:
        #image_data = f.read()

    # Para tomar foto y mandarla directamente al blob storage de Azure
    captureAndUpload()
    lastblob = getmostrecentblob()
    image_data = downloadImage(lastblob)

    # Llamar el contenedor de custom vision predict
    results = predict.detect_image(project_id, publish_iteration_name, image_data)

    # Definir resultados vacios 
    occupied_list = []
    occupied_prob_total = 0
    unoccupied_list = []
    unoccupied_prob_total = 0
    total_spots = 0

    # Sacar resultados del modelo Custom Vision
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
            if prediction.probability > 0.90:
                total_spots += 1

    occupied_count = len(occupied_list)
    unoccupied_count = len(unoccupied_list)

    # Imprimir el numero total de puestos, detectado por el numero de sillas 
    if total_spots > occupied_count and total_spots > unoccupied_count:
        print(f"# de Puestos: {total_spots}")
    elif total_spots < occupied_count or total_spots < unoccupied_count:
        print(f"# de Puestos: {occupied_count + unoccupied_count}")
    
    # Imprimir el numero total de puestos ocupados, y la probabilidad de acertaje solo si hay algun puesto ocupado
    print(f"# de Puestos Occupados: {occupied_count}")
    if occupied_count > 0:
        occupied_avg_prob = occupied_prob_total / occupied_count * 100
        print(f"Probabilidad de Acertaje: {occupied_avg_prob:.2f}")
    else:
        occupied_avg_prob = 0
        print("No se detectan sitios ocupados.")

    # Imprimir la cantidad de puestos desocupados para que la suma de los ocupados y libres siempre sea igual a la cantidad total de puestos
    if total_spots > occupied_count and total_spots > unoccupied_count:
        print(f"# de Puestos Libres: {total_spots - occupied_count}")
    else: 
        print(f"# de Puestos Libres: {unoccupied_count}")
    if unoccupied_count > 0:
        unoccupied_avg_prob = unoccupied_prob_total / unoccupied_count * 100
        print(f"Probabilidad de Acertaje: {unoccupied_avg_prob:.2f}")
    else:
        unoccupied_avg_prob = 0
        print("No se detectan sitios desocupados.")
    
    # Codigo para actualizar documento de excel y power BI
    
    

results = analyze_image()
