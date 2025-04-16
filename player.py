import time
import threading

class Player:
    def __init__(self):
        self.hearts = 3
        self.countdown = None
        self.move_count = 0

    def lose_heart(self):
        self.hearts -= 1

    def is_alive(self):
        return self.hearts > 0

    def increment_move(self):
        self.move_count += 1

    def start_countdown(self, duration=30):
        self.countdown = duration

        def countdown_logic():
            while self.countdown > 0:
                time.sleep(1)
                self.countdown -= 1
            self.hearts = 0

        threading.Thread(target=countdown_logic).start()
