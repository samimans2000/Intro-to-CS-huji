
class Car:
    """
    This class creates the object 'car' , by assigning a name, length,
     location, and orientation. The class also checks the legal moves of
    each object and the confidants of each object on the map.
    """
    VERTICAL = 0
    HORIZONTAL = 1
    ROW = 0
    COlUMN = 1
    UP = 'u'
    DOWN = 'd'
    RIGHT = 'r'
    LEFT = 'l'
    MSG_UP = "causes the car to drive one tile up"
    MSG_DOWN = "causes the car to drive one tile down"
    MSG_RIGHT = "causes the car to drive one tile right"
    MSG_LEFT = "causes the car to drive one tile left"
    LAST = -1
    FIRST = 0

    def __init__(self, name, length, location, orientation):
        """
        A constructor for a Car object
        :param name: A string representing the car's name
        :param length: A positive int representing the car's length.
        :param location: A tuple representing the car's head (row, col)
                        location
        :param orientation: One of either 0 (VERTICAL) or 1 (HORIZONTAL)
        """
        self.__name = name
        self.__length = length
        self.__location = location
        self.__orientation = orientation

    def car_coordinates(self):
        """
        :return: A list of coordinates the car is in
        """
        ans = [self.__location]
        temp = list(self.__location)
        if self.__orientation == self.VERTICAL:
            for i in range(self.__length - 1):
                temp[self.ROW] += 1
                ans.append(tuple(temp))
        elif self.__orientation == self.HORIZONTAL:
            for i in range(self.__length - 1):
                temp[self.COlUMN] += 1
                ans.append(tuple(temp))
        return ans

    def possible_moves(self):
        """
        :return: A dictionary of strings describing possible movements
         permitted by this car.
        """
        move_dic = {}
        if self.__orientation == self.VERTICAL:
            move_dic[self.UP] = self.MSG_UP
            move_dic[self.DOWN] = self.MSG_DOWN
        if self.__orientation == self.HORIZONTAL:
            move_dic[self.RIGHT] = self.MSG_RIGHT
            move_dic[self.LEFT] = self.MSG_LEFT
        return move_dic

    def movement_requirements(self, movekey):
        """
        :param movekey: A string representing the key of the required move.
        :return: A list of cell locations which must be empty in order for this
         move to be legal.
        """
        if self.__orientation == self.VERTICAL:
            if movekey == self.DOWN:
                temp = list(self.car_coordinates()[self.LAST])
                temp[self.ROW] += 1
                return [tuple(temp)]
            elif movekey == self.UP:
                temp = list(self.car_coordinates()[self.FIRST])
                temp[self.ROW] -= 1
                return [tuple(temp)]
        elif self.__orientation == self.HORIZONTAL:
            if movekey == self.RIGHT:
                temp = list(self.car_coordinates()[self.LAST])
                temp[self.COlUMN] += 1
                return [tuple(temp)]
            elif movekey == self.LEFT:
                temp = list(self.car_coordinates()[self.FIRST])
                temp[self.COlUMN] -= 1
                return [tuple(temp)]

    def move(self, movekey):
        """
        :param movekey: A string representing the key of the required move.
        :return: True upon success, False otherwise
        """
        if self.__orientation == self.VERTICAL:
            if movekey == self.DOWN:
                temp = list(self.__location)
                temp[self.ROW] += 1
                self.__location = tuple(temp)
                self.car_coordinates()
                return True
            elif movekey == self.UP:
                temp = list(self.__location)
                temp[self.ROW] -= 1
                self.__location = tuple(temp)
                self.car_coordinates()
                return True
        elif self.__orientation == self.HORIZONTAL:
            if movekey == self.RIGHT:
                temp = list(self.__location)
                temp[self.COlUMN] += 1
                self.__location = tuple(temp)
                self.car_coordinates()
                return True
            elif movekey == self.LEFT:
                temp = list(self.__location)
                temp[self.COlUMN] -= 1
                self.__location = tuple(temp)
                self.car_coordinates()
                return True
        else:
            return False

    def get_name(self):
        """
        :return: The name of this car.
        """
        return self.__name
