from grid import Grid
from blocks import *
import random
import copy
import pygame

class Game:
    def __init__(self):
        self.grid = Grid()
        self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
        self.current_block = self.get_random_block()
        self.next_block = self.get_random_block()
        self.held_block = None
        self.lock_delay = 250
        self.lock_timer = None
        self.game_over = False
        self.score = 0
        self.lines_cleared_total = 0

    def update_score(self, lines_cleared, move_down_points):
        if lines_cleared == 1:
            self.score += 100
        elif lines_cleared == 2:
            self.score += 300
        elif lines_cleared == 3:
            self.score += 500
        elif lines_cleared == 4:
            self.score += 1000
        self.score += move_down_points

    def get_random_block(self):
        if len(self.blocks) == 0:
            self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
        block = random.choice(self.blocks)
        self.blocks.remove(block)
        return block
    
    def move_left(self):
        self.current_block.move(0, -1)
        if self.block_inside() == False or self.block_fits() == False:
            self.current_block.move(0, 1)

    def move_right(self):
        self.current_block.move(0, 1)
        if self.block_inside() == False or self.block_fits() == False:
            self.current_block.move(0, -1)
    
    def move_down(self):
        self.current_block.move(1,0)
        if self.block_inside() == False or self.block_fits() == False:
            self.current_block.move(-1, 0)
            if self.lock_timer is None:
                self.lock_timer = pygame.time.get_ticks()
            elif pygame.time.get_ticks() - self.lock_timer >= self.lock_delay:
                self.lock_block()
                self.lock_timer = None
        else:
            self.lock_timer = None
    
    def hard_drop(self):
        while True:
            self.current_block.move(1, 0)
            if self.block_inside() == False or self.block_fits() == False:
                self.current_block.move(-1, 0)
                self.lock_block()
                break

    def hold_block(self):
        if self.held_block == None:
            self.held_block = type(self.current_block)()
            self.current_block = self.next_block
            self.next_block = self.get_random_block()
        else:
            temp = self.held_block
            self.held_block = type(self.current_block)()
            self.current_block = temp

    def lock_block(self):
        tiles = self.current_block.get_cell_positions()
        for positions in tiles:
            self.grid.grid[positions.row][positions.column] = self.current_block.id
        lines_cleared = self.grid.clear_full_rows()
        self.lines_cleared_total += lines_cleared
        self.update_score(lines_cleared, 1)
        self.current_block = self.next_block
        self.next_block = self.get_random_block()
        rows_cleared = self.grid.clear_full_rows()
        self.update_score(rows_cleared, 0)
        if self.block_fits() == False:
            self.game_over = True

    def reset(self):
        self.grid.reset()
        self.blocks = [IBlock(), JBlock(), LBlock(), OBlock(), SBlock(), TBlock(), ZBlock()]
        self.current_block = self.get_random_block()
        self.next_block =  self.get_random_block()
        self.score = 0
        self.lines_cleared_total = 0

    def block_fits(self):
        tiles = self.current_block.get_cell_positions()
        for tile in tiles:
            if self.grid.is_empty(tile.row, tile.column) == False:
                return False
        return True
    
    def gblock_fits(self, block):
        gtiles = block.get_cell_positions()
        for gtile in gtiles:
            if self.grid.is_empty(gtile.row, gtile.column) == False:
                return False
        return True

    def rotate(self):
        self.current_block.rotate()
        if self.block_inside() == False or self.block_fits() == False:
            self.current_block.undo_rotation()

    def undo_rotate(self):
        self.current_block.undo_rotation()
        if self.block_inside() == False or self.block_fits() == False:
            self.current_block.rotate()

    def block_inside(self):
        tiles = self.current_block.get_cell_positions()
        for tile in tiles:
            if self.grid.is_inside(tile.row, tile.column) == False:
                return False
        return True
    
    def gblock_inside(self, block):
        gtiles = block.get_cell_positions()
        for gtile in gtiles:
            if self.grid.is_inside(gtile.row, gtile.column) == False:
                return False
        return True
    
    def draw(self, screen):
        self.grid.draw(screen)
        ghost_block = self.get_ghost_block()
        ghost_block.draw_ghost(screen, 11, 11)
        self.current_block.draw(screen, 11, 11)

        if self.next_block.id == 3:
            self.next_block.draw(screen, 257.5, 290)
        elif self.next_block.id == 4:
            self.next_block.draw(screen, 255, 280)
        else:
            self.next_block.draw(screen, 270, 270)

        if self.held_block is not None and self.held_block.id == 3:
            self.held_block.draw(screen, 257.5, 510)
        elif self.held_block is not None and self.held_block.id == 4:
            self.held_block.draw(screen, 255, 500)
        elif self.held_block is not None:
            self.held_block.draw(screen, 270, 490)
        
    def get_ghost_block(self):
        ghost_block = copy.deepcopy(self.current_block)
        ghost_block.row_offset = self.current_block.row_offset
        ghost_block.column_offset = self.current_block.column_offset
        while True:
            ghost_block.move(1, 0)
            if self.gblock_inside(ghost_block) == False or self.gblock_fits(ghost_block) == False:
                ghost_block.move(-1, 0)
                break
        return ghost_block