import imageio, pygame

# Initialize pygame
pygame.init()

# Open webcam using imageio
webcam = imageio.get_reader('<video0>', 'ffmpeg')

# Get the size of the webcam image from the first frame of the webcam
webcam_image = webcam.get_data(0)
height, width, other = webcam_image.shape

# Set up pygame window
window = pygame.display.set_mode((width, height))
pygame.display.set_caption('Webcam')

# Loop to constantly update the frames
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    # Get the latest frame from the webcam
    frame = webcam.get_next_data()

    # Convert the frame to a format pygame can use
    frame = pygame.image.frombuffer(frame.tobytes(), (width, height), 'RGB')

    # Display the frame in the pygame window
    window.blit(frame, (0, 0))
    pygame.display.update()

# Quit pygame
pygame.quit()
