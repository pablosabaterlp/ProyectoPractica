from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from msrest.authentication import ApiKeyCredentials
from read_line import read_line
from captureAndUpload import captureAndUpload, getmostrecentblob, downloadImage
from datetime import datetime
import azure.functions as func
import logging, openpyxl

# Definir 
prediction_key = read_line('TXTFILE', 'LINE#')
prediction_endpoint = read_line('TXTFILE', 'LINENUM')
project_id = read_line('TXTFILE', 'LINENUM')
publish_iteration_name = 'ITERATIONNUM'
file_path = 'FILEPATH'

# Inicializar el modelo de Custom Vision entrenado manualmente 
prediction_credentials = ApiKeyCredentials(in_headers={"Prediction-key": prediction_key})
predict = CustomVisionPredictionClient(prediction_endpoint, prediction_credentials)

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
    
    imgshape = ['WIDTH', 'HEIGHT']
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
                            8: {'x': 1200, 'y': 920 #Values should be manually changed according to location of the center of desk spaces in the images
                               }}

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

    excel = {1: 'C3', 2:'C4', 3:'C5', 4:'C6', 5:'C7', 6:'C8', 7:'C9', 8:'C10'} #Should be modified depending on the spreadsheet created

    for desk in desk_statuses:
        bidesknum = desk['Desk']
        bistatus = desk['Status']
        editCell(file_path, cell=excel[bidesknum], value=bistatus)

    logging.info(f'Python timer trigger function ran at {timestamp}')
