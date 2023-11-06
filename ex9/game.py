

import helper
from board import Board
from car import Car
import sys

POSSIBLE_NAMES = {'R', 'G', 'W', 'O', 'B', 'Y'}
NAME = 0
LENGTH = 1
MIN_LEN = 2
MAX_LEN = 4
ORIENTATION = 3
POSSIBLE_ORIENTATION = {0, 1}
START_LOCATION = 2
PATH_FILE = 1



def create_cars_database(filename):
    """
    reads the json file, creates a list of tuples and returns is
    :param filename: the file to be read
    :return: a list of tuples
    """
    cars_raw = helper.load_json(filename)
    cars_list = []
    for i in cars_raw:
        cars_list.append((i, cars_raw[i][0], tuple(cars_raw[i][1]),
                          cars_raw[i][2]))
    return cars_list


def load_cars(cars_list, game_board):
    """
    checks if the cars are legit and adds them to the game board
    :param cars_list: a list of cars
    :param game_board: the game board
    :return: None
    """
    for car in cars_list:
        if car[NAME] not in POSSIBLE_NAMES:
            continue
        if car[LENGTH] < MIN_LEN or car[LENGTH] > MAX_LEN:
            continue
        if car[ORIENTATION] not in POSSIBLE_ORIENTATION:
            continue
        else:
            car = Car(car[NAME], car[LENGTH], car[START_LOCATION],
                      car[ORIENTATION])
            game_board.add_car(car)
    return


class Game:
    """
    the class crates used the class Car and class Board, and runs the game
    """
    EXIT = 'Exit'
    MSG_MOVE = 'car moved'
    MSG_CANT_MOVE = 'wrong movement orientation or car crash with another car'
    MSG_USER_INPUT = 'pls choose a car and a direction to move '
    MSG_WRONG_NAME = 'wrong car name'
    MSG_WRONG_DIRECTION = 'wrong direction chosen'
    MSG_WRONG_INPUT = 'wrong input'
    WRONG_INPUT = "" or " "
    STOP_GAME = '!'
    DIRECTION = 2
    CAR_NAME = 0
    POSSIBLE_DIRECTIONS = {'u', 'd', 'r', 'l'}
    END_GAME_TILE_1 = 3, 7
    END_GAME_TILE_2 = 3, 6

    def __init__(self, board):
        """
        Initialize a new Game object.
        :param board: An object of type board
        """
        self.__board = board

    def __single_turn(self):
        """
        The function runs one round of the game :
            1. Get user's input of: what color car to move, and what
                direction to move it.
            2. Check if the input is valid.
            3. Try moving car according to user's input.
        """
        car, direction = game.get_user_input()
        if car == self.EXIT:
            return None
        else:
            if self.__board.move_car(car, direction):
                print(self.MSG_MOVE)
                return True
            else:
                print(self.MSG_CANT_MOVE)
                return False

    def get_user_input(self):
        """
        the function gets the user input and checks for it validity
        :return: the name of the car and the direction to be moved to, or
        'exit' if the player chose to en the game
        """
        car = None
        direction = None
        car_exists = False
        direction_exists = False
        while not car_exists or not direction_exists:
            user_input = input(self.MSG_USER_INPUT)
            if user_input == self.WRONG_INPUT:
                print(self.MSG_WRONG_INPUT)
                continue
            if user_input == self.STOP_GAME:
                return self.EXIT * 2
            car = user_input[self.CAR_NAME]
            direction = user_input[self.DIRECTION]
            for auto in cars:
                if car not in auto:
                    continue
                else:
                    car_exists = True
            if direction in self.POSSIBLE_DIRECTIONS:
                direction_exists = True
            if not car_exists:
                print(self.MSG_WRONG_NAME)
            elif not direction_exists:
                print(self.MSG_WRONG_DIRECTION)
        return car, direction

    def play(self):
        """
        The main driver of the Game. Manages the game until completion.
        :return: None
        """
        print(self.__board)
        res = self.__single_turn()
        if res is None:
            return
        while self.__board.cell_content(self.END_GAME_TILE_1) is None or\
                self.__board.cell_content(self.END_GAME_TILE_1) != \
                self.__board.cell_content(self.END_GAME_TILE_2):
            if res:
                print(self.__board)
                res = self.__single_turn()
            elif not res:
                res = self.__single_turn()
            elif res == self.EXIT:
                break


if __name__ == "__main__":
    board = Board()
    cars = create_cars_database(sys.argv[PATH_FILE])
    load_cars(cars, board)
    game = Game(board)
    game.play()



