import pygame
import random

pygame.init()
pygame.mixer.init()

info = pygame.display.Info()
WIDTH = info.current_w
HEIGHT = info.current_h

screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Square Clicker")

BASE_WIDTH = 1366
scale = WIDTH / BASE_WIDTH

SQUARE_SIZE = max(30, int(50 * scale))
square_color = (255, 0, 0)

FONT_SIZE = max(20, int(30 * scale))
BIG_FONT_SIZE = max(40, int(80 * scale))
font = pygame.font.SysFont("Arial", FONT_SIZE)
big_font = pygame.font.SysFont("Arial", BIG_FONT_SIZE)

try:
    bg_image = pygame.image.load('background.png')
    bg_rect = bg_image.get_rect()
    scale_bg = max(WIDTH / bg_rect.width, HEIGHT / bg_rect.height)
    new_size = (int(bg_rect.width * scale_bg), int(bg_rect.height * scale_bg))
    bg_image = pygame.transform.smoothscale(bg_image, new_size)
    bg_x = (WIDTH - new_size[0]) // 2
    bg_y = (HEIGHT - new_size[1]) // 2
    pygame.mixer.music.load('music.mp3')
    music_loaded = True
except:
    print("Файлы не найдены! Используем стандартный фон.")
    bg_image = None
    music_loaded = False

def reset_game():
    global score, start_ticks, game_active, square_rect
    score = 0
    start_ticks = pygame.time.get_ticks()
    game_active = True
    square_rect = pygame.Rect(random.randint(0, WIDTH - SQUARE_SIZE),
                              random.randint(0, HEIGHT - SQUARE_SIZE),
                              SQUARE_SIZE, SQUARE_SIZE)
    if music_loaded:
        pygame.mixer.music.stop()
        pygame.mixer.music.play(-1)

square_rect = pygame.Rect(random.randint(0, WIDTH - SQUARE_SIZE),
                          random.randint(0, HEIGHT - SQUARE_SIZE),
                          SQUARE_SIZE, SQUARE_SIZE)
score = 0
GAME_DURATION = 20
start_ticks = pygame.time.get_ticks()
game_active = True

if music_loaded:
    pygame.mixer.music.play(-1)

running = True
while running:
    if game_active:
        elapsed_seconds = (pygame.time.get_ticks() - start_ticks) // 1000
        time_left = max(0, GAME_DURATION - elapsed_seconds)
        if time_left <= 0:
            game_active = False

    if bg_image:
        screen.blit(bg_image, (bg_x, bg_y))
    else:
        screen.fill((20, 20, 20))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if game_active:
                if square_rect.collidepoint(event.pos):
                    score += 1
                    square_rect.x = random.randint(0, WIDTH - SQUARE_SIZE)
                    square_rect.y = random.randint(0, HEIGHT - SQUARE_SIZE)
            else:
                reset_game()

    pygame.draw.rect(screen, square_color, square_rect)

    score_txt = font.render(f"Счёт: {score}", True, (253, 255, 255))
    screen.blit(score_txt, (10, 10))

    timer_color = (255, 2, 200) if game_active else (255, 0, 0)
    timer_text = font.render(f"Время: {time_left if game_active else 0}", True, timer_color)
    
    timer_x = WIDTH - timer_text.get_width() - 10
    screen.blit(timer_text, (timer_x, 10))

    if not game_active:
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        final_score_text = big_font.render(f"{score}", True, (255, 255, 0))
        text_rect = final_score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(final_score_text, text_rect)

        label_text = font.render("ОЧКИ", True, (255, 255, 255))
        label_rect = label_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 60))
        screen.blit(label_text, label_rect)

    pygame.display.flip()

pygame.quit()