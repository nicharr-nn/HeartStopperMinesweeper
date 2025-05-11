class Bomb:
    def __init__(self, bomb_img):
        self.bomb_img = bomb_img

    def trigger_effect(self, player):
        pass

class ClassicBomb(Bomb):
    def trigger_effect(self, player):
        player.hearts = 0

class HeartDrainBomb(Bomb):
    def trigger_effect(self, player):
        player.lose_heart()

class CountdownBomb(Bomb):
    def trigger_effect(self, player):
        player.start_countdown()
