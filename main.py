import pygame
import sys
import random
import os

# Initialize pygame
pygame.init()

# Constants for screen dimensions
SCREEN_WIDTH = 1020
SCREEN_HEIGHT = 800
ground_height = 100
game_over = False
# Score settings
pipe_count = 0
score = pipe_count
# for playing score sound 
last_score_milestone = 0


font = pygame.font.SysFont("Arial", 40, bold=True)
# initilize the pygame mixer
pygame.mixer.init()


# pipe configuration
PIPE_WIDTH = 80
PIPE_GAP = 200  # Gap between top and bottom pipe
PIPE_SPEED = 4
pipe_border_color = (0, 0, 0)    # Darker green for border

# Create the window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird 🐤")

# Set frame rate
clock = pygame.time.Clock()
FPS = 60

# Bird settings
bird_x = 150
bird_y = SCREEN_HEIGHT // 2
bird_radius = 20
bird_velocity = 0
gravity = 0.3
flap_strength = -6  # Negative means "go up"

# pipes lists
pipes = []  # List of dictionaries, each with 'x', 'gap_y'
SPAWN_PIPE_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_PIPE_EVENT, 1500)  # New pipe every 1.5 sec


# preparing the images for background
day_bg = pygame.image.load("assests/bg-day.png").convert()
day_bg = pygame.transform.scale(day_bg, (1020, 800))

night_bg = pygame.image.load("assests/nt-bg.png").convert()
night_bg = pygame.transform.scale(night_bg, (1020, 800))

# Grounds
g_day = pygame.image.load("assests/g-day.png").convert_alpha()
g_night = pygame.image.load("assests/gn.png").convert_alpha()

# showing heart 
lives = 3
heart_image = pygame.image.load("/media/faisal-chap/Python/p-projects/Flappy Bird/heart.png")  # use a small heart image if available
heart_image = pygame.transform.scale(heart_image, (30, 30))


# loading the bird image
bird_image = pygame.image.load("assests/f-bird.png").convert_alpha()
bird_rect = bird_image.get_rect(center=(200, 300))


# geting the high score
high_score_file = "highscore.txt"
if os.path.exists(high_score_file):
    with open(high_score_file, "r") as f:
        high_score = int(f.read())
else:
    high_score = 0



# load the sounds
flap_sound = pygame.mixer.Sound("assests/wing.wav")
score_sound = pygame.mixer.Sound("assests/point.wav")
hit_sound = pygame.mixer.Sound("assests/hit.wav")
die_sound = pygame.mixer.Sound("assests/die.wav")


# Define the current background
current_bg = day_bg
bg_x = 0

ground_x = 0


# function to rotate the bird image based on velocity
# This function will rotate the bird image based on its velocity
# The bird will rotate upwards when flapping and downwards when falling
def rotate_bird(image, velocity):
    angle = max(-30, min(velocity * -3, 30))  # clamp between -30 and 30 degrees
    return pygame.transform.rotate(image, angle)


# Game loop
while True:

    # Handle events regardless of game state
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Handle space key for jumping
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_velocity = -9  # Jump upward
        
        if not game_over:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird_velocity = flap_strength 
                    flap_sound.play() # Flap up
            if event.type == SPAWN_PIPE_EVENT:
                gap_y = random.randint(150, SCREEN_HEIGHT - ground_height - 150)
                pipes.append({'x': SCREEN_WIDTH, 'gap_y': gap_y})
        else:
            # Allow restart when game is over
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    # Reset game
                    game_over = False
                    bird_y = SCREEN_HEIGHT // 2
                    bird_velocity = 0
                    pipes = []
                    pipe_count = 0
                    lives = 3  # Reset lives
                    score = 0
                    pygame.time.set_timer(SPAWN_PIPE_EVENT, 1500)  # Restart pipe spawning
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Reset game
                    game_over = False
                    bird_y = SCREEN_HEIGHT // 2
                    bird_velocity = 0
                    pipes = []
                    pipe_count = 0
                    score = 0
                    lives = 3  # Reset lives
                    pygame.time.set_timer(SPAWN_PIPE_EVENT, 1500)  # Restart pipe spawning

    # Check the score to change background and ground
    if score < 1500 or  (score >= 2500 and score < 4000):
        current_bg = day_bg
        current_ground = g_day
    else:
        current_bg = night_bg
        current_ground = g_night



    if not game_over:
        # Apply gravity
        bird_velocity += gravity
        bird_y += bird_velocity


        # Play score sound at every 100 points (once per milestone)
        if score >= last_score_milestone + 100:
            score_sound.play()
            last_score_milestone += 100

        # Prevent bird from falling below ground
        if bird_y + bird_radius > SCREEN_HEIGHT - ground_height:
            bird_y = SCREEN_HEIGHT - ground_height - bird_radius
            bird_velocity = 0  # Stop falling

        # Prevent bird from going above the screen
        if bird_y - bird_radius < 0:
            bird_y = bird_radius
            bird_velocity = 0


        # saving the high score        if score > high_score:
        if score > high_score:
            high_score = score
            with open(high_score_file, "w") as f:
                f.write(str(high_score))


        # Move pipes
        for pipe in pipes:
            pipe['x'] -= PIPE_SPEED

        # Remove pipes that go off screen
        pipes = [pipe for pipe in pipes if pipe['x'] + PIPE_WIDTH > 0]

        # Create bird collision rect (UPDATED EACH FRAME)
        bird_rect = pygame.Rect(bird_x - bird_radius, int(bird_y - bird_radius), bird_radius * 2, bird_radius * 2)

        # Check collisions with pipes
        for pipe in pipes:
            x = pipe['x']
            gap_y = pipe['gap_y']

            top_pipe_rect = pygame.Rect(x, 0, PIPE_WIDTH, gap_y - PIPE_GAP // 2)
            bottom_pipe_rect = pygame.Rect(x, gap_y + PIPE_GAP // 2, PIPE_WIDTH, SCREEN_HEIGHT - ground_height - (gap_y + PIPE_GAP // 2))

            if bird_rect.colliderect(top_pipe_rect) or bird_rect.colliderect(bottom_pipe_rect):
                hit_sound.play()
                game_over = True
                die_sound.play()
                pygame.time.set_timer(SPAWN_PIPE_EVENT, 0)  # Stop pipe spawning
                break

        # Check collision with ground
        if bird_y + bird_radius >= SCREEN_HEIGHT - ground_height:
            bird_y = SCREEN_HEIGHT - ground_height - bird_radius
            bird_velocity = 0
            hit_sound.play()
            game_over = True
            die_sound.play()
            pygame.time.set_timer(SPAWN_PIPE_EVENT, 0)  # Stop pipe spawning

    # Draw everything (both during game and game over)
    screen.fill((135, 206, 235))  # Light blue sky
    # Draw current background
    bg_x -= 1
    if bg_x <= -1020:
        bg_x = 0

    # Draw both images side-by-side for seamless scroll
    screen.blit(current_bg, (bg_x, 0))
    screen.blit(current_bg, (bg_x + 1020, 0))


    # dynamic color for pipes based on score
    if score < 1500 or  (score >= 2500 and score < 4000):
        current_pipe_color = (90, 0, 120)  # Day pipe
    else:
        current_pipe_color = (25, 25, 112)  # Night pipe

    # Draw pipes
    for pipe in pipes:
        # Score logic: give 2 points when bird crosses the center of a pipe
        if not pipe.get('scored') and pipe['x'] + PIPE_WIDTH < bird_x:
            pipe_count += 1  # Keep track of pipes passed
            score += pipe_count
            pipe['scored'] = True



        # Draw the pipes
        x = pipe['x']
        gap_y = pipe['gap_y']
        # Top pipe
        pygame.draw.rect(screen, pipe_border_color, (x - 4, 0, PIPE_WIDTH + 8, gap_y - PIPE_GAP//2))
        pygame.draw.rect(screen, current_pipe_color, (x, 0, PIPE_WIDTH, gap_y - PIPE_GAP//2))
        
        # Bottom pipe
        pygame.draw.rect(screen, pipe_border_color, (x - 4, gap_y + PIPE_GAP//2, PIPE_WIDTH + 8, SCREEN_HEIGHT - ground_height - (gap_y + PIPE_GAP//2)))
        pygame.draw.rect(screen, current_pipe_color, (x, gap_y + PIPE_GAP//2, PIPE_WIDTH, SCREEN_HEIGHT - ground_height - (gap_y + PIPE_GAP//2)))

    # Draw the bird
    rotated_bird = rotate_bird(bird_image, bird_velocity)
    rotated_rect = rotated_bird.get_rect(center=(bird_rect.centerx, bird_y))
    screen.blit(rotated_bird, rotated_rect)

    # # Draw the ground
    # pygame.draw.rect(screen, (222, 184, 135), (0, SCREEN_HEIGHT - ground_height, SCREEN_WIDTH, ground_height))
    ground_y = SCREEN_HEIGHT - 100  # Position it exactly at bottom

    # Scroll ground
    if not game_over:
        ground_x -= 3
        if ground_x <= -1020:
            ground_x = 0


    # Draw scrolling ground image
    screen.blit(current_ground, (ground_x, ground_y))
    screen.blit(current_ground, (ground_x + 1020, ground_y))

    # Draw game over message
    if game_over:


        lives -= 1
        if lives > 0:
            game_over = False
            bird_y = SCREEN_HEIGHT // 2
            bird_velocity = 0
            pipes = []
            pipe_count = 0

            pygame.time.set_timer(SPAWN_PIPE_EVENT, 1500)
        else:
            pygame.time.set_timer(SPAWN_PIPE_EVENT, 0)  # stop pipe spawn

            font = pygame.font.Font(None, 74)
            game_over_text = font.render("GAME OVER", True, (255, 0, 0))
            restart_text = font.render("Press SPC-Bar or R to Restart", True, (255, 255, 255))
            
            # Center the text
            screen.blit(game_over_text, (SCREEN_WIDTH//2 - game_over_text.get_width()//2, SCREEN_HEIGHT//2 - 50))
            screen.blit(restart_text, (SCREEN_WIDTH//2 - restart_text.get_width()//2, SCREEN_HEIGHT//2 + 20))


    # Draw high score
    font_hs = pygame.font.Font(None, 36)
    high_score_surface = font_hs.render(f"High Score: {high_score}", True, (255, 215, 0))
    screen.blit(high_score_surface, (20, 70))






    # Draw lives
    for i in range(lives):
        screen.blit(heart_image, (SCREEN_WIDTH - 40 - i * 35, 20))
    # Draw score
    score_surface = font.render(f"Score: {score}", True, (255, 255, 255))  # Black text
    screen.blit(score_surface, (20, 20))  # Top-left corner

    # Update screen
    pygame.display.update()
    clock.tick(FPS)