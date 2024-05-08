from grid import Grid
from blocks import *
import random
import numpy as np
import copy
from color import Colors
import torch

class Game:
    def __init__(self):
        self.grid = Grid()
        self.blocks = []
        self.current_block = self.get_block()
        self.game_over = False
        self.score = 0
        self.lines_cleared=0
        self.cumulative_lines_cleared=0
        self.blocks_placed=0
        self.rows_cleared=0
        self.reward=0

    def get_block(self, id=None):
        if (id==None):
            if len(self.blocks) == 0:
                self.blocks = [
                    JBlock(),
                    LBlock(),
                    IBlock(),
                    OBlock(),
                    SBlock(),
                    ZBlock(),
                    TBlock(),
                ]

            block = random.choice(self.blocks)

            self.blocks.remove(block)

            return block
        elif id==0:
            return LBlock()
        elif id==1:
            return JBlock()
        elif id==2:
            return IBlock()
        elif id==3:
            return OBlock()
        elif id==4:
            return SBlock()
        elif id==5:
            return ZBlock()
        elif id==6:
            return TBlock()

    def render(self, surface):
        self.grid.render(surface)
        self.current_block.render(surface)

    def move_left(self):
        self.current_block.move(0, -1)
        if self.block_inside_window() == False or self.block_fits() == False:
            self.current_block.move(0, 1)

    def move_right(self):
        self.current_block.move(0, 1)
        if self.block_inside_window() == False or self.block_fits() == False:
            self.current_block.move(0, -1)

    def move_down(self):
        self.current_block.move(1, 0)
        self.reward=0
        if self.block_inside_window() == False or self.block_fits() == False:
            self.current_block.move(-1, 0)
            self.lock_block()
            return False
        return True

    def block_inside_window(self):
        tiles = self.current_block.get_cell_positions()
        for tile in tiles:
            if self.grid.is_inside(tile[0], tile[1]) == False:
                return False
        return True

    def rotate(self):
        self.current_block.rotate()
        if self.block_inside_window() == False or self.block_fits() == False:
            self.current_block.undo_rotate()

    def lock_block(self):
        
        self.lines_cleared=0
        tiles = self.current_block.get_cell_positions()
        for position in tiles:
            self.grid.grid[position[0]][position[1]] = 1
        #self.current_block = self.get_block()
        self.lines_cleared=self.grid.clear_full_rows()

       

    def block_fits(self):
        tiles = self.current_block.get_cell_positions()
        for tile in tiles:
            if self.grid.is_empty(tile[0], tile[1]) == False:
                return False
        return True

    def reset(self):
        self.grid.reset()
        self.blocks = []
        self.current_block = self.get_block()
        self.score=0
        self.reward=0
        self.lines_cleared=0
        self.cumulative_lines_cleared=0
        self.blocks_placed=0
        self.game_over=False

    def update_score(self,lines_cleared):
        if self.game_over==True:
            self.reward=-100
            return
        if lines_cleared==1:
            self.score=self.score+100
            self.reward=100
        elif lines_cleared==2:
            self.score=self.score+250
            self.reward=250
        elif lines_cleared==3:
            self.score=self.score+500
            self.reward=500
        elif lines_cleared==4:
            self.score=self.score+1000
            self.reward=1000
        else:
            self.score=self.score+5
        self.cumulative_lines_cleared=self.cumulative_lines_cleared+self.lines_cleared
        self.reward=5#*self.grid.number_of_columns**(self.lines_cleared/2)-(0.15*self.grid.height+0.1*self.grid.holes+0.05*self.grid.bumpiness)
        self.blocks_placed=self.blocks_placed+1
        

    def play_step(self, rotation, move):
        # [left, right, rotate, do_nothing]
        self.current_block.rotation=rotation
        self.current_block.move(0,move)
        if self.block_fits() == False:
            self.game_over = True
        while self.move_down():
            pass
        self.update_score(self.lines_cleared)
        self.current_block=self.get_block()


    
    #def touching_a_border(self):
    #    tiles = self.current_block.get_cell_positions()
    #    for cell in tiles:
    #        if cell[1]==0:
    #            return 1, 0
    #        elif cell[1]==9:
    #            return 0, 1
    #        else:
    #            pass
    #    return 0,0
    
    def get_x_y_coordinate(self):
        tiles=self.current_block.get_cell_positions()
        x=tiles[0][0]
        y=tiles[0][1]

        return x,y
    
    def get_properties(self):
        height,bumpiness,holes=self.grid.get_height_and_bumpiness_and_holes()
        lines_cleared=self.lines_cleared
        state=np.array([lines_cleared,height,bumpiness,holes],dtype=np.float32)
        return torch.FloatTensor(state)

    def get_next_states(self):
        starting_grid=copy.deepcopy(self.grid.grid)
        states={}
        block_id=self.current_block.id
        self.current_block.color=Colors.red
        for rotation in [0,90,180,270]:
            min_x,max_x=self.current_block.get_min_and_max_x()
            for x in range(min_x,max_x+1):
                self.current_block.row_offset=0
                self.current_block.column_offset=0
                self.current_block.rotation=rotation
                self.current_block.move(0,x)
                while self.move_down():
                    pass
                states[(rotation,x)]=self.get_properties()
                self.current_block=self.get_block(block_id)
                self.grid.grid=copy.deepcopy(starting_grid)
                
        return states
