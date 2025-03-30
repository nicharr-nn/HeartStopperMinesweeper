import pygame as pg
from player import Player

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (50, 50, 50)
TEAL = (115, 199, 199)
YELLOW = (244, 248, 211)
PINK = (247, 207, 216)
LIGHT_PINK = (253, 223, 229)
LIGHT_TEAL = (166, 241, 224)
DARK_TEAL = (74,133,135)
GRID_SIZE = 10
TILE_SIZE = 40

class GameGUI:
    def __init__(self):
        pg.init()
        self.__screen = pg.display.set_mode((800, 600))
        pg.display.set_caption("Heart Stopper Minesweeper")
        self.__running = True
        self.__game_started = False
        # self.player = Player()

        self.font = pg.font.Font("font/PixeloidMono.ttf", 25)
        self.title_font = pg.font.Font("font/PixeloidMono.ttf", 50)

        self.classic_bomb_img = pg.transform.scale(pg.image.load("image/classic.png"), (TILE_SIZE, TILE_SIZE))
        self.heartdrain_bomb_img = pg.transform.scale(pg.image.load("image/heartdrain.png"), (TILE_SIZE, TILE_SIZE))
        self.countdown_bomb_img = pg.transform.scale(pg.image.load("image/countdown.png"), (TILE_SIZE, TILE_SIZE))

        self.home_screen()

    def home_screen(self):
        """Displays the home screen."""
        self.__screen.fill(YELLOW)

        background_text_rect = pg.Rect(100, 100, 600, 400)
        pg.draw.rect(self.__screen, WHITE, background_text_rect, border_radius=50)

        text_welcome = self.title_font.render("Welcome!", True, DARK_TEAL)
        text_start_btn = self.font.render("Start", True, YELLOW)
        text_quit_btn = self.font.render("Quit", True, YELLOW)

        self.start_btn = pg.Rect(300, 300, 200, 50)
        self.quit_btn = pg.Rect(300, 400, 200, 50)

        text_welcome_rect = text_welcome.get_rect(center=(400, 200))
        text_start_btn_rect = text_start_btn.get_rect(center=(400, 325))
        text_quit_btn_rect = text_quit_btn.get_rect(center=(400, 425))

        self.__screen.blit(text_welcome, text_welcome_rect)

        pg.draw.rect(self.__screen, TEAL, self.start_btn, border_radius=20)
        pg.draw.rect(self.__screen, TEAL, self.quit_btn, border_radius=20)

        self.__screen.blit(text_start_btn, text_start_btn_rect)
        self.__screen.blit(text_quit_btn, text_quit_btn_rect)

        pg.display.update()


    def display_board(self):
        """Renders the grid. Game screen"""
        self.__screen.fill(YELLOW)

        heart_img = pg.image.load("image/heart.png")
        heart_img = pg.transform.scale(heart_img, (30, 30))
        self.__screen.blit(heart_img, (20, 20))

        font = pg.font.Font("font/PixeloidMono.ttf", 24)
        hearts_text = font.render(f"x {self.player.hearts}", True, BLACK)
        self.__screen.blit(hearts_text, (60, 20))

        score_text = font.render(f"COUNTDOWN:", True, BLACK)
        self.__screen.blit(score_text, (570, 20))

        grid_start_x = (750 - GRID_SIZE * TILE_SIZE) // 2
        grid_start_y = (600 - GRID_SIZE * TILE_SIZE) // 2

        # Draw grid
        for x in range(GRID_SIZE):
            for y in range(GRID_SIZE):
                tile_rect = pg.Rect(grid_start_x + x * (TILE_SIZE+5), grid_start_y + y * (TILE_SIZE+5), TILE_SIZE, TILE_SIZE)
                pg.draw.rect(self.__screen, LIGHT_PINK, tile_rect, border_radius=5)

        pg.display.update()


    def handle_click(self, pos):
        """Handles button clicks on the screen."""
        if self.start_btn.collidepoint(pos):
            self.__game_started = True
        elif self.quit_btn.collidepoint(pos):
            self.__running = False

    def game_loop(self):
        """Game loop handling events."""
        while self.__running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.__running = False
                elif event.type == pg.MOUSEBUTTONDOWN and not self.__game_started:
                    self.handle_click(event.pos)

            if self.__game_started:
                self.display_board()

        pg.quit()


if __name__ == '__main__':
    g1 = GameGUI()
    g1.game_loop()