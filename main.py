# main.py

import pygame, sys
from game import Game       
from colors import Colors  
from game_over import game_over_screen

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
            game_over_screen(game.score) 
            game.reset()                
            continue

        pygame.draw.rect(screen, Colors.white, score_rect, 0, border_radius=12)
        screen.blit(score_value_surface, score_value_surface.get_rect(
            centerx=score_rect.centerx, centery=score_rect.centery))

        pygame.draw.rect(screen, Colors.white, next_rect, 0, border_radius=12)

        game.draw(screen)
        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    run_game()
