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

# Timing for delay and saving when you last moved
move_delay = 95
last_move_time = 0

# Loops the game
while True:
    # Gets the current time of the run time
    current_time = pygame.time.get_ticks()
    keys = pygame.key.get_pressed()
    # Only does the if statement if the game isn't paused or the game isn't over
    if paused == False and game.game_over == False:
        # Detects if it is any of these keys and if the last time you moved wasn't below the move delay
        if (keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_DOWN] or keys[pygame.K_a] or keys[pygame.K_d] or keys[pygame.K_s]) and (current_time - last_move_time > move_delay):
            # Moves the block left one cell
            if keys[pygame.K_LEFT]:
                game.move_left()
            # Moves the block right one cell
            if keys[pygame.K_RIGHT]:
                game.move_right()
            # Brings the block down one cell
            if keys[pygame.K_DOWN]:
                game.move_down()
            last_move_time = current_time
            # Moves the block left one cell
            if keys[pygame.K_a]:
                game.move_left()
            # Moves the block right one cell
            if keys[pygame.K_d]:
                game.move_right()
            # Brings the block down one cell
            if keys[pygame.K_s]:
                game.move_down()
            last_move_time = current_time

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
            # Rotates the block
            if paused == False and event.key == pygame.K_UP and game.game_over == False:
                game.rotate()
            # Rotates the block clockwise
            if paused == False and event.key == pygame.K_w and game.game_over == False:
                game.rotate()
            # Rotates the block counter clockwise
            if paused == False and event.key == pygame.K_x and game.game_over == False:
                game.undo_rotate()
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
            # Resets the game
            if event.key == pygame.K_r and game.game_over == False:
                game.held_block = None
                game.reset()
        # Updates the block by moving it down
        if paused == False and event.type == GAME_UPDATE and game.game_over == False:
            game.move_down()
            # Makes the speed faster depending on how many 10 lines you've cleared
            if game.lines_cleared_total > 0 and game.lines_cleared_total % 10 == 0:
                new_interval = max(100, 500 - (game.lines_cleared_total // 10) * 50)
                pygame.time.set_timer(GAME_UPDATE, new_interval)
                

    # Drawing
    # The text for the score and cleared lines
    score_value_surface = title_font.render(str(game.score), True, Colors.white)
    cleared_value_surface = title_font.render(str(game.lines_cleared_total), True, Colors.white)

    # The color of the matrix
    screen.fill(Colors.dark_blue)
    # The place and the size of the text
    screen.blit(score_surface, (365, 20, 50, 50))
    screen.blit(next_surface, (375, 180, 50, 50))
    screen.blit(hold_surface, (375, 410, 50, 50))

    # The lines cleared count only appears if the game isn't over
    if game.game_over == True:
        screen.blit(game_over_surface, (320, 137.5, 50, 50))
    else:
        if game.lines_cleared_total < 10:
            screen.blit(cleared_value_surface, (397.5, 135, 50, 50))
        elif game.lines_cleared_total >= 10:
            screen.blit(cleared_value_surface, (390, 135, 50, 50))
    # The block for the score
    pygame.draw.rect(screen, Colors.light_blue, score_rect, 0, 10)
    # The score being auto adjusted to be centered in the block
    screen.blit(score_value_surface, score_value_surface.get_rect(centerx = score_rect.centerx, centery = score_rect.centery))
    
    # The blocks for the Next and Hold area
    pygame.draw.rect(screen, Colors.light_blue, next_rect, 0, 10)
    pygame.draw.rect(screen, Colors.light_blue, hold_rect, 0, 10)
    # Draws the current block, next block, ghost block, and held block
    game.draw(screen)

    # Updates the display and sets the game at 60fps
    pygame.display.update()
    clock.tick(60)