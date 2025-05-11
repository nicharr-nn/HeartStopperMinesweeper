import os
import csv
import constants
import pygame as pg
from player import Player
from board import Board
from visualizer import Visualizer

class GameGUI:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((800, 600))
        pg.display.set_caption("Heart Stopper Minesweeper")

        self.running = True
        self.game_started = False
        self.start_time = None
        self.fail_reason = None
        self.current_screen = "home"
        self.player = Player()
        self.board = Board()
        self.visualizer = Visualizer()

        self.tile_states = [[False for _ in range(constants.GRID_SIZE)] for _ in range(constants.GRID_SIZE)]
        self.font = pg.font.Font("font/PixeloidMono.ttf", 25)
        self.title_font = pg.font.Font("font/PixeloidMono.ttf", 50)

        self.classic_bomb_img = pg.transform.scale(pg.image.load("image/classic.png"), (constants.TILE_SIZE, constants.TILE_SIZE))
        self.heartdrain_bomb_img = pg.transform.scale(pg.image.load("image/heartdrain.png"), (constants.TILE_SIZE, constants.TILE_SIZE))
        self.countdown_bomb_img = pg.transform.scale(pg.image.load("image/countdown.png"), (constants.TILE_SIZE, constants.TILE_SIZE))
        self.board.generate_bomb(self.classic_bomb_img, self.heartdrain_bomb_img, self.countdown_bomb_img)
        self.board.set_surrounding_bombs()

        self.heart_img = pg.transform.scale(pg.image.load("image/heart.png"), (30, 30))

        self.grid_start_x = (750 - constants.GRID_SIZE * constants.TILE_SIZE) // 2
        self.grid_start_y = (600 - constants.GRID_SIZE * constants.TILE_SIZE) // 2

        self.home_screen()

    def home_screen(self):
        self.screen.fill(constants.YELLOW)

        pg.draw.rect(self.screen, constants.WHITE, pg.Rect(100, 100, 600, 400), border_radius=50)
        welcome = self.title_font.render("Welcome!", True, constants.DARK_TEAL)
        start_txt = self.font.render("Start", True, constants.YELLOW)
        graph_txt = self.font.render("Graphs", True, constants.YELLOW)
        stat_txt = self.font.render("Statistics", True, constants.YELLOW)
        quit_txt = self.font.render("Quit", True, constants.YELLOW)

        self.start_btn = pg.Rect(300, 220, 200, 50)
        self.graph_btn = pg.Rect(300, 280, 200, 50)
        self.stat_btn = pg.Rect(300, 340, 200, 50)
        self.quit_btn = pg.Rect(300, 400, 200, 50)

        self.screen.blit(welcome, welcome.get_rect(center=(400, 180)))

        pg.draw.rect(self.screen, constants.TEAL, self.start_btn, border_radius=20)
        pg.draw.rect(self.screen, constants.TEAL, self.quit_btn, border_radius=20)
        pg.draw.rect(self.screen, constants.TEAL, self.graph_btn, border_radius=20)
        pg.draw.rect(self.screen, constants.TEAL, self.stat_btn, border_radius=20)

        self.screen.blit(start_txt, start_txt.get_rect(center=self.start_btn.center))
        self.screen.blit(quit_txt, quit_txt.get_rect(center=self.quit_btn.center))
        self.screen.blit(graph_txt, graph_txt.get_rect(center=self.graph_btn.center))
        self.screen.blit(stat_txt, stat_txt.get_rect(center=self.stat_btn.center))

        pg.display.update()

    def display_board(self):
        self.screen.fill(constants.YELLOW)

        self.screen.blit(self.heart_img, (20, 20))
        hearts_text = self.font.render(f"x {self.player.hearts}", True, constants.BLACK)
        self.screen.blit(hearts_text, (60, 20))
        moves_text = self.font.render(f"Moves: {self.player.move_count}", True, constants.BLACK)
        self.screen.blit(moves_text, (250, 20))

        current_time = pg.time.get_ticks()
        elapsed_seconds = (current_time - self.start_time) // 1000
        time_text = self.font.render(f"Time: {elapsed_seconds} s", True, constants.BLACK)
        self.screen.blit(time_text, (320, 550))

        if self.player.hearts == 0:
            self.game_over()
            return

        countdown_text = self.font.render(f"Countdown: {self.player.countdown}", True, constants.BLACK)
        self.screen.blit(countdown_text, (570, 20))

        for row in range(constants.GRID_SIZE):
            for col in range(constants.GRID_SIZE):
                tile_x = self.grid_start_x + row * (constants.TILE_SIZE + 5)
                tile_y = self.grid_start_y + col * (constants.TILE_SIZE + 5)
                tile_rect = pg.Rect(tile_x, tile_y, constants.TILE_SIZE, constants.TILE_SIZE)

                if self.tile_states[row][col]:
                    pg.draw.rect(self.screen, constants.LIGHT_TEAL, tile_rect, border_radius=5)
                    tile = self.board.grid[row][col]
                    if tile.is_bomb():
                        bomb = tile.get_bomb_type()
                        self.screen.blit(bomb.bomb_img, (tile_x, tile_y))
                    elif tile.get_surrounding_bombs() > 0:
                        text = self.font.render(str(tile.get_surrounding_bombs()), True, constants.BLACK)
                        self.screen.blit(text, text.get_rect(center=tile_rect.center))
                else:
                    pg.draw.rect(self.screen, constants.LIGHT_PINK, tile_rect, border_radius=5)

                pg.draw.rect(self.screen, constants.DARK_TEAL, tile_rect, 2, border_radius=5)

        pg.display.update()

    def reveal_tile(self, row, col):
        tile = self.board.grid[row][col]
        self.tile_states[row][col] = True

        if tile.is_bomb():
            bomb = tile.get_bomb_type()
            bomb.trigger_effect(self.player)
            if self.player.hearts <= 0:
                self.fail_reason = bomb.__class__.__name__
            elif self.player.countdown_event.is_set() and self.current_screen == "game":
                self.fail_reason = "CountdownBomb"
                self.game_over()

        elif tile.get_surrounding_bombs() == 0:
            self.flood_fill(row, col)

        if self.check_win_condition():
            self.fail_reason = None
            self.win_screen()

    def flood_fill(self, row, col):
        for dr in range(-1, 2):
            for dc in range(-1, 2):
                r, c = row + dr, col + dc
                if 0 <= r < constants.GRID_SIZE and 0 <= c < constants.GRID_SIZE and not self.tile_states[r][c]:
                    self.tile_states[r][c] = True
                    tile = self.board.grid[r][c]
                    if not tile.is_bomb() and tile.get_surrounding_bombs() == 0:
                        self.flood_fill(r, c)

    def check_win_condition(self):
        for row in range(constants.GRID_SIZE):
            for col in range(constants.GRID_SIZE):
                tile = self.board.grid[row][col]
                if not tile.is_bomb() and not self.tile_states[row][col]:
                    return False
        return True

    def win_screen(self):
        end_time = pg.time.get_ticks()
        self.time_taken = (end_time - self.start_time) // 1000
        self.game_result_data("win")

        self.current_screen = "win"
        self.screen.fill(constants.YELLOW)
        pg.draw.rect(self.screen, constants.WHITE, pg.Rect(100, 100, 600, 400), border_radius=50)
        win_text = self.title_font.render("You Win!", True, constants.DARK_TEAL)
        self.screen.blit(win_text, win_text.get_rect(center=(400, 225)))
        pg.display.update()

        self.home_btn = pg.Rect(300, 325, 200, 50)
        pg.draw.rect(self.screen, constants.TEAL, self.home_btn, border_radius=20)
        home_text = self.font.render("Home", True, constants.YELLOW)
        self.screen.blit(home_text, home_text.get_rect(center=(400, 350)))

        pg.display.update()

    def game_over(self):
        end_time = pg.time.get_ticks()
        self.time_taken = (end_time - self.start_time) // 1000
        self.game_result_data("lose")

        self.current_screen = "game_over"
        self.screen.fill(constants.YELLOW)
        pg.draw.rect(self.screen, constants.WHITE, pg.Rect(100, 100, 600, 400), border_radius=50)
        game_over_text = self.title_font.render("Game Over", True, constants.DARK_TEAL)
        self.screen.blit(game_over_text, game_over_text.get_rect(center=(400, 225)))

        self.home_btn = pg.Rect(300, 325, 200, 50)
        pg.draw.rect(self.screen, constants.TEAL, self.home_btn, border_radius=20)
        home_text = self.font.render("Home", True, constants.YELLOW)
        self.screen.blit(home_text, home_text.get_rect(center=(400, 350)))

        pg.display.update()

    def reset_game(self):
        self.player = Player()
        self.board = Board()
        self.board.generate_bomb(self.classic_bomb_img, self.heartdrain_bomb_img, self.countdown_bomb_img)
        self.board.set_surrounding_bombs()
        self.tile_states = [[False for _ in range(constants.GRID_SIZE)] for _ in range(constants.GRID_SIZE)]
        self.game_started = False

    def game_result_data(self, result):
        next_id = 1
        file_path = "game_results.csv"
        if os.path.exists(file_path):
            with open(file_path, mode="r") as file:
                lines = file.readlines()
                if len(lines) > 0:
                    last_line = lines[-1]
                    try:
                        last_id = int(last_line.split(",")[0])
                        next_id = last_id + 1
                    except (ValueError, IndexError):
                        next_id = 1
        with open(file_path, mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([next_id, self.player.move_count, 3 - self.player.hearts, self.time_taken, self.fail_reason, result])

    def graph_screen(self):
        self.current_screen = "graph"
        self.screen.fill(constants.YELLOW)
        pg.draw.rect(self.screen, constants.WHITE, pg.Rect(100, 100, 600, 400), border_radius=50)

        move_hist = self.font.render("Move Count Histogram", True, constants.YELLOW)
        self.move_hist_btn = pg.Rect(175, 150, 450, 40)
        pg.draw.rect(self.screen, constants.TEAL, self.move_hist_btn, border_radius=20)
        self.screen.blit(move_hist, move_hist.get_rect(center=self.move_hist_btn.center))

        hearts_bar = self.font.render("Hearts Lost Bar Chart", True, constants.YELLOW)
        self.hearts_bar_btn = pg.Rect(175, 200, 450, 40)
        pg.draw.rect(self.screen, constants.TEAL, self.hearts_bar_btn, border_radius=20)
        self.screen.blit(hearts_bar, hearts_bar.get_rect(center=self.hearts_bar_btn.center))

        time_box = self.font.render("Time Taken Box Plot", True, constants.YELLOW)
        self.time_box_btn = pg.Rect(175, 250, 450, 40)
        pg.draw.rect(self.screen, constants.TEAL, self.time_box_btn, border_radius=20)
        self.screen.blit(time_box, time_box.get_rect(center=self.time_box_btn.center))

        countdown_pie = self.font.render("Countdown Bomb Pie Chart", True, constants.YELLOW)
        self.countdown_pie_btn = pg.Rect(175, 300, 450, 40)
        pg.draw.rect(self.screen, constants.TEAL, self.countdown_pie_btn, border_radius=20)
        self.screen.blit(countdown_pie, countdown_pie.get_rect(center=self.countdown_pie_btn.center))

        win_loss_pie = self.font.render("Win/Loss Pie Chart", True, constants.YELLOW)
        self.win_loss_pie_btn = pg.Rect(175, 350, 450, 40)
        pg.draw.rect(self.screen, constants.TEAL, self.win_loss_pie_btn, border_radius=20)
        self.screen.blit(win_loss_pie, win_loss_pie.get_rect(center=self.win_loss_pie_btn.center))

        back_text = self.font.render("Back", True, constants.YELLOW)
        self.back_btn = pg.Rect(175, 400, 450, 40)
        pg.draw.rect(self.screen, constants.TEAL, self.back_btn, border_radius=20)
        self.screen.blit(back_text, back_text.get_rect(center=self.back_btn.center))

        pg.display.update()

    def show_graph(self, graph_type):
        if graph_type == "histogram_moves":
            img = pg.image.load("image/graphs/histogram_moves.png")
            img = pg.transform.scale(img, (600, 400))
        elif graph_type == "bar_hearts_lost":
            img = pg.image.load("image/graphs/bar_hearts_lost.png")
            img = pg.transform.scale(img, (600, 400))
        elif graph_type == "box_time_taken":
            img = pg.image.load("image/graphs/box_time_taken.png")
            img = pg.transform.scale(img, (600, 400))
        elif graph_type == "pie_countdown_fail":
            img = pg.image.load("image/graphs/pie_countdown_fail.png")
            img = pg.transform.scale(img, (600, 400))
        elif graph_type == "pie_win_loss":
            img = pg.image.load("image/graphs/pie_win_loss.png")
            img = pg.transform.scale(img, (600, 400))
        else:
            return

        self.screen.fill(constants.YELLOW)
        self.screen.blit(img, (100, 100))

        self.back_graph_btn = pg.Rect(300, 520, 200, 40)
        back_text = self.font.render("Back", True, constants.YELLOW)
        pg.draw.rect(self.screen, constants.TEAL, self.back_graph_btn, border_radius=20)
        self.screen.blit(back_text, back_text.get_rect(center=self.back_graph_btn.center))

        pg.display.update()

    def stat_screen(self):
        self.current_screen = "stats"
        self.screen.fill(constants.YELLOW)

        self.visualizer.statistics_table()
        img = pg.image.load("image/graphs/summary_table.png")
        img = pg.transform.scale(img, (700, 500))
        self.screen.blit(img, (50, 30))

        self.back_stat_btn = pg.Rect(300, 540, 200, 40)
        back_text = self.font.render("Back", True, constants.YELLOW)
        pg.draw.rect(self.screen,constants.TEAL, self.back_stat_btn, border_radius=20)
        self.screen.blit(back_text, back_text.get_rect(center=self.back_stat_btn.center))
        pg.display.update()

        pg.display.update()

    def handle_click(self, pos):
        if self.current_screen == "home":
            if self.start_btn.collidepoint(pos):
                self.reset_game()
                self.current_screen = "game"
                self.game_started = True
                self.start_time = pg.time.get_ticks()
            elif self.quit_btn.collidepoint(pos):
                self.running = False
            elif self.graph_btn.collidepoint(pos):
                self.graph_screen()
            elif self.stat_btn.collidepoint(pos):
                self.stat_screen()

        elif self.current_screen in ["win", "game_over"]:
            if self.home_btn.collidepoint(pos):
                self.current_screen = "home"
                self.game_started = False
                self.visualizer = Visualizer()
                self.home_screen()

        elif self.current_screen == "game":
            for row in range(constants.GRID_SIZE):
                for col in range(constants.GRID_SIZE):
                    tile_rect = pg.Rect(
                        self.grid_start_x + row * (constants.TILE_SIZE + 5),
                        self.grid_start_y + col * (constants.TILE_SIZE + 5),
                        constants.TILE_SIZE,
                        constants.TILE_SIZE,
                    )
                    if tile_rect.collidepoint(pos) and not self.tile_states[row][col]:
                        self.player.increment_move()
                        self.reveal_tile(row, col)

        elif self.current_screen == "graph":
            if self.move_hist_btn.collidepoint(pos):
                self.visualizer.histogram_moves()
                self.show_graph("histogram_moves")
            elif self.hearts_bar_btn.collidepoint(pos):
                self.visualizer.bar_hearts_lost()
                self.show_graph("bar_hearts_lost")
            elif self.time_box_btn.collidepoint(pos):
                self.visualizer.box_time_taken()
                self.show_graph("box_time_taken")
            elif self.countdown_pie_btn.collidepoint(pos):
                self.visualizer.pie_countdown_fail()
                self.show_graph("pie_countdown_fail")
            elif self.win_loss_pie_btn.collidepoint(pos):
                self.visualizer.pie_win_loss()
                self.show_graph("pie_win_loss")
            elif self.back_btn.collidepoint(pos):
                self.current_screen = "home"
                self.home_screen()
            elif self.back_graph_btn.collidepoint(pos):
                self.current_screen = "graph"
                self.graph_screen()
        elif self.current_screen == "stats":
            if self.back_stat_btn.collidepoint(pos):
                self.current_screen = "home"
                self.home_screen()

    def game_loop(self):
        while self.running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                elif event.type == pg.MOUSEBUTTONDOWN:
                    self.handle_click(event.pos)

            if self.current_screen == "game":
                if self.player.countdown_event.is_set():
                    self.fail_reason = "CountdownBomb"
                    self.game_over()
                    continue

                self.display_board()
                if self.check_win_condition():
                    self.win_screen()
                    self.fail_reason = None
                    self.game_started = False

        pg.quit()
