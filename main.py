import pygame, sys
from game import Game
from colors import Colors

pygame.init()

# Fonts and texts
title_font = pygame.font.Font(None, 40)
score_surface = title_font.render("Score", True, Colors.white)
next_surface = title_font.render("Next", True, Colors.white)
game_over_surface = title_font.render("GAME OVER", True, Colors.white)
hold_surface = title_font.render("Hold", True, Colors.white)

# Squares that contain things
score_rect = pygame.Rect(320, 55, 170, 60)
next_rect = pygame.Rect(320, 215, 170, 180)
hold_rect = pygame.Rect(320, 440, 170, 170)

# Sets screen size and window name
screen = pygame.display.set_mode((500, 620))
pygame.display.set_caption("Python Tetris")

# Gives clock the ability to be a clock
clock = pygame.time.Clock()

# Assigns the Game class from game.py to game
game = Game()

# Sets the speed and the time it updates
GAME_UPDATE = pygame.USEREVENT
pygame.time.set_timer(GAME_UPDATE, 500)

paused = False

# Loops the game
while True:
    # Loops to detect events
    for event in pygame.event.get():
        # Detect when window is closed
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        # Gets key inputs
        if event.type == pygame.KEYDOWN:
            # Ends game if it's over
            if game.game_over == True:
                game.game_over = False
                game.reset()
            # Moves the block left one cell
            if paused == False and event.key == pygame.K_LEFT and game.game_over == False:
                game.move_left()
            # Moves the block right one cell
            if paused == False and event.key == pygame.K_RIGHT and game.game_over == False:
                game.move_right()
            # Brings the block down one cell
            if paused == False and event.key == pygame.K_DOWN and game.game_over == False:
                game.move_down()
            # Rotates the block
            if paused == False and event.key == pygame.K_UP and game.game_over == False:
                game.rotate()
                # Moves the block left one cell
            if paused == False and event.key == pygame.K_a and game.game_over == False:
                game.move_left()
            # Moves the block right one cell
            if paused == False and event.key == pygame.K_d and game.game_over == False:
                game.move_right()
            # Brings the block down one cell
            if paused == False and event.key == pygame.K_s and game.game_over == False:
                game.move_down()
            # Rotates the block
            if paused == False and event.key == pygame.K_w and game.game_over == False:
                game.rotate()
            # Drops the block as low as it can go
            if paused == False and event.key == pygame.K_SPACE and game.game_over == False:
                game.hard_drop()
                game.update_score(0, 4)
            # Holds the current block
            if paused == False and event.key == pygame.K_c and game.game_over == False:
                game.hold_block()
            # Pauses and unpauses the game
            if event.key == pygame.K_ESCAPE and game.game_over == False:
                if paused == False:
                    paused = True
                elif paused == True:
                    paused = False
        if paused == False and event.type == GAME_UPDATE and game.game_over == False:
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

    # Updates the display and sets the game at 60fps
    pygame.display.update()
    clock.tick(60)