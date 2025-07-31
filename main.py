import pygame
import sys
import random

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

font = pygame.font.SysFont("Arial", 40, bold=True)


# pipe configuration
PIPE_WIDTH = 80
PIPE_GAP = 200  # Gap between top and bottom pipe
PIPE_SPEED = 4
pipe_color = (34, 139, 34)         # Forest Green
pipe_border_color = (0, 100, 0)    # Darker green for border

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

# Game loop
while True:
    # Handle events regardless of game state
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if not game_over:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird_velocity = flap_strength  # Flap up
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
                    pygame.time.set_timer(SPAWN_PIPE_EVENT, 1500)  # Restart pipe spawning

    if not game_over:
        # Apply gravity
        bird_velocity += gravity
        bird_y += bird_velocity

        # Prevent bird from falling below ground
        if bird_y + bird_radius > SCREEN_HEIGHT - ground_height:
            bird_y = SCREEN_HEIGHT - ground_height - bird_radius
            bird_velocity = 0  # Stop falling

        # Prevent bird from going above the screen
        if bird_y - bird_radius < 0:
            bird_y = bird_radius
            bird_velocity = 0

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
                game_over = True
                pygame.time.set_timer(SPAWN_PIPE_EVENT, 0)  # Stop pipe spawning
                break

        # Check collision with ground
        if bird_y + bird_radius >= SCREEN_HEIGHT - ground_height:
            bird_y = SCREEN_HEIGHT - ground_height - bird_radius
            bird_velocity = 0
            game_over = True
            pygame.time.set_timer(SPAWN_PIPE_EVENT, 0)  # Stop pipe spawning

    # Draw everything (both during game and game over)
    screen.fill((135, 206, 235))  # Light blue sky

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
        pygame.draw.rect(screen, pipe_color, (x, 0, PIPE_WIDTH, gap_y - PIPE_GAP//2))
        
        # Bottom pipe
        pygame.draw.rect(screen, pipe_border_color, (x - 4, gap_y + PIPE_GAP//2, PIPE_WIDTH + 8, SCREEN_HEIGHT - ground_height - (gap_y + PIPE_GAP//2)))
        pygame.draw.rect(screen, pipe_color, (x, gap_y + PIPE_GAP//2, PIPE_WIDTH, SCREEN_HEIGHT - ground_height - (gap_y + PIPE_GAP//2)))

    # Draw the bird
    pygame.draw.circle(screen, (255, 255, 0), (bird_x, int(bird_y)), bird_radius)  # Yellow bird
    
    # Draw the ground
    pygame.draw.rect(screen, (222, 184, 135), (0, SCREEN_HEIGHT - ground_height, SCREEN_WIDTH, ground_height))

    # Draw game over message
    if game_over:
        font = pygame.font.Font(None, 74)
        game_over_text = font.render("GAME OVER", True, (255, 0, 0))
        restart_text = font.render("Press SPC-Bar or R to Restart", True, (255, 255, 255))
        
        # Center the text
        screen.blit(game_over_text, (SCREEN_WIDTH//2 - game_over_text.get_width()//2, SCREEN_HEIGHT//2 - 50))
        screen.blit(restart_text, (SCREEN_WIDTH//2 - restart_text.get_width()//2, SCREEN_HEIGHT//2 + 20))


    # Draw score
    score_surface = font.render(f"Score: {score}", True, (0, 0, 0))  # Black text
    screen.blit(score_surface, (20, 20))  # Top-left corner

    # Update screen
    pygame.display.update()
    clock.tick(FPS)