import requests, os, pygame, io
from PIL import Image

# Initialize Pygame
pygame.init()

# Set Azure Computer Vision API credentials
KEY = read_line('TXTPATH', 'LINENUM')
ENDPOINT = read_line('TXTPATH', 'LINENUM')

# Image URL
imageUrl = 'https://media-cldnry.s-nbcnews.com/image/upload/rockcms/2022-07/family-quotes-2x1-bn-220712-8a4afd.jpg'

# Azure Computer Vision API endpoint
compvisapiEndpoint = f'{ENDPOINT}/vision/v3.2/analyze'

# Headers
headers = {
    'Ocp-Apim-Subscription-Key': KEY,
    'Content-Type': 'application/json'
}

# Parameters
params = {
    'visualFeatures': 'Faces'
}

# Send request to Computer Vision API
response = requests.post(compvisapiEndpoint, params=params, headers=headers, json={'url': imageUrl})

def rescale(image_url, size):
    try:
        # Download image from URL
        response = requests.get(image_url)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Open image from bytes
        img = Image.open(io.BytesIO(response.content))

        # Rescale image
        resized_img = img.resize(size)

        return resized_img

    except Exception as e:
        print(f"Error: {e}")
        return None

# Check if the request was successful
if response.status_code == 200:
    facesdetected = response.json().get('faces', [])
    if not facesdetected:
        print("No faces detected")
    else:
        # Load image using PIL
        image_response = requests.get(imageUrl)
        img = Image.open(io.BytesIO(image_response.content))
        img = img.convert('RGB')

        # Create Pygame window
        screen = pygame.display.set_mode(img.size)
        pygame.display.set_caption("Faces Detected")

        # Convert PIL image to Pygame surface
        img = pygame.image.fromstring(img.tobytes(), img.size, img.mode)

        # Draw bounding boxes around detected faces
        for face in facesdetected:
            face_rectangle = face['faceRectangle']
            left = face_rectangle['left']
            top = face_rectangle['top']
            width = face_rectangle['width']
            height = face_rectangle['height']
            pygame.draw.rect(img, (255, 0, 0), (left, top, width, height), 2)

        # Blit the image with bounding boxes onto the Pygame screen
        screen.blit(img, (0, 0))
        pygame.display.flip()

        # Wait for user to close the window
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
else:
    print("Error:", response.status_code, response.text)

# Quit Pygame
pygame.quit()
