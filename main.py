# main.py

import pygame, sys
from game import Game       
from colors import Colors 
from ranking import *

def run_game():
    pygame.init()

    # Cria uma fonte para os títulos e textos da interface.
    title_font = pygame.font.Font(None, 40)

    # Pré-renderiza os textos fixos da interface do usuário.
    score_surface = title_font.render("PONTUAÇÃO", True, Colors.white)
    next_surface = title_font.render("PRÓXIMO BLOCO", True, Colors.white)
    game_over_surface = title_font.render("GAME OVER", True, Colors.white)

    # Define os retângulos onde serão mostradas a pontuação e o próximo bloco
    score_rect = pygame.Rect(320, 80, 420, 80)
    next_rect = pygame.Rect(320, 220, 420, 220)

    # Define o tamanho da tela e o título da janela.
    screen = pygame.display.set_mode((720, 620))
    pygame.display.set_caption("TETRIS UNIFAP") 

    # Framerate
    clock = pygame.time.Clock()

    # Instancia o jogo
    game = Game()

    # Cria um evento customizado que dispara a cada 200ms
    GAME_UPDATE = pygame.USEREVENT
    pygame.time.set_timer(GAME_UPDATE, 200)

    while True:
        # Input o jogador
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
                # Botão de acelerar peça
                if event.key == pygame.K_DOWN and not game.game_over:
                    game.move_down()   
                    game.update_score(0, 1)
                # Botão de girar peça
                if event.key == pygame.K_UP and not game.game_over:
                    game.rotate()

            # A cada 200ms move o bloco para baixo, "GRAVIDADE"
            if event.type == GAME_UPDATE and not game.game_over:
                game.move_down()

        # Renderiza a pontuação atual
        score_value_surface = title_font.render(str(game.score), True, 0)
        screen.fill(0)

        # Rendeiza texto de pontuação e próximo bloco
        screen.blit(score_surface, (score_rect.x + 30, score_rect.y - 30))
        screen.blit(next_surface, (next_rect.x + 30, next_rect.y - 30))

        # Verifica se o o player perdeu para chamar a interface
        if game.game_over:
            game_over_screen(screen, game.score) 
            game.reset()                
            continue

        # Renderiza o placar e o próximo bloco
        pygame.draw.rect(screen, Colors.white, score_rect, 0, border_radius=12)
        screen.blit(score_value_surface, score_value_surface.get_rect(
            centerx=score_rect.centerx, centery=score_rect.centery))

        # Desenha o placar e o estado atual do jogo
        pygame.draw.rect(screen, Colors.white, next_rect, 0, border_radius=12)
        game.draw(screen)

        # Atualiza a tela e limita o framerate a 60 FPS
        pygame.display.update()
        clock.tick(60)

def game_over_screen(screen, final_score):
    # Inicializa as fontes para os títulos e textos menores
    pygame.font.init()
    font = pygame.font.Font(None, 60)
    small_font = pygame.font.Font(None, 40)

    # Captura as letras | ativação de input | somente um envio
    initials = ""
    input_active = True
    score_saved = False

    # Controla o cursor piscando no input
    clock = pygame.time.Clock()
    cursor_visible = True
    cursor_timer = 0
    cursor_interval = 500  # ms

    screen_width = screen.get_width()

    while True:
        # Cor de fundo para o clima de game over
        screen.fill(Colors.dark_grey)

        # Título
        title = font.render("GAME OVER", True, Colors.white)
        screen.blit(title, title.get_rect(center=(screen_width // 2, 80)))

        # Score
        score_text = small_font.render(f"Score: {final_score}", True, Colors.white)
        screen.blit(score_text, score_text.get_rect(center=(screen_width // 2, 140)))

        # Faz o underline (_) piscar se ainda não foram digitadas 3 letras
        cursor_timer += clock.get_time()
        if cursor_timer >= cursor_interval:
            cursor_visible = not cursor_visible
            cursor_timer = 0

        # Mostra o input do jogador enquanto ele digita
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
            prompt_text = small_font.render("ESPAÇO: Jogar  |  ESC: Sair", True, Colors.white)
            screen.blit(prompt_text, prompt_text.get_rect(center=(screen_width // 2, 240)))

        # Renderiza o título
        ranking_title = small_font.render("RANKING", True, Colors.white)
        screen.blit(ranking_title, ranking_title.get_rect(center=(screen_width // 2, 300)))

        # Renderiza a o ranking já formatado
        for i, entry in enumerate(get_formatted_ranking()):
            entry_text = small_font.render(entry, True, Colors.white)
            y = 340 + i * 30
            screen.blit(entry_text, entry_text.get_rect(center=(screen_width // 2, y)))

        # Eventos do usuário
        for event in pygame.event.get():
            # Fechar o jogo
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            # Salvar o score
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
            # Reiniciar o jogo
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
