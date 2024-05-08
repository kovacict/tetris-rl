from color import Colors
import pygame

class Block:
    def __init__(self,id):
        self.id=id
        self.cells={}
        self.block_size=30
        self.row_offset=0
        self.column_offset=0
        self.rotation=0
        self.color=Colors.get_block_colors()

    def render(self, surface):
        tiles=self.get_cell_positions()
        for tile in tiles:
            tile_rect=pygame.Rect(tile[1]*self.block_size, tile[0]*self.block_size,self.block_size,self.block_size)
            pygame.draw.rect(surface, self.color[2],tile_rect)

    def move(self, rows, columns):
        self.row_offset=self.row_offset+rows
        self.column_offset=self.column_offset+columns

    def get_cell_positions(self):
        tiles = self.cells[self.rotation]
        moved_tiles=[]
        for position in tiles:
            position=(position[0]+self.row_offset,position[1]+self.column_offset)
            moved_tiles.append(position)
        return moved_tiles
    
    def rotate(self):
        self.rotation=(self.rotation+90)%360
    
    def undo_rotate(self):
        self.rotation=(self.rotation-90)%360

    def get_min_and_max_x(self):
        tiles=self.get_cell_positions()
        for i in range(0,-3,-1):
            columns=[tile[1] for tile in tiles]
            columns = [x + i for x in columns]
            if min(columns)==0:
                min_x=i
                break
        for i in range(6,10,1):
            columns=[tile[1] for tile in tiles]
            columns=[x + i for x in columns]
            if max(columns)==9:
                max_x=i
                break
        return min_x, max_x

