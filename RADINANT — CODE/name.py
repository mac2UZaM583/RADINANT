import pygame
import sys
import os

pygame.init()

# Установка экрана
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Перезапуск игры")

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Шрифт
font = pygame.font.Font(None, 36)


def game():
    # Логика игры
    pass


def restart_game():
    python = sys.executable
    os.execl(python, python, *sys.argv)


# Основной цикл игры
running = True
while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                restart_game()

    game()

    # Отображение
    text = font.render("Нажмите R для перезапуска игры", True, WHITE)
    text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2))
    screen.blit(text, text_rect)

    pygame.display.flip()

pygame.quit()
sys.exit()
