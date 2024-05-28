from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from msrest.authentication import ApiKeyCredentials
from read_line import read_line
from captureAndUpload import captureAndUpload, getmostrecentblob, downloadImage
import azure.functions as func
import logging, cv2, time

# Definir 
prediction_key = read_line('/Users/pablosabater/Desktop/Santander/Scripts/customVisionKeys.txt', 2)
prediction_endpoint = read_line('/Users/pablosabater/Desktop/Santander/Scripts/customVisionKeys.txt', 3)
project_id = read_line('/Users/pablosabater/Desktop/Santander/Scripts/customVisionKeys.txt', 4)
publish_iteration_name = 'Iteration4'

# Inicializar el modelo de Custom Vision entrenado manualmente 
prediction_credentials = ApiKeyCredentials(in_headers={"Prediction-key": prediction_key})
predict = CustomVisionPredictionClient(prediction_endpoint, prediction_credentials)


def keyExists(key, value, list):
    for dict in list:
        if dict.get(key) == value:
            return True
    return False

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

# Funcion para analizar una imagen y representarla en power BI
@app.route(route="http_trigger")
def http_trigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')    
    
    name = req.params.get('name')

    timeout = time.time() + 30
    while True: 
        # Para tomar foto y mandarla directamente al blob storage de Azure
        #captureAndUpload()
        lastblob = getmostrecentblob()
        imgshape, image_data = downloadImage(lastblob)

        # Llamar el contenedor de custom vision predict
        results = predict.detect_image(project_id, publish_iteration_name, image_data)

        desk_positions = {1: {'x': 760, 'y': 320},
                            2: {'x': 1000, 'y': 310},
                            3: {'x': 730, 'y': 410},
                            4: {'x': 1110, 'y': 410},
                            5: {'x': 520, 'y': 580},
                            6: {'x': 1150, 'y': 580},
                            7: {'x': 380, 'y': 890},
                            8: {'x': 1200, 'y': 920}}

        # Codigo para actualizar documento de excel y power BI
        desk_statuses = []
        for prediction in results.predictions:
            if prediction.tag_name == 'Occupied' or prediction.tag_name == 'Unoccupied':
                if prediction.probability > 0.5:
                    leftpred = int(prediction.bounding_box.left * imgshape[1])
                    toppred = int(prediction.bounding_box.top * imgshape[0])
                    widthpred = int(prediction.bounding_box.width * imgshape[1])
                    heightpred = int(prediction.bounding_box.height * imgshape[0])
                    predcenter_x = leftpred + widthpred / 2
                    predcenter_y = heightpred + toppred / 2

                    for desknum, position in desk_positions.items():
                        if abs(predcenter_x - position['x']) < 150 and abs(predcenter_y - position['y']) < 150:
                            if not keyExists('Desk', desknum, desk_statuses):
                                if prediction.tag_name == 'Occupied':
                                    desk_statuses.append({'Desk':desknum, 'Status':1})
                                else:
                                    desk_statuses.append({'Desk':desknum, 'Status':0})
        # Se asume que si no se detecta un puesto como occupado, entonces estara desocupado
        for desknum in desk_positions.keys():
            if not keyExists('Desk', desknum, desk_statuses):
                desk_statuses.append({'Desk': desknum, 'Status': 0})
        print(desk_statuses)

        time.sleep(60)

        if time.time() > timeout:
              break
        

    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
            "This HTTP triggered function executed successfully.",
            status_code=200
            )