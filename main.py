import pygame, sys
from game import Game       
from colors import Colors   

pygame.init()

title_font = pygame.font.Font(None, 40)

# Cria superfícies de texto para os títulos e mensagens do jogo
score_surface = title_font.render("PONTUAÇÃO", True, Colors.white)
next_surface = title_font.render("PRÓXIMO BLOCO", True, Colors.white)
game_over_surface = title_font.render("GAME OVER", True, Colors.white)

# Cria retângulos que servirão como caixas de exibição (score e próximo bloco)
score_rect = pygame.Rect(320, 80, 420, 80)      # Caixa da pontuação
next_rect = pygame.Rect(320, 220, 420, 220)     # Caixa do próximo bloco


screen = pygame.display.set_mode((720, 620))
pygame.display.set_caption("TETRIS UNIFAP") 

clock = pygame.time.Clock()

game = Game()

GAME_UPDATE = pygame.USEREVENT
pygame.time.set_timer(GAME_UPDATE, 200)  # Atualiza a queda das peças

while True:
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            pygame.quit() 
            sys.exit()
        
        if event.type == pygame.KEYDOWN:  
            if game.game_over:  # 
                game.game_over = False  
                game.reset()            

            # Controles do jogador (movimentações)
            if event.key == pygame.K_LEFT and not game.game_over:
                game.move_left()   
            if event.key == pygame.K_RIGHT and not game.game_over:
                game.move_right()  
            if event.key == pygame.K_DOWN and not game.game_over:
                game.move_down()   
                game.update_score(0, 1)  # Adiciona 1 ponto pela descida manual
            if event.key == pygame.K_UP and not game.game_over:
                game.rotate()      # Rotaciona a peça

        # Evento automático de queda da peça a cada 200ms
        if event.type == GAME_UPDATE and not game.game_over:
            game.move_down()

    # RENDERIZAÇÃO DOS ELEMENTOS NA TELA

    # Texto da pontuação atual
    score_value_surface = title_font.render(str(game.score), True, 000000)

    screen.fill(0000)

    # Desenha os títulos acima das caixas
    screen.blit(score_surface, (score_rect.x + 30, score_rect.y - 30))
    screen.blit(next_surface, (next_rect.x + 30, next_rect.y - 30))

    # Exibe "GAME OVER" se o jogo estiver encerrado
    if game.game_over:
        screen.blit(game_over_surface, (320, 470, 50, 50))

    # Desenha a caixa da pontuação com cantos arredondados
    pygame.draw.rect(screen, Colors.white, score_rect, 0, border_radius=12)
    screen.blit(score_value_surface, score_value_surface.get_rect(
        centerx=score_rect.centerx, centery=score_rect.centery))

    # Desenha a caixa do próximo bloco com cantos arredondados
    pygame.draw.rect(screen, Colors.white, next_rect, 0, border_radius=12)

    # Chama o método da classe Game que desenha o tabuleiro e blocos
    game.draw(screen)

    # Atualiza a tela com o novo frame
    pygame.display.update()

    # Controla para que o loop rode a no máximo 60 frames por segundo
    clock.tick(60)
