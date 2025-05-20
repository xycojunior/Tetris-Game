# menu.py
import pygame
from main import run_game  # agora vai funcionar, pois main não importa mais o menu

def menu():
    screen = pygame.display.set_mode((720, 620))
    pygame.display.set_caption("MENU")
    font = pygame.font.Font(None, 80)
    button_font = pygame.font.Font(None, 40)

    play_button = pygame.Rect(260, 260, 200, 80)
    running = True
    while running:
        screen.fill((30, 30, 30))
        title = font.render("TETRIS UNIFAP", True, (255, 255, 255))
        screen.blit(title, title.get_rect(center=(360, 150)))

        pygame.draw.rect(screen, (255, 255, 255), play_button, border_radius=12)
        play_text = button_font.render("JOGAR", True, (0, 0, 0))
        screen.blit(play_text, play_text.get_rect(center=play_button.center))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.collidepoint(event.pos):
                    return  # Sai do menu e entra no jogo

        pygame.display.update()

if __name__ == "__main__":
    pygame.init()
    while True:
        menu()
        run_game() 