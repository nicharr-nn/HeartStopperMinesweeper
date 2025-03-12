import pygame as pg

class GameGUI:
    def __init__(self):
        pg.init()
        self.__screen = pg.display.set_mode((800, 600))
        pg.display.set_caption("Heart Stopper Minesweeper")
        self.__running = True

    def game_loop(self):
        pass

if __name__ == '__main__':
    g1 = GameGUI()
    g1.game_loop()