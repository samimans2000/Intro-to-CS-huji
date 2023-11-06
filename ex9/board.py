

class Board:
    """
    This class creates the board object and holds the cars on it. It also moves
    the cars and makes sure they are in place
    """

    NUM_OF_ROWS = 7
    NUM_OF_CUlUMNS = 7
    EMPTY_TILE = '_'
    EXIT_TILE = 'E'
    EXIT_ROW = 3
    EXIT_COORDINATE = 3, 7
    UP = 'u'
    DOWN = 'd'
    RIGHT = 'r'
    LEFT = 'l'
    MSG_UP = "causes the car to drive one tile up"
    MSG_DOWN = "causes the car to drive one tile down"
    MSG_RIGHT = "causes the car to drive one tile right"
    MSG_LEFT = "causes the car to drive one tile left"
    ROW = 0
    COLUMN = 1

    def __init__(self):
        self.__grid = []
        temp = []
        for row in range(self.NUM_OF_ROWS):
            for column in range(self.NUM_OF_CUlUMNS):
                temp.append(self.EMPTY_TILE)
            if row == self.EXIT_ROW:
                temp.append(self.EXIT_TILE)
            self.__grid.append(temp)
            temp = []
        self.__cars_and_movement = {}
        self.__cars_on_grid = {}

    def __str__(self):
        """
        This function is called when a board object is to be printed.
        :return: A string of the current status of the board
        """
        ans = ""
        for row in range(self.NUM_OF_ROWS):
            ans += (" ".join(self.__grid[row]) + '\n')
        return ans

    def cell_list(self):
        """
        This function returns the coordinates of cells in this board
        :return: list of coordinates
        """
        grid_coordinates = []
        for row in range(self.NUM_OF_ROWS):
            for column in range(self.NUM_OF_CUlUMNS):
                grid_coordinates.append((row, column))
        grid_coordinates.append(self.EXIT_COORDINATE)
        return grid_coordinates

    def possible_moves(self):
        """
        This function returns the legal moves of all cars in this board
        :return: list of tuples of the form (name,movekey,description)
                 representing legal moves
        """
        possible_moves = []
        for car_name in self.__cars_and_movement:
            for i in range(2):
                if self.__cars_and_movement[car_name][i] == self.UP:
                    if Board.possible_moves_helper(self, self.UP, car_name):
                        possible_moves.append((car_name,
                                               self.__cars_and_movement[
                                                   car_name][i], self.MSG_UP))
                elif self.__cars_and_movement[car_name][i] == self.DOWN:
                    if Board.possible_moves_helper(self, self.DOWN, car_name):
                        possible_moves.append((car_name,
                                               self.__cars_and_movement[
                                                   car_name][i],
                                               self.MSG_DOWN))
                elif self.__cars_and_movement[car_name][i] == self.RIGHT:
                    if Board.possible_moves_helper(self, self.RIGHT,
                                                   car_name):
                        possible_moves.append((car_name,
                                               self.__cars_and_movement[
                                                   car_name][i],
                                               self.MSG_RIGHT))
                elif self.__cars_and_movement[car_name][i] == self.LEFT:
                    if Board.possible_moves_helper(self, self.LEFT, car_name):
                        possible_moves.append((car_name,
                                               self.__cars_and_movement[
                                                   car_name][i],
                                               self.MSG_LEFT))
        return possible_moves

    def possible_moves_helper(self, movekey, car_name):
        """
        checks if the car can be moves in the direction given
        :param movekey: the direction to be moved to
        :param car_name: the name of the car
        :return: True if can be moved, else False
        """
        temp = (self.__cars_on_grid[car_name]).movement_requirements(movekey)
        if temp[0][self.ROW] < 0 or temp[0][self.COLUMN] < 0:
            return False
        if temp is None:
            return False
        if Board.cell_content(self, temp[0]) is None:
            return True
        else:
            return False

    def target_location(self):
        """
        This function returns the coordinates of the location which is to
         be filled for victory.
        :return: (row,col) of goal location
        """
        return self.EXIT_COORDINATE

    def cell_content(self, coordinate):
        """
        Checks if the given coordinates are empty.
        :param coordinate: tuple of (row,col) of the coordinate to check
        :return: The name if the car in coordinate, None if empty
        """
        row, column = coordinate
        if self.__grid[row][column] == self.EMPTY_TILE or \
                self.__grid[row][column] == self.EXIT_TILE:
            return None
        else:
            return self.__grid[row][column]

    def add_car(self, car):
        """
        Adds a car to the game.
        :param car: car object of car to add
        :return: True upon success. False if failed
        """
        if Board.check_if_legit(self, car):
            for i in car.car_coordinates():
                self.__grid[i[self.ROW]][i[self.COLUMN]] = car.get_name()
            return True
        else:
            return False

    def check_if_legit(self, car):
        """
        checks if the car exists on the board and can be moved
        :param car: the car to be moves
        :return: True if can be moved, else False
        """
        if car.get_name() in self.__cars_on_grid:
            return False
        for i in car.car_coordinates():
            if i not in Board.cell_list(self):
                return False
        for i in car.car_coordinates():
            if self.__grid[i[self.ROW]][i[self.COLUMN]] != self.EMPTY_TILE:
                return False
        else:
            self.__cars_and_movement[car.get_name()] = list(
                car.possible_moves())
            self.__cars_on_grid[car.get_name()] = car
            return True

    def move_car(self, name, movekey):
        """
        moves car one step in given direction.
        :param name: name of the car to move
        :param movekey: Key of move in car to activate
        :return: True upon success, False otherwise
        """
        try:
            name = self.__cars_on_grid[name]
        except KeyError:
            return False
        target_tile = name.movement_requirements(movekey)
        temp = name.car_coordinates()
        if target_tile is None:
            return False
        if target_tile[0][self.ROW] < 0 or target_tile[0][self.COLUMN] < 0:
            return False
        if Board.cell_content(self, target_tile[0]) is None and name.move(
                movekey):
            extra = Board.find_extra(self, temp, name.car_coordinates())
            for i in name.car_coordinates():
                self.__grid[i[self.ROW]][i[self.COLUMN]] = name.get_name()
            self.__grid[extra[0][self.ROW]][extra[0][self.COLUMN]] \
                = self.EMPTY_TILE
            return True
        else:
            return False

    def find_extra(self, list_1, list_2):
        """
        the function checks what tile needs to be changed to an empty tile
        after the movement of the car
        :param list_1: original coordinates
        :param list_2: new coordinates
        :return: tile only found in the original coordinates
        """
        set_1 = set(list_1)
        set_2 = set(list_2)
        extra = set_1 - set_2
        return list(extra)
