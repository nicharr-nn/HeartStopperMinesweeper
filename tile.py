class Tile:
    def __init__(self):
        self.__is_bomb = False
        self.__surrounding_bombs = 0
        self.__bomb_type = None

    def get_bomb_type(self):
        return self.__bomb_type

    def set_bomb(self, bomb_type):
        self.__bomb_type = bomb_type
        self.__is_bomb = bomb_type is not None

    def is_bomb(self):
        return self.__is_bomb

    def get_surrounding_bombs(self):
        return self.__surrounding_bombs

    def set_surrounding_bombs(self, surrounding_bombs):
        self.__surrounding_bombs = surrounding_bombs