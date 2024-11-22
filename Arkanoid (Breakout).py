import pygame
import random
import sys
import json
import os

# Inicialização do Pygame
pygame.init()

# Configurações de tela
WIDTH, HEIGHT = 1024, 620
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Arkanoid Game")

# Configurações do jogo
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 149, 221)
DARK_GREEN = (1, 50, 32)
BALL_RADIUS = 12
PADDLE_WIDTH, PADDLE_HEIGHT = 150, 15
BRICK_WIDTH, BRICK_HEIGHT = 60, 20
BRICK_PADDING = 10
BRICK_ROWS, BRICK_COLS = 8, 14
LIVES = 3

# Variáveis do jogo
paddle_x = (WIDTH - PADDLE_WIDTH) // 2
ball_x, ball_y = WIDTH // 2, HEIGHT - 30
ball_dx, ball_dy = 7, -7
score = 0
level = 1
lives = LIVES

# Arquivo para salvar o HighScore
HIGHSCORE_FILE = "highscore.json"

def load_high_score():
    if os.path.exists(HIGHSCORE_FILE):
        with open(HIGHSCORE_FILE, "r") as file:
            data = json.load(file)
            return data.get("high_score", 0)
    return 0

def save_high_score(high_score):
    with open(HIGHSCORE_FILE, "w") as file:
        json.dump({"high_score": high_score}, file)

# Carregar o HighScore inicial
high_score = load_high_score()

# Configuração dos blocos
def create_bricks():
    bricks = []
    colors_points = [
        (WHITE, 10), (BLUE, 25), (pygame.Color('orange'), 50), 
        (GREEN, 75), (pygame.Color('purple'), 100), 
        (pygame.Color('yellow'), 150), (pygame.Color('red'), 200), 
        (pygame.Color('gray'), 300)
    ]
    for row in range(BRICK_ROWS):
        row_bricks = []
        for col in range(BRICK_COLS):
            x = BRICK_PADDING + col * (BRICK_WIDTH + BRICK_PADDING)
            y = BRICK_PADDING + row * (BRICK_HEIGHT + BRICK_PADDING) + 30
            color, points = colors_points[row]
            brick = pygame.Rect(x, y, BRICK_WIDTH, BRICK_HEIGHT)
            row_bricks.append({"rect": brick, "color": color, "points": points, "status": 1})
        bricks.append(row_bricks)
    return bricks

bricks = create_bricks()

# Funções de desenho
def draw_paddle():
    pygame.draw.rect(screen, GREEN, (paddle_x, HEIGHT - PADDLE_HEIGHT, PADDLE_WIDTH, PADDLE_HEIGHT))

def draw_ball():
    pygame.draw.circle(screen, WHITE, (ball_x, ball_y), BALL_RADIUS)

def draw_bricks():
    for row in bricks:
        for brick in row:
            if brick["status"] == 1:
                pygame.draw.rect(screen, brick["color"], brick["rect"])

def draw_text(text, font_size, color, x, y):
    font = pygame.font.Font(None, font_size)
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

# Funções de lógica do jogo
def reset_ball():
    global ball_x, ball_y, ball_dx, ball_dy, paddle_x
    ball_x, ball_y = WIDTH // 2, HEIGHT - 30
    ball_dx, ball_dy = 7, -7
    paddle_x = (WIDTH - PADDLE_WIDTH) // 2

def check_collision():
    global ball_dx, ball_dy, score, high_score, level
    for row in bricks:
        for brick in row:
            if brick["status"] == 1 and brick["rect"].collidepoint(ball_x, ball_y):
                ball_dy = -ball_dy
                brick["status"] = 0
                score += brick["points"]
                if score > high_score:
                    high_score = score
                if all(brick["status"] == 0 for row in bricks for brick in row):
                    level_up()

def level_up():
    global level, bricks
    level += 1
    bricks = create_bricks()
    reset_ball()

# Loop principal
running = True
clock = pygame.time.Clock()
right_pressed = False
left_pressed = False

while running:
    screen.fill(DARK_GREEN)
    
    # Eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                right_pressed = True
            elif event.key == pygame.K_LEFT:
                left_pressed = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                right_pressed = False
            elif event.key == pygame.K_LEFT:
                left_pressed = False

    # Movimento do paddle
    if right_pressed and paddle_x < WIDTH - PADDLE_WIDTH:
        paddle_x += 7
    if left_pressed and paddle_x > 0:
        paddle_x -= 7

    # Movimento da bola
    ball_x += ball_dx
    ball_y += ball_dy

    # Detecção de colisões
    if ball_x + BALL_RADIUS > WIDTH or ball_x - BALL_RADIUS < 0:
        ball_dx = -ball_dx
    if ball_y - BALL_RADIUS < 0:
        ball_dy = -ball_dy
    elif ball_y + BALL_RADIUS > HEIGHT:
        lives -= 1
        if lives == 0:
            running = False
        else:
            reset_ball()

    if (paddle_x < ball_x < paddle_x + PADDLE_WIDTH) and (ball_y + BALL_RADIUS >= HEIGHT - PADDLE_HEIGHT):
        ball_dy = -ball_dy

    check_collision()

    # Desenhar elementos
    draw_paddle()
    draw_ball()
    draw_bricks()
    draw_text(f"Score: {score}", 30, BLUE, 10, 10)
    draw_text(f"High Score: {high_score}", 30, BLUE, WIDTH - 400, 10)
    draw_text(f"Lives: {lives}", 30, BLUE, WIDTH - 100, 10)
    draw_text(f"Level: {level}", 30, BLUE, WIDTH // 3, 10)

    pygame.display.flip()
    clock.tick(60)

# Salvar o HighScore no arquivo ao sair
save_high_score(high_score)

pygame.quit()
sys.exit()
