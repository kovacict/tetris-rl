import pygame
from color import Colors


class Grid:
    def __init__(self):
        self.number_of_rows = 20
        self.number_of_columns = 10
        self.block_size = 30
        self.grid = [
            [0 for i in range(self.number_of_columns)]
            for j in range(self.number_of_rows)
        ]
        self.height = 0
        self.bumpiness = 0
        self.holes = 0
        self.colors = Colors.get_block_colors()

    def print_grid(self):
        for row in range(self.number_of_rows):
            for column in range(self.number_of_columns):
                print(self.grid[row][column], end=" ")
            print()

    def render(self, surface):
        for row in range(self.number_of_rows):
            for column in range(self.number_of_columns):
                block_value = self.grid[row][column]
                block_rect = pygame.Rect(
                    column * self.block_size,
                    row * self.block_size,
                    self.block_size,
                    self.block_size,
                )
                pygame.draw.rect(surface, self.colors[block_value], block_rect)

    def is_inside(self, row, column):
        if (
            row >= 0
            and row < self.number_of_rows
            and column >= 0
            and column < self.number_of_columns
        ):
            return True
        return False

    def is_empty(self, row, column):
        if self.grid[row][column] == 0:
            return True
        return False

    def is_row_full(self, row):
        for column in range(self.number_of_columns):
            if self.grid[row][column] == 0:
                return False
        return True

    def clear_row(self, row):
        for column in range(self.number_of_columns):
            self.grid[row][column] = 0

    def move_row_down(self, row, number_of_rows):
        for column in range(self.number_of_columns):
            self.grid[row + number_of_rows][column] = self.grid[row][column]
            self.grid[row][column] = 0

    def clear_full_rows(self):
        completed_rows = 0
        for row in range(self.number_of_rows - 1, 0, -1):
            if self.is_row_full(row):
                self.clear_row(row)
                completed_rows = completed_rows + 1
            elif completed_rows > 0:
                self.move_row_down(row, completed_rows)
        return completed_rows

    def reset(self):
        for row in range(self.number_of_rows):
            for column in range(self.number_of_columns):
                self.grid[row][column] = 0

    def get_height_and_bumpiness_and_holes(self):
        bumpiness = 0
        height_list = []
        holes = 0

        for column in range(self.number_of_columns):
            for row in range(self.number_of_rows):
                if self.grid[row][column] != 0:
                    height_list.append(20 - (row))
                    break
                if row == 19:
                    height_list.append(0)

        for x in range(len(height_list) - 1):
            bumpiness = bumpiness + abs(height_list[x] - height_list[x + 1])

        for column in range(self.number_of_columns):
            for row in range(
                self.number_of_rows - 1, self.number_of_rows - height_list[column], -1
            ):
                if height_list[column] == 0:
                    break

                if self.grid[row][column] == 0:
                    holes = holes + 1

        self.height = sum(height_list)
        self.bumpiness = bumpiness
        self.holes = holes
        return self.height, self.bumpiness, self.holes
