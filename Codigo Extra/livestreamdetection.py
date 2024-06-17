import imageio
import pygame
import threading
import requests
import cv2
import os

# Azure Computer Vision API setup
subscription_key = read_line('TXTPATH', 'LINENUM') 
endpoint = read_line('TXTPATH', 'LINENUM') 
api_url = f"{endpoint}/vision/v3.2/analyze"

# Initialize global variables
running = True
face_boxes = []
frame = None

# Function to get face bounding boxes from Azure Vision API
def get_face_boxes(image_bytes):
    headers = {
        'Ocp-Apim-Subscription-Key': subscription_key,
        'Content-Type': 'application/octet-stream'
    }
    params = {
        'visualFeatures': 'Faces'
    }
    response = requests.post(api_url, headers=headers, params=params, data=image_bytes)
    if response.status_code == 200:
        faces = response.json().get('faces', [])
        face_boxes = []
        for face in faces:
            face_rectangle = face['faceRectangle']
            left = face_rectangle['left']
            top = face_rectangle['top']
            width = face_rectangle['width']
            height = face_rectangle['height']
            face_boxes.append((left, top, width, height))
        return face_boxes
    else:
        print("Error:", response.status_code, response.text)
        return []

# Thread function to process frames and detect faces
def process_frame():
    global running, face_boxes, frame
    while running:
        if frame is not None:
            # Encode frame as JPEG
            _, img_encoded = cv2.imencode('.jpg', frame)
            img_bytes = img_encoded.tobytes()

            # Get face bounding boxes
            try:
                face_boxes = get_face_boxes(img_bytes)
                print("Face boxes:", face_boxes)
            except Exception as e:
                print(f"Error: {e}")
                face_boxes = []

# Initialize pygame
pygame.init()

# Open webcam using imageio
webcam = imageio.get_reader('<video0>', 'ffmpeg')

# Set desired resolution (reduce the resolution to optimize)
desired_resolution = (320, 240)

# Set up pygame window
window = pygame.display.set_mode(desired_resolution)
pygame.display.set_caption('Webcam Live Stream with Face Detection')

# Define desired FPS
desired_fps = 30

# Start the frame processing thread
thread = threading.Thread(target=process_frame)
thread.start()

# Main loop
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Get the latest frame from the webcam
    frame = webcam.get_next_data()

    # Resize frame to desired resolution
    frame = cv2.resize(frame, desired_resolution)

    # Convert the frame to a format pygame can use
    frame_surface = pygame.image.frombuffer(frame.tobytes(), desired_resolution, 'RGB')

    # Display the frame in the pygame window
    window.blit(frame_surface, (0, 0))
    pygame.display.update()

    # Limit FPS
    clock.tick(desired_fps)

# Stop the processing thread
running = False
thread.join()

# Quit pygame
pygame.quit()
