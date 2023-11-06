


class SpaceObj:
    """
    class for representing generic objects floating in space
    """

    def __init__(self, x, x_speed, y, y_speed, radius):
        """
        Constructor, initializes the object.
        :param x: x coordinate of object (int)
        :param x_speed: x velocity of object (int)
        :param y: y coordinate of object (int)
        :param y_speed: y velocity of object (int)
        :param radius: radius of object (int)
        """
        self.__x = x
        self.__x_speed = x_speed
        self.__y = y
        self.__y_speed = y_speed
        self.__radius = radius

    def get_x(self):
        """
        :return: the object's x coordinate (int)
        """
        return self.__x

    def get_x_speed(self):
        """
        :return: the object's x velocity (int)
        """
        return self.__x_speed

    def get_y(self):
        """
        :return: the object's y coordinate (int)
        """
        return self.__y

    def get_y_speed(self):
        """
        :return: the object's y velocity (int)
        """
        return self.__y_speed

    def get_radius(self):
        """
        :return: the object's radius (int)
        """
        return self.__radius

    def set_x(self, x):
        """
        :param x: new x coordinate for the object (int)
        """
        self.__x = x

    def set_x_speed(self, x_speed):
        """
        :param x_speed: new x velocity for the object (int)
        """
        self.__x_speed = x_speed

    def set_y(self, y):
        """
        :param y: new y coordinate for the object (int)
        """
        self.__y = y

    def set_y_speed(self, y_speed):
        """
        :param y_speed: new y velocity for the object (int)
        """
        self.__y_speed = y_speed

    def set_radius(self, rad):
        """
        :param rad: new radius for the object (int)
        """
        self.__radius = rad

    def dist(self, x2, y2):
        """
        :param x2: an x coordinate
        :param y2: a y coordinate
        :return: distance from own center to given coordinates (float)
        """
        return ((self.__x - x2) ** 2 + (self.__y - y2) ** 2) ** 0.5
