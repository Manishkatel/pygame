import pygame
import random
import math
from pygame import mixer

# Initialize pygame
pygame.init()

# Creating the screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('background.png')

# Background Sound
mixer.music.load('background.wav')
mixer.music.play(-1)  # -1 tells Pygame to play the music in an infinite loop

# Caption and Icon
pygame.display.set_caption("pygame shooter")
icon = pygame.image.load("spaceship.png")  # Loading icon before caption
pygame.display.set_icon(icon)  # Displays the icon

# Player Image and its size
playerImg = pygame.image.load('arcade.png')
playerX = 370
playerY = 480
playerX_change = 0  # Ensures that the player character stops moving horizontally when no movement keys are being pressed

# Enemy
enemyImg = []  # This list will store the images of the enemies in the game.
enemyX = []  # This list will store the x-coordinates of the enemies' positions on the screen.
enemyY = []  # This list will store the y-coordinates of the enemies' positions on the screen.
enemyX_change = []  # This list will store the horizontal movement speed of each enemy.
enemyY_change = []  # This list will store the vertical movement speed of each enemy.
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('monster.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(1.2)
    enemyY_change.append(30)

# Bullets
# Ready - You can't see the bullet on the screen
# Fire - The bullet is currently moving
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

# Score
score_value = 0
font = pygame.font.Font('alienss.ttf', 32)  # Font of score

textX = 10
textY = 10

# GameOver Text
over_font = pygame.font.Font('alienss.ttf', 64)  # Font of game over

def show_score(x, y):
    score = font.render("Score :" + str(score_value), True, (255, 255, 255))  # Render the score text in white color.
    screen.blit(score, (x, y))  # Draw the score on the screen at the specified coordinates

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))  # Render the "GAME OVER" text in white color.
    screen.blit(over_text, (200, 250))  # Draw the "GAME OVER" text at the specified coordinates.

def player(x, y):
    screen.blit(playerImg, (x, y))  # Draw the player image at the given coordinates

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))  # Draw the enemy image at the given coordinates

def fire_bullet(x, y):
    global bullet_state  # Access the global bullet_state variable
    bullet_state = "fire"  # Set the bullet state to "fire"
    screen.blit(bulletImg, (x + 16, y + 10))  # Draw the bullet image at the specified coordinates

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))  # Calculate the distance between the enemy and the bullet
    if distance < 27:  # Check if the distance is less than 27 pixels
        return True  # Return True if there is a collision.
    else:
        return False

running = True
while running:

    screen.fill((0, 0, 0))
    # Background Image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # If keystroke is pressed check whether it's right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.2
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.2
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_Sound = mixer.Sound('laser.wav')
                    bullet_Sound.play()
                    bulletX = playerX
                    fire_bullet(playerX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # Checking the boundary of both the player and enemy during their movement
    playerX += playerX_change  # Updates the player's horizontal position based on playerX_change
    if playerX <= 0:
        playerX = 0  # If the player moves beyond the left or right boundaries of the screen, reset their position to within the boundaries
    elif playerX >= 736:
        playerX = 736

    for i in range(num_of_enemies):

        # Game Over
        if enemyY[i] > 440:  # If any enemy moves below a certain point on the screen (y-coordinate > 440), it triggers the game over condition
            for j in range(num_of_enemies):
                enemyY[j] = 2000  # Moves all enemies off-screen by setting their enemyY to 2000.
            game_over_text()  # Displays the "GAME OVER" text
            break

        enemyX[i] += enemyX_change[i]  # Updates the enemy's horizontal position based on enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 1.2
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -1.2  # If an enemy hits the left or right boundary of the screen, it changes direction and moves down a row.
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)  # Checks if a collision occurred between the enemy and the bullet.
        if collision:
            explosion_Sound = mixer.Sound('explosion.wav')
            explosion_Sound.play()  # Plays the explosion sound
            bulletY = 480
            bullet_state = "ready"  # Reset the bullet position and state
            score_value += 1  # Increase the score by 1
            enemyX[i] = random.randint(0, 735)  # Reset the enemy's position to a new random location at the top of the screen.
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)  # Draws the enemy at its current position.

    # Bullet Movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"  # If the bullet goes off the top of the screen, reset its position and state.
    if bullet_state == "fire":  # If the bullet is in the "fire" state, move it upward and redraw it at its new position.
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()  # pygame.display.update() is more flexible and allows you to update specific portions of the screen efficiently while pygame.display.flip() is simpler and updates the entire display at once
