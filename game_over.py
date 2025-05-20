# game_over.py
import pygame
import sys
from colors import Colors

def game_over_screen(score):
    pygame.init()
    screen = pygame.display.set_mode((720, 620))
    pygame.display.set_caption("GAME OVER")

    font_big = pygame.font.Font(None, 80)
    font_small = pygame.font.Font(None, 40)

    game_over_text = font_big.render("GAME OVER", True, Colors.white)
    score_text = font_small.render(f"PONTUAÇÃO: {score}", True, Colors.white)
    prompt_text = font_small.render("ESC: Sair", True, Colors.white)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        screen.fill(Colors.dark_grey)
        screen.blit(game_over_text, game_over_text.get_rect(center=(360, 200)))
        screen.blit(score_text, score_text.get_rect(center=(360, 300)))
        screen.blit(prompt_text, prompt_text.get_rect(center=(360, 400)))

        pygame.display.update()
