import pygame
import sys
import random

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 160
BALL_RADIUS = 10
BALL_SPEED = 4.5
DELAY_TIME = 100
FONT_SIZE = 50
WHITE = pygame.Color("white")
RED = (255, 0, 0)
GREEN = (0, 255, 50)
DARK_PURPLE_SHADE = (75, 0, 130)
AI_SPEED = 3
PLAYER_SPEED = 2


def init_game():
    """Initialize game components."""
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    fps = pygame.time.Clock()
    
    p1 = pygame.Rect(0, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
    p2 = pygame.Rect(SCREEN_WIDTH - PADDLE_WIDTH, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
    cpu = pygame.Rect(0, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
    ball = pygame.Rect(0, 0, BALL_RADIUS * 2, BALL_RADIUS * 2)
    
    p1_score, p2_score = 0, 0
    font = pygame.font.Font(None, FONT_SIZE)
    return screen, fps, p1, p2, cpu, ball, p1_score, p2_score, font


def handle_input(p1, p2):
    """Handle input for player movement."""
    keys_pressed = pygame.key.get_pressed()
    
    if keys_pressed[pygame.K_w] and p1.top > 0:
        p1.top -= PLAYER_SPEED
    if keys_pressed[pygame.K_s] and p1.bottom < SCREEN_HEIGHT:
        p1.bottom += PLAYER_SPEED
    
    if keys_pressed[pygame.K_UP] and p2.top > 0:
        p2.top -= 2
    if keys_pressed[pygame.K_DOWN] and p2.bottom < SCREEN_HEIGHT:
        p2.bottom += 2

def cpu_ai(cpu, ball):
    """Basic AI for CPU to follow the ball on the left side."""
    if cpu.centery < ball.centery and cpu.bottom < SCREEN_HEIGHT:
        cpu.top += AI_SPEED
    elif cpu.centery > ball.centery and cpu.top > 0:
        cpu.top -= AI_SPEED


def update_ball(ball, ball_vel_x, ball_vel_y, p1, p2, cpu, p1_score, p2_score, is_human):
    """Update the ball's position and handle collisions."""
    ball.x += ball_vel_x
    ball.y += ball_vel_y
    
    # Ball hitting top or bottom
    if ball.y >= SCREEN_HEIGHT - BALL_RADIUS:
        ball_vel_y = -BALL_SPEED
    if ball.y <= 0:
        ball_vel_y = BALL_SPEED
    # Ball out of bounds (score points)
    if ball.x <= 0 - 2 * BALL_RADIUS:
        p2_score += 1
        ball.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        ball_vel_x = random.choice([BALL_SPEED, -BALL_SPEED])
        ball_vel_y = random.choice([BALL_SPEED, -BALL_SPEED])
    
    if ball.x >= SCREEN_WIDTH + 2 * BALL_RADIUS:
        p1_score += 1
        ball.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        ball_vel_x = random.choice([BALL_SPEED, -BALL_SPEED])
        ball_vel_y = random.choice([BALL_SPEED, -BALL_SPEED])
    
    # Ball hitting paddles (collisions)
    if ball.colliderect(p2):
        ball_vel_x = -BALL_SPEED
    if ball.colliderect(p1) and is_human:
        ball_vel_x = BALL_SPEED
    if ball.colliderect(cpu) and is_human == False:
        ball_vel_x = BALL_SPEED
    
    return ball, ball_vel_x, ball_vel_y, p1_score, p2_score

def draw_text(screen,text, font, text_col, x, y):
  """Draw button menue on the screen."""
  img = font.render(text, True, text_col)
  screen.blit(img, (x, y))

def draw(screen, p1, p2, cpu, ball, p1_score, p2_score, font, is_human):
    """Draw all elements on the screen."""
    
    # Display scores
    player_score_text = font.render(str(p1_score), True, WHITE)
    opponent_score_text = font.render(str(p2_score), True, WHITE)
    colon_text = font.render(":", True, WHITE)
    
    screen.blit(player_score_text, (SCREEN_WIDTH // 2 - 50, 50))
    screen.blit(opponent_score_text, (SCREEN_WIDTH // 2 + 50, 50))
    screen.blit(colon_text, (SCREEN_WIDTH // 2, 50))
    
    # Draw paddles and ball
    if is_human:
        pygame.draw.rect(screen, WHITE, p1)
        pygame.draw.rect(screen, WHITE, p2)
    else:
        pygame.draw.rect(screen, WHITE, p2)
        pygame.draw.rect(screen, WHITE, cpu)
    pygame.draw.circle(screen, WHITE, ball.center, BALL_RADIUS)
    
    pygame.display.update()


def The_result(p1_score, p2_score):
     aim = 2
     p2_win = None
     if p2_score == aim:
        p2_win = True
     if p1_score == aim:
         p2_win = False
     return p2_win


def main():
    """Main game loop."""
    screen, fps, p1, p2, cpu, ball, p1_score, p2_score, font = init_game()

    color = WHITE
    r_color = RED
    g_color = GREEN
    pr_color = DARK_PURPLE_SHADE
    B_font = pygame.font.Font(None, 100)
    ball_vel_x = BALL_SPEED
    ball_vel_y = BALL_SPEED
    
    """just to see what the user choice"""   
    is_human = None
    while is_human is None:
        screen.fill("black")
        draw_text(screen, "Press C to play against Computer", font, color, SCREEN_WIDTH/4.5, SCREEN_HEIGHT//2 + 0)
        draw_text(screen, "Press P to play against Human Player", font, color, SCREEN_WIDTH/5.25, SCREEN_HEIGHT//2 + 50)
        draw_text(screen, "PONG GAME", B_font, pr_color, SCREEN_WIDTH/3.6, SCREEN_HEIGHT//2 -100)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    is_human = False
                elif event.key == pygame.K_p:
                    is_human = True
    
    running = True
    while running:
        screen.fill("black")
        if The_result(p1_score, p2_score):
            screen.fill("black")
            draw_text(screen, "Congratulations", font, g_color, SCREEN_WIDTH/2.7, SCREEN_HEIGHT//2)
            draw_text(screen, "Player1 Win!", font, color, SCREEN_WIDTH/2.5, SCREEN_HEIGHT//2 - 50)
            ball_vel_x = 0
            ball_vel_x = 0
        elif The_result(p1_score, p2_score) == False and is_human:
            screen.fill("black")
            draw_text(screen, "Congratulations", font, g_color, SCREEN_WIDTH/2.7, SCREEN_HEIGHT//2)
            draw_text(screen, "Player2 Win!", font, color, SCREEN_WIDTH/2.5, SCREEN_HEIGHT//2 - 50)
            ball_vel_x = 0
            ball_vel_x = 0
        elif The_result(p1_score, p2_score) == False and is_human == False:
            screen.fill("black")
            draw_text(screen, "Game Over", font, r_color, SCREEN_WIDTH/2.5, SCREEN_HEIGHT//2 - 50)
            draw_text(screen, "Ai win He will take over the world!", font, color, SCREEN_WIDTH/4.5, SCREEN_HEIGHT//2 )
            ball_vel_x = 0
            ball_vel_x = 0

        handle_input(p1, p2)
        cpu_ai(cpu, ball)
        ball, ball_vel_x, ball_vel_y, p1_score, p2_score = update_ball(
            ball, ball_vel_x, ball_vel_y, p1, p2, cpu, p1_score, p2_score,
            is_human)
        draw(screen, p1, p2, cpu, ball, p1_score, p2_score, font, is_human)

        pygame.display.update()
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        fps.tick(DELAY_TIME)
    
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
