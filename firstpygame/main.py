import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up display
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))           # Helps displays the screen of that width and height
pygame.display.set_caption("My First Pygame")           # Name of Game

# Set up the clock for managing the frame rate
clock = pygame.time.Clock()                      # This line creates an instance of the Clock class.
                                    # The Clock object provides a method called tick which you call once per frame to manage the frame rate.
# Define the character
character = pygame.Rect(375, 275, 50, 50)  # x, y, width, height    # Create the character with 50 width and 50pix height

# Movement speed
speed = 5                         # speed = 5 determines the number of pixels the character moves per frame in any direction (left, right, up, down)

# Main game loop
running = True      # Initializes a flag to control the game loop
while running:
    for event in pygame.event.get():    # Iterates through all the events captured by Pygame.
        if event.type == pygame.QUIT:   # Checks if the user has requested to quit the game.
            running = False             # Stops the game loop if a quit event is detected

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        character.x -= speed
    if keys[pygame.K_RIGHT]:
        character.x += speed
    if keys[pygame.K_UP]:
        character.y -= speed
    if keys[pygame.K_DOWN]:
        character.y += speed

    # Fill the screen with a color (RGB)
    screen.fill((0, 0, 0))  # Black      #Gives background color to the screen

    # Draw the character
    pygame.draw.rect(screen, (255, 0, 0), character)  # Draw red on the rectangle created

    # Update the display
    pygame.display.flip()         # Double buffering is used to minimize flickering and tearing. It ensures that only complete frames are shown on the screen.
                                  # All rendering operations are done on the off-screen buffer and hen the frame is fully rendered, the off-screen buffer is swapped with the on-screen buffer.

    # Cap the frame rate (fps)
    clock.tick(60)             # clock.tick(60) ensures that the game runs at a maximum of 60 frames per second. Like saying hey just use this much of CPU just run at this rate not fast or slow even if the hardware is fast or slow.

# Quit Pygame
pygame.quit()   # This function call un initializes all Pygame modules
sys.exit()     # It ensures that the script exits cleanly, closing the game window and stopping any running processes associated with the game.


