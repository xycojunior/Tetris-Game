# main.py

import pygame, sys
from game import Game       
from colors import Colors 

def run_game():
    pygame.init()

    title_font = pygame.font.Font(None, 40)

    score_surface = title_font.render("PONTUAÇÃO", True, Colors.white)
    next_surface = title_font.render("PRÓXIMO BLOCO", True, Colors.white)
    game_over_surface = title_font.render("GAME OVER", True, Colors.white)

    score_rect = pygame.Rect(320, 80, 420, 80)
    next_rect = pygame.Rect(320, 220, 420, 220)

    screen = pygame.display.set_mode((720, 620))
    pygame.display.set_caption("TETRIS UNIFAP") 

    clock = pygame.time.Clock()
    game = Game()

    GAME_UPDATE = pygame.USEREVENT
    pygame.time.set_timer(GAME_UPDATE, 200)

    while True:
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                pygame.quit() 
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if game.game_over:
                    game.game_over = False  
                    game.reset()            
                if event.key == pygame.K_LEFT and not game.game_over:
                    game.move_left()   
                if event.key == pygame.K_RIGHT and not game.game_over:
                    game.move_right()  
                if event.key == pygame.K_DOWN and not game.game_over:
                    game.move_down()   
                    game.update_score(0, 1)
                if event.key == pygame.K_UP and not game.game_over:
                    game.rotate()

            if event.type == GAME_UPDATE and not game.game_over:
                game.move_down()

        score_value_surface = title_font.render(str(game.score), True, 0)

        screen.fill(0)

        screen.blit(score_surface, (score_rect.x + 30, score_rect.y - 30))
        screen.blit(next_surface, (next_rect.x + 30, next_rect.y - 30))
        if game.game_over:
            game_over_screen(screen, game.score) 
            game.reset()                
            continue

        pygame.draw.rect(screen, Colors.white, score_rect, 0, border_radius=12)
        screen.blit(score_value_surface, score_value_surface.get_rect(
            centerx=score_rect.centerx, centery=score_rect.centery))

        pygame.draw.rect(screen, Colors.white, next_rect, 0, border_radius=12)

        game.draw(screen)
        pygame.display.update()
        clock.tick(60)

from ranking import *

def game_over_screen(screen, final_score):
    pygame.font.init()
    font = pygame.font.Font(None, 60)
    small_font = pygame.font.Font(None, 40)

    initials = ""
    input_active = True
    score_saved = False

    clock = pygame.time.Clock()

    cursor_visible = True
    cursor_timer = 0
    cursor_interval = 500  # ms

    screen_width = screen.get_width()

    while True:
        screen.fill(Colors.dark_grey)

        # Título
        title = font.render("GAME OVER", True, Colors.white)
        screen.blit(title, title.get_rect(center=(screen_width // 2, 80)))

        # Score
        score_text = small_font.render(f"Score: {final_score}", True, Colors.white)
        screen.blit(score_text, score_text.get_rect(center=(screen_width // 2, 140)))

        # Input / Confirmação
        cursor_timer += clock.get_time()
        if cursor_timer >= cursor_interval:
            cursor_visible = not cursor_visible
            cursor_timer = 0

        if input_active:
            display_initials = initials
            if cursor_visible and len(initials) < 3:
                display_initials += "_"
            initials_text = small_font.render(f"Digite 3 letras: {display_initials}", True, Colors.white)
        else:
            initials_text = small_font.render(f"Iniciais salvas: {initials}", True, Colors.green)

        screen.blit(initials_text, initials_text.get_rect(center=(screen_width // 2, 200)))

        # Instruções (só após salvar)
        if not input_active:
            prompt_text = small_font.render("ESPAÇO: Menu  |  ESC: Sair", True, Colors.white)
            screen.blit(prompt_text, prompt_text.get_rect(center=(screen_width // 2, 240)))

        # Ranking Title
        ranking_title = small_font.render("RANKING", True, Colors.white)
        screen.blit(ranking_title, ranking_title.get_rect(center=(screen_width // 2, 300)))

        # Ranking List
        for i, entry in enumerate(get_formatted_ranking()):
            entry_text = small_font.render(entry, True, Colors.white)
            y = 340 + i * 30
            screen.blit(entry_text, entry_text.get_rect(center=(screen_width // 2, y)))

        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if input_active and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and len(initials) == 3:
                    if not score_saved:
                        save_score(initials.upper(), final_score)
                        input_active = False
                        score_saved = True
                elif event.key == pygame.K_BACKSPACE:
                    initials = initials[:-1]
                elif len(initials) < 3 and event.unicode.isalpha():
                    initials += event.unicode.upper()

            if not input_active and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return run_game()
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()

        pygame.display.update()
        clock.tick(30)


if __name__ == "__main__":
    run_game()
