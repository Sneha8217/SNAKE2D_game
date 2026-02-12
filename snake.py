import pygame
import random
import sys

pygame.init()

WIDTH = 600
HEIGHT = 600
BLOCK = 20

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game - Stylish Edition")

clock = pygame.time.Clock()

# 🎨 Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 50, 50)
BLUE = (50, 150, 255)
PURPLE = (170, 0, 255)
YELLOW = (255, 200, 0)

font = pygame.font.SysFont("Arial", 35, bold=True)
big_font = pygame.font.SysFont("Arial", 55, bold=True)

# 🐍 Load Snake Image
snake_img = pygame.image.load("snake.png").convert_alpha()
snake_img = pygame.transform.scale(snake_img, (BLOCK, BLOCK))


def reset_game():
    global snake, snake_dir, food, score
    snake = [(100, 100)]
    snake_dir = (BLOCK, 0)
    food = (
        random.randrange(0, WIDTH, BLOCK),
        random.randrange(0, HEIGHT, BLOCK)
    )
    score = 0


# 🌈 Gradient Background
def draw_background():
    for y in range(HEIGHT):
        color = (20, 20 + y // 4, 40 + y // 6)
        pygame.draw.line(screen, color, (0, y), (WIDTH, y))

    # Grid lines
    for x in range(0, WIDTH, BLOCK):
        pygame.draw.line(screen, (40, 40, 60), (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, BLOCK):
        pygame.draw.line(screen, (40, 40, 60), (0, y), (WIDTH, y))


def draw_snake():
    for i, segment in enumerate(snake):
        if i == 0:
            # Rotate head
            if snake_dir == (BLOCK, 0):
                rotated = pygame.transform.rotate(snake_img, 0)
            elif snake_dir == (-BLOCK, 0):
                rotated = pygame.transform.rotate(snake_img, 180)
            elif snake_dir == (0, -BLOCK):
                rotated = pygame.transform.rotate(snake_img, 90)
            else:
                rotated = pygame.transform.rotate(snake_img, -90)

            screen.blit(rotated, segment)
        else:
            # 🌈 Color changing body
            color = (
                (i * 15) % 255,
                (150 + i * 10) % 255,
                (255 - i * 20) % 255
            )
            pygame.draw.rect(screen, color, (*segment, BLOCK, BLOCK), border_radius=6)


def draw_food():
    # Glow effect
    pygame.draw.circle(
        screen,
        YELLOW,
        (food[0] + BLOCK // 2, food[1] + BLOCK // 2),
        BLOCK // 2 + 4,
    )
    pygame.draw.circle(
        screen,
        RED,
        (food[0] + BLOCK // 2, food[1] + BLOCK // 2),
        BLOCK // 2,
    )


def show_score():
    shadow = font.render(f"Score: {score}", True, BLACK)
    text = font.render(f"Score: {score}", True, WHITE)

    screen.blit(shadow, (WIDTH // 2 - 80 + 2, 12))
    screen.blit(text, (WIDTH // 2 - 80, 10))


def game_over_screen():
    screen.fill((15, 0, 30))

    over_text = big_font.render("GAME OVER", True, PURPLE)
    score_text = font.render(f"Final Score: {score}", True, WHITE)
    restart_text = font.render("Press R to Restart", True, YELLOW)

    screen.blit(over_text, over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 60)))
    screen.blit(score_text, score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
    screen.blit(restart_text, restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 60)))

    pygame.display.update()


reset_game()
game_over = False
running = True

while running:

    if not game_over:
        clock.tick(10 + score)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake_dir != (0, BLOCK):
                    snake_dir = (0, -BLOCK)
                if event.key == pygame.K_DOWN and snake_dir != (0, -BLOCK):
                    snake_dir = (0, BLOCK)
                if event.key == pygame.K_LEFT and snake_dir != (BLOCK, 0):
                    snake_dir = (-BLOCK, 0)
                if event.key == pygame.K_RIGHT and snake_dir != (-BLOCK, 0):
                    snake_dir = (BLOCK, 0)

        head_x = snake[0][0] + snake_dir[0]
        head_y = snake[0][1] + snake_dir[1]
        new_head = (head_x, head_y)

        if head_x < 0 or head_x >= WIDTH or head_y < 0 or head_y >= HEIGHT:
            game_over = True

        if new_head in snake:
            game_over = True

        if not game_over:
            snake.insert(0, new_head)

            if new_head == food:
                score += 1
                food = (
                    random.randrange(0, WIDTH, BLOCK),
                    random.randrange(0, HEIGHT, BLOCK)
                )
            else:
                snake.pop()

        draw_background()
        draw_snake()
        draw_food()
        show_score()
        pygame.display.update()

    else:
        game_over_screen()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    reset_game()
                    game_over = False

pygame.quit()
