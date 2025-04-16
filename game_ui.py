import pygame as pg
from player import Player
from board import Board

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (50, 50, 50)
TEAL = (115, 199, 199)
YELLOW = (244, 248, 211)
PINK = (247, 207, 216)
LIGHT_PINK = (253, 223, 229)
LIGHT_TEAL = (166, 241, 224)
DARK_TEAL = (74, 133, 135)

GRID_SIZE = 10
TILE_SIZE = 40

class GameGUI:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((800, 600))
        pg.display.set_caption("Heart Stopper Minesweeper")

        self.running = True
        self.game_started = False
        self.start_time = None
        self.player = Player()
        self.board = Board()

        self.tile_states = [[False for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.font = pg.font.Font("font/PixeloidMono.ttf", 25)
        self.title_font = pg.font.Font("font/PixeloidMono.ttf", 50)

        self.classic_bomb_img = pg.transform.scale(pg.image.load("image/classic.png"), (TILE_SIZE, TILE_SIZE))
        self.heartdrain_bomb_img = pg.transform.scale(pg.image.load("image/heartdrain.png"), (TILE_SIZE, TILE_SIZE))
        self.countdown_bomb_img = pg.transform.scale(pg.image.load("image/countdown.png"), (TILE_SIZE, TILE_SIZE))
        self.board.generate_bomb(self.classic_bomb_img, self.heartdrain_bomb_img, self.countdown_bomb_img)
        self.board.set_surrounding_bombs()

        self.heart_img = pg.transform.scale(pg.image.load("image/heart.png"), (30, 30))

        self.grid_start_x = (750 - GRID_SIZE * TILE_SIZE) // 2
        self.grid_start_y = (600 - GRID_SIZE * TILE_SIZE) // 2

        self.bookmarked_tiles = [[False for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

        self.home_screen()

    def home_screen(self):
        self.screen.fill(YELLOW)

        pg.draw.rect(self.screen, WHITE, pg.Rect(100, 100, 600, 400), border_radius=50)
        welcome = self.title_font.render("Welcome!", True, DARK_TEAL)
        start = self.font.render("Start", True, YELLOW)
        quit_btn = self.font.render("Quit", True, YELLOW)

        self.start_btn = pg.Rect(300, 300, 200, 50)
        self.quit_btn = pg.Rect(300, 400, 200, 50)

        self.screen.blit(welcome, welcome.get_rect(center=(400, 200)))

        pg.draw.rect(self.screen, TEAL, self.start_btn, border_radius=20)
        pg.draw.rect(self.screen, TEAL, self.quit_btn, border_radius=20)

        self.screen.blit(start, start.get_rect(center=(400, 325)))
        self.screen.blit(quit_btn, quit_btn.get_rect(center=(400, 425)))

        pg.display.update()

    def display_board(self):
        self.screen.fill(YELLOW)

        self.screen.blit(self.heart_img, (20, 20))
        hearts_text = self.font.render(f"x {self.player.hearts}", True, BLACK)
        self.screen.blit(hearts_text, (60, 20))

        if self.player.hearts == 0:
            self.game_over()
            return

        countdown_text = self.font.render(f"COUNTDOWN: {self.player.countdown}", True, BLACK)
        self.screen.blit(countdown_text, (570, 20))


        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                tile_x = self.grid_start_x + row * (TILE_SIZE + 5)
                tile_y = self.grid_start_y + col * (TILE_SIZE + 5)
                tile_rect = pg.Rect(tile_x, tile_y, TILE_SIZE, TILE_SIZE)

                if self.tile_states[row][col]:
                    pg.draw.rect(self.screen, LIGHT_TEAL, tile_rect, border_radius=5)
                    tile = self.board.grid[row][col]
                    if tile.is_bomb():
                        bomb = tile.get_bomb_type()
                        self.screen.blit(bomb.bomb_img, (tile_x, tile_y))
                    elif tile.get_surrounding_bombs() > 0:
                        text = self.font.render(str(tile.get_surrounding_bombs()), True, BLACK)
                        self.screen.blit(text, text.get_rect(center=tile_rect.center))
                else:
                    pg.draw.rect(self.screen, LIGHT_PINK, tile_rect, border_radius=5)

                pg.draw.rect(self.screen, DARK_TEAL, tile_rect, 2, border_radius=5)

        pg.display.update()

    def handle_click(self, pos):
        if not self.game_started:
            if self.start_btn.collidepoint(pos):
                self.game_started = True
            elif self.quit_btn.collidepoint(pos):
                self.running = False
        else:
            for row in range(GRID_SIZE):
                for col in range(GRID_SIZE):
                    tile_rect = pg.Rect(
                        self.grid_start_x + row * (TILE_SIZE + 5),
                        self.grid_start_y + col * (TILE_SIZE + 5),
                        TILE_SIZE,
                        TILE_SIZE,
                    )
                    if tile_rect.collidepoint(pos) and not self.tile_states[row][col]:
                        self.reveal_tile(row, col)

    def reveal_tile(self, row, col):
        tile = self.board.grid[row][col]
        self.tile_states[row][col] = True

        if tile.is_bomb():
            tile.get_bomb_type().trigger_effect(self.player)
        elif tile.get_surrounding_bombs() == 0:
            self.flood_fill(row, col)

        if self.check_win_condition():
            self.win_screen()

    def flood_fill(self, row, col):
        for dr in range(-1, 2):
            for dc in range(-1, 2):
                r, c = row + dr, col + dc
                if 0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE and not self.tile_states[r][c]:
                    self.tile_states[r][c] = True
                    tile = self.board.grid[r][c]
                    if not tile.is_bomb() and tile.get_surrounding_bombs() == 0:
                        self.flood_fill(r, c)

    def check_win_condition(self):
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                tile = self.board.grid[row][col]
                if not tile.is_bomb() and not self.tile_states[row][col]:
                    return False
        return True

    def win_screen(self):
        self.screen.fill(YELLOW)
        pg.draw.rect(self.screen, WHITE, pg.Rect(100, 100, 600, 400), border_radius=50)
        win_text = self.title_font.render("You Win!", True, DARK_TEAL)
        self.screen.blit(win_text, win_text.get_rect(center=(400, 200)))
        pg.display.update()

    def game_over(self):
        self.screen.fill(YELLOW)
        pg.draw.rect(self.screen, WHITE, pg.Rect(100, 100, 600, 400), border_radius=50)
        game_over_text = self.title_font.render("Game Over", True, DARK_TEAL)
        # home_text = self.font.render("Home", True, YELLOW)
        # quit_text = self.font.render("Quit", True, YELLOW)
        #
        # restart_btn = pg.Rect(300, 300, 200, 50)
        # quit_btn = pg.Rect(300, 400, 200, 50)
        #
        # pg.draw.rect(self.screen, TEAL, restart_btn, border_radius=20)
        # pg.draw.rect(self.screen, TEAL, quit_btn, border_radius=20)
        #
        self.screen.blit(game_over_text, game_over_text.get_rect(center=(400, 200)))
        # self.screen.blit(home_text, home_text.get_rect(center=(400, 325)))
        # self.screen.blit(quit_text, quit_text.get_rect(center=(400, 425)))

        pg.display.update()

    def game_loop(self):
        while self.running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                elif event.type == pg.MOUSEBUTTONDOWN:
                    self.handle_click(event.pos)

            if self.game_started:
                self.display_board()


        pg.quit()
