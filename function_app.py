from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from msrest.authentication import ApiKeyCredentials
import azure.functions as func
import logging, openpyxl, cv2, io
import numpy as np
from azure.storage.blob import BlobClient, BlobServiceClient, ContainerClient
from datetime import datetime, timezone

def read_line(path, line):
    with open(path, 'r') as file:
        lines = file.readlines()
        if 0 <= line < len(lines):
            return lines[line].strip()
        else:
            raise ValueError("Line Number out of Range")
        
# Definir 
prediction_key = read_line('/Users/pablosabater/Desktop/Santander/Scripts/customVisionKeys.txt', 2)
prediction_endpoint = read_line('/Users/pablosabater/Desktop/Santander/Scripts/customVisionKeys.txt', 3)
project_id = read_line('/Users/pablosabater/Desktop/Santander/Scripts/customVisionKeys.txt', 4)
publish_iteration_name = 'Iteration4'
file_path = '/Users/pablosabater/Library/CloudStorage/OneDrive-NortheasternUniversity/Other/Mapa de Oficina Practica.xlsx'

# Inicializar el modelo de Custom Vision entrenado manualmente 
prediction_credentials = ApiKeyCredentials(in_headers={"Prediction-key": prediction_key})
predict = CustomVisionPredictionClient(prediction_endpoint, prediction_credentials)
conn_string = read_line('/Users/pablosabater/Desktop/Santander/Scripts/storageClientConnString.txt', 0)
conn_name="fotos-camara"

blob_service_client = BlobServiceClient.from_connection_string(conn_string)
container_client = blob_service_client.get_container_client(conn_name)

def captureAndUpload():
    now = datetime.now()
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()
    if not ret:
        print("Image capture failed.")
        return
    success, buffer = cv2.imencode(".jpg", frame)
    if not success:
        print("Failed to encode image.")
        return
    image_bytes = io.BytesIO(buffer).getvalue()
    blobname = f"{now}.jpg"
    blob_client = container_client.get_blob_client(blobname)

    try:
        blob_client.upload_blob(image_bytes)
        print(f"Image uploaded successfully as {blobname}")
    except Exception as e: 
        print(f"Failed to upload: {e}")

def getmostrecentblob():
    blob_list = container_client.list_blobs()
    lastBlob = None
    lastTime = datetime.min.replace(tzinfo=timezone.utc)

    for blob in blob_list:
        if blob.name.lower().endswith('.jpg') or blob.name.lower().endswith('.jpeg'):
            if blob.last_modified > lastTime:
                lastBlob = blob
                lastTime = blob.last_modified
    return lastBlob
    
def downloadImage(lastBlob):
    blob_client = container_client.get_blob_client(lastBlob)
    blob_data = blob_client.download_blob().readall()

    array = np.frombuffer(blob_data, np.uint8)

    img = cv2.imdecode(array, cv2.IMREAD_COLOR)

    if img is None:
        print("Failed to decode image.")
        return
    
    resized_image = imageResize(img)
    success, encoded_image = cv2.imencode('.jpg', resized_image)
    if success:
        return encoded_image.tobytes()#, img
    else:
        raise ValueError("Failed to encode image.")
 
def imageResize(image, size = (1600, 1200)):
    imgresize = cv2.resize(image, size)
    return imgresize

def editCell(file_path, cell, value):
    # Load the workbook and select the sheet
    workbook = openpyxl.load_workbook(file_path)
    sheet = workbook['Sheet1']
    
    # Edit the specified cell
    sheet[cell] = value
    
    # Save the workbook
    workbook.save(file_path)
    print(f"Cell {cell} in {file_path} updated to {value}")

def deskExists(key, value, list):
    for dict in list:
        if dict.get(key) == value:
            return True
    return False

app = func.FunctionApp()

@app.function_name(name="mytimer")
@app.schedule(schedule="0 */5 * * * *", arg_name="mytimer", run_on_startup=True, use_monitor=False)

def test_function(mytimer: func.TimerRequest) -> None:
    timestamp = datetime.now()

    if mytimer.past_due:
        logging.info('The timer is past due!')
    
    imgshape = [1600, 1200]
    # Para tomar foto y mandarla directamente al blob storage de Azure
    #captureAndUpload()
    lastblob = getmostrecentblob()
    image_data = downloadImage(lastblob)

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
            if prediction.probability > 0.7:
                leftpred = int(prediction.bounding_box.left * imgshape[0])
                toppred = int(prediction.bounding_box.top * imgshape[1])
                widthpred = int(prediction.bounding_box.width * imgshape[0])
                heightpred = int(prediction.bounding_box.height * imgshape[1])
                predcenter_x = leftpred + widthpred / 2
                predcenter_y = heightpred + toppred / 2

                for desknum, position in desk_positions.items():
                    if abs(predcenter_x - position['x']) < 150 and abs(predcenter_y - position['y']) < 150:
                        if not deskExists('Desk', desknum, desk_statuses):
                            if prediction.tag_name == 'Occupied':
                                desk_statuses.append({'Desk':desknum, 'Status':1})
                            else:
                                desk_statuses.append({'Desk':desknum, 'Status':0})
        # Se asume que si no se detecta un puesto como occupado, entonces estara desocupado
    for desknum in desk_positions.keys():
        if not deskExists('Desk', desknum, desk_statuses):
            desk_statuses.append({'Desk': desknum, 'Status': 0})
    print(desk_statuses)

    excel = {1: 'C3', 2:'C4', 3:'C5', 4:'C6', 5:'C7', 6:'C8', 7:'C9', 8:'C10'}

    for desk in desk_statuses:
        bidesknum = desk['Desk']
        bistatus = desk['Status']
        editCell(file_path, cell=excel[bidesknum], value=bistatus)

    logging.info(f'Python timer trigger function ran at {timestamp}')