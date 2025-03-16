import random
import pygame

pygame.init()

# Screen dimensions
width, height = 600, 600
game_screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Munna Snake Game")

# Snake initial position and movement
snake_x, snake_y = width // 2, height // 2
change_x, change_y = 10, 0
snake_body = [(snake_x, snake_y)]
score = 0
high_score = 0
speed = 10  # Initial speed

# Game mode
walls_mode = True  # If True, hitting walls ends the game

# Colors
WHITE = (255, 255, 255)
GRAY = (150, 150, 150)
YELLOW = (255, 255, 102)
BLUE = (0, 0, 128)
GOLD = (255, 215, 0)
RED = (255, 0, 0)

# Font
font = pygame.font.Font(None, 36)

# Load sound effects
food_sound = pygame.mixer.Sound("foodwav.mp3")  # Eating food sound
game_over_sound = pygame.mixer.Sound("game_overwav.mp3")  # Game over sound

# Generate food at a valid position
def generate_food():
    while True:
        food_x = random.randrange(0, width, 10)
        food_y = random.randrange(0, height, 10)
        if (food_x, food_y) not in snake_body:
            return food_x, food_y, random.choice(["normal", "golden"])

food_x, food_y, food_type = generate_food()

# Clock for controlling FPS
clock = pygame.time.Clock()
running = True
game_over = False

# Function to display snake, food, and score
def display_snake_and_food():
    global snake_x, snake_y, food_x, food_y, food_type, score, high_score, speed

    # Move the snake
    if walls_mode:
        if snake_x + change_x >= width or snake_x + change_x < 0 or snake_y + change_y >= height or snake_y + change_y < 0:
            game_over_screen("Hit the Wall!")
            return
    else:
        snake_x = (snake_x + change_x) % width
        snake_y = (snake_y + change_y) % height

    # Check for self-collision
    if (snake_x, snake_y) in snake_body[1:]:
        game_over_screen("Collided with Self!")
        return

    # Add new position to snake's body
    snake_body.append((snake_x, snake_y))

    # Check if the snake eats the food
    if (food_x, food_y) == (snake_x, snake_y):
        pygame.mixer.Sound.play(food_sound)
        if food_type == "golden":
            score += 5
        else:
            score += 1
        
        # Increase speed every 5 points
        if score % 5 == 0:
            speed += 1
        
        food_x, food_y, food_type = generate_food()
    else:
        del snake_body[0]  # Remove tail segment

    # Update high score
    if score > high_score:
        high_score = score

    # Draw background
    game_screen.fill(GRAY)

    # Draw food
    if food_type == "golden":
        pygame.draw.circle(game_screen, GOLD, (food_x, food_y), 6)
    else:
        pygame.draw.circle(game_screen, BLUE, (food_x, food_y), 6)

    # Draw snake
    for (x, y) in snake_body:
        pygame.draw.circle(game_screen, YELLOW, (x, y), 6)

    # Display score and high score
    score_text = font.render(f"Score: {score}", True, WHITE)
    high_score_text = font.render(f"High Score: {high_score}", True, WHITE)
    mode_text = font.render(f"Walls Mode: {'ON' if walls_mode else 'OFF'}", True, RED)
    game_screen.blit(score_text, (10, 10))
    game_screen.blit(high_score_text, (10, 40))
    game_screen.blit(mode_text, (10, 70))

    pygame.display.update()

# Function to display game over screen
def game_over_screen(reason):
    global game_over
    game_over = True
    pygame.mixer.Sound.play(game_over_sound)

    game_screen.fill((0, 0, 0))
    text = font.render(f"GAME OVER! {reason}", True, RED)
    restart_text = font.render("Press R to Restart", True, WHITE)
    exit_text = font.render("Press Q to Quit", True, WHITE)
    
    game_screen.blit(text, (width // 2 - 150, height // 2 - 50))
    game_screen.blit(restart_text, (width // 2 - 100, height // 2))
    game_screen.blit(exit_text, (width // 2 - 100, height // 2 + 40))

    pygame.display.update()

# Main game loop
while running:
    if game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Restart
                    snake_x, snake_y = width // 2, height // 2
                    change_x, change_y = 10, 0
                    snake_body = [(snake_x, snake_y)]
                    score = 0
                    speed = 10
                    food_x, food_y, food_type = generate_food()
                    game_over = False
                if event.key == pygame.K_q:  # Quit
                    running = False
    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and change_x == 0:
                    change_x = -10
                    change_y = 0
                elif event.key == pygame.K_RIGHT and change_x == 0:
                    change_x = 10
                    change_y = 0
                elif event.key == pygame.K_UP and change_y == 0:
                    change_x = 0
                    change_y = -10
                elif event.key == pygame.K_DOWN and change_y == 0:
                    change_x = 0
                    change_y = 10
                elif event.key == pygame.K_w:  # Toggle walls mode
                    walls_mode = not walls_mode

        # Update game state
        display_snake_and_food()
        clock.tick(speed)

pygame.quit()
