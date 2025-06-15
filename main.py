import pygame, sys
from game import Game
from colors import Colors

pygame.init()

title_font = pygame.font.Font(None, 40)
score_surface = title_font.render("Score", True, Colors.white)
next_surface = title_font.render("Next", True, Colors.white)
game_over_surface = title_font.render("GAME OVER", True, Colors.white)
hold_surface = title_font.render("Hold", True, Colors.white)

score_rect = pygame.Rect(320, 55, 170, 60)
next_rect = pygame.Rect(320, 215, 170, 180)
hold_rect = pygame.Rect(320, 440, 170, 170)

screen = pygame.display.set_mode((500, 620))
pygame.display.set_caption("Python Tetris")

clock = pygame.time.Clock()

game = Game()

GAME_UPDATE = pygame.USEREVENT
pygame.time.set_timer(GAME_UPDATE, 500)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if game.game_over == True:
                game.game_over = False
                game.reset()
            if event.key == pygame.K_LEFT and game.game_over == False:
                game.move_left()
            if event.key == pygame.K_RIGHT and game.game_over == False:
                game.move_right()
            if event.key == pygame.K_DOWN and game.game_over == False:
                game.move_down()
            if event.key == pygame.K_UP and game.game_over == False:
                game.rotate()
            if event.key == pygame.K_a and game.game_over == False:
                game.move_left()
            if event.key == pygame.K_d and game.game_over == False:
                game.move_right()
            if event.key == pygame.K_s and game.game_over == False:
                game.move_down()
            if event.key == pygame.K_w and game.game_over == False:
                game.rotate()
            if event.key == pygame.K_SPACE and game.game_over == False:
                game.hard_drop()
                game.update_score(0, 4)
            if event.key == pygame.K_c and game.game_over == False:
                game.hold_block()
        if event.type == GAME_UPDATE and game.game_over == False:
            game.move_down()
            if game.lines_cleared_total > 0 and game.lines_cleared_total % 10 == 0:
                new_interval = max(100, 500 - (game.lines_cleared_total // 10) * 50)
                pygame.time.set_timer(GAME_UPDATE, new_interval)
                

    # Drawing
    score_value_surface = title_font.render(str(game.score), True, Colors.white)
    cleared_value_surface = title_font.render(str(game.lines_cleared_total), True, Colors.white)

    screen.fill(Colors.dark_blue)
    screen.blit(score_surface, (365, 20, 50, 50))
    screen.blit(next_surface, (375, 180, 50, 50))
    screen.blit(hold_surface, (375, 410, 50, 50))

    if game.game_over == True:
        screen.blit(game_over_surface, (320, 137.5, 50, 50))
    else:
        if game.lines_cleared_total < 10:
            screen.blit(cleared_value_surface, (397.5, 135, 50, 50))
        elif game.lines_cleared_total >= 10:
            screen.blit(cleared_value_surface, (390, 135, 50, 50))
    pygame.draw.rect(screen, Colors.light_blue, score_rect, 0, 10)
    screen.blit(score_value_surface, score_value_surface.get_rect(centerx = score_rect.centerx, centery = score_rect.centery))
    
    pygame.draw.rect(screen, Colors.light_blue, next_rect, 0, 10)
    pygame.draw.rect(screen, Colors.light_blue, hold_rect, 0, 10)
    game.draw(screen)

    pygame.display.update()
    clock.tick(60)