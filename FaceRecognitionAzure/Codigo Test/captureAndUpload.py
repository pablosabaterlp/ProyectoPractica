import os, cv2, uuid, io
import numpy as np
from azure.storage.blob import BlobClient, BlobServiceClient, ContainerClient
from read_line import read_line
from datetime import datetime

conn_string = read_line('/Users/pablosabater/Desktop/Santander/Scripts/storageClientConnString.txt', 0)
conn_name="fotos-camara"

blob_service_client = BlobServiceClient.from_connection_string(conn_string)
container_client = blob_service_client.get_container_client(conn_name)

def captureAndUpload():
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
    blobname = "webcamimage.jpg"
    blob_client = container_client.get_blob_client(blobname)

    try:
        blob_client.upload_blob(image_bytes)
        print(f"Image uploaded successfully as {blobname}")
    except Exception as e: 
        print(f"Failed to upload: {e}")

def getmostrecentblob():
    blob_list = container_client.list_blobs()
    lastBlob = None
    lastTime = datetime.min

    for blob in blob_list:
        if blob.last_modified > lastTime:
            lastBlob = blob
            lastTime = blob.last_modified
        return lastBlob
    
def downloadImage(blobName):
    blob_client = container_client.get_blob_client(blobName)
    blob_data = blob_client.download_blob().readall()

    array = np.frombuffer(blob_data, np.uint8)

    img = cv2.imencode(array, cv2.IMREAD_COLOR)

    if img is None:
        print("Failed to decode image.")
        return
    
    return img