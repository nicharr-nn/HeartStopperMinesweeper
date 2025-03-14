import pygame as pg

GRID_SIZE = 10
TILE_SIZE = 30
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (50, 50, 50)
TEAL = (115, 199, 199)
YELLOW = (244, 248, 211)
PINK = (247, 207, 216)
LIGHT_TEAL = (166, 241, 224)
DARK_TEAL = (74,133,135)

class GameGUI:
    def __init__(self):
        pg.init()
        self.__screen = pg.display.set_mode((800, 600))
        pg.display.set_caption("Heart Stopper Minesweeper")
        self.__running = True
        self.__game_started = False
        self.font = pg.font.Font("font/PixeloidMono.ttf", 25)
        self.title_font = pg.font.Font("font/PixeloidMono.ttf", 50)
        self.home_screen()

    def home_screen(self):
        """Displays the home screen."""
        self.__screen.fill(YELLOW)
        background_text_rect = pg.Rect(100, 100, 600, 400)
        pg.draw.rect(self.__screen, WHITE, background_text_rect, border_radius=50)

        # Render text using the preloaded font
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
        """Renders the grid."""
        pass

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
