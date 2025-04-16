import time
import threading

class Player:
    def __init__(self):
        self.hearts = 3
        self.countdown = 30
        self.countdown_active = False
        self.move_count = 0

    def lose_heart(self):
        self.hearts -= 1

    def is_alive(self):
        return self.hearts > 0

    def increment_move(self):
        self.move_count += 1

    def start_countdown(self, duration=30):
        if self.countdown_active:
            return

        self.countdown = duration
        self.countdown_active = True

        def countdown_logic():
            while self.countdown > 0 and self.hearts > 0:
                time.sleep(1)
                self.countdown -= 1
            if self.countdown <= 0:
                self.hearts = 0

        threading.Thread(target=countdown_logic, daemon=True).start()
