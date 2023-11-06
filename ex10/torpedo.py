
from space_obj import SpaceObj


class Torpedo(SpaceObj):
    """
    class for representing torpedos.
    """
    RADIUS = 4
    INITIAL_LIFE = 200

    def __init__(self, x, x_speed, y, y_speed, direction):
        """
        Constructor of Torpedo object.
        :param x: x coordinate of torpedo (int)
        :param x_speed: x velocity of torpedo (int)
        :param y: y coordinate of torpedo (int)
        :param y_speed: y velocity of torpedo (int)
        :param direction: angle between x axis' positive direction and
            the torpedo's direction in degrees (int)
        """
        super().__init__(x, x_speed, y, y_speed, Torpedo.RADIUS)
        self.__direction = direction
        self.__life = Torpedo.INITIAL_LIFE

    def get_direction(self):
        """
        :return: torpedo's direction (angle with positive direction of x axis
            in degrees, float)
        """
        return self.__direction

    def get_life(self):
        """
        :return: torpedo's life (int)
        """
        return self.__life

    def deduct_life(self):
        """
        reduces torpedo's life by 1
        """
        self.__life -= 1

    # no need of set_direction - torpedo directions do not change
