
from space_obj import SpaceObj


class Ship(SpaceObj):
    """
    A class for representing spaceships.
    """
    RADIUS = 1
    INITIAL_HP = 3

    def __init__(self, x, x_speed, y, y_speed, tip_direction):
        """
        Constructor of ship object.
        :param x: x coordinate of object (int)
        :param x_speed: x velocity of object (int)
        :param y: y coordinate of object (int)
        :param y_speed: y velocity of object (int)
        :param tip_direction: angle between x axis' positive direction and
            the ship's direction in degrees (int)
        """
        super().__init__(x, x_speed, y, y_speed, Ship.RADIUS)
        self.__tip_direction = tip_direction
        self.__hp = Ship.INITIAL_HP

    def get_direction(self):
        """
        :return: ship's direction (angle with positive direction of x axis in
            degrees, float)
        """
        return self.__tip_direction

    def set_direction(self, tip_direction):
        """
        sets new ship direction (angle with positive direction of x axis in
            degrees, float)
        :param tip_direction: new ship direction, float
        """
        self.__tip_direction += tip_direction

    def get_ship_hp(self):
        """
        :return: ship's HP (int)
        """
        return self.__hp

    def deduct_ship_hp(self):
        """
        reduces ship's HP by 1
        """
        self.__hp -= 1
