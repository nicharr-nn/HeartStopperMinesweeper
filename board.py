import random
import constants
from tile import Tile
from bomb import ClassicBomb, HeartDrainBomb, CountdownBomb

class Board:
    def __init__(self):
        self.grid = self.initial_grid()

    @staticmethod
    def initial_grid():
        grid = []
        for row in range(constants.GRID_SIZE):
            grid.append([])
            for _ in range(constants.GRID_SIZE):
                grid[row].append(Tile())
        return grid

    def get_grid(self):
        return self.grid

    def set_surrounding_bombs(self):
        for row in range(constants.GRID_SIZE):
            for col in range(constants.GRID_SIZE):
                self.grid[row][col].set_surrounding_bombs(self.get_surrounding_bombs_tile(row, col))

    def get_surrounding_bombs_tile(self, row, col):
        surrounding_bombs = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                new_row = row + i
                new_col = col + j
                if 0 <= new_row < constants.GRID_SIZE and 0 <= new_col < constants.GRID_SIZE:
                    if self.grid[new_row][new_col].is_bomb():
                        surrounding_bombs += 1
        return surrounding_bombs

    def generate_bomb(self, classic_img, heart_drain_img, countdown_img):
        bomb_classes = [ClassicBomb, HeartDrainBomb, CountdownBomb]
        bomb_counts = [3, 8, 4]
        positions = random.sample(range(constants.GRID_SIZE * constants.GRID_SIZE),
                                  sum(bomb_counts))

        for bomb_cls, count in zip(bomb_classes, bomb_counts):
            for _ in range(count):
                pos = positions.pop()
                row = pos // constants.GRID_SIZE
                col = pos % constants.GRID_SIZE
                if bomb_cls == ClassicBomb:
                    bomb_instance = bomb_cls(classic_img)
                elif bomb_cls == HeartDrainBomb:
                    bomb_instance = bomb_cls(heart_drain_img)
                elif bomb_cls == CountdownBomb:
                    bomb_instance = bomb_cls(countdown_img)

                self.grid[row][col].set_bomb(bomb_instance)
