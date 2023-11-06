

from space_obj import SpaceObj


class Asteroid(SpaceObj):
    def rad_from_size(size):
        """
        :param size: size of some asteroid (int)
        :return: radius of an asteroid of given size
        """
        return size * 10 - 5

    def __init__(self, x, x_speed, y, y_speed, size):
        """
        Constructor of Asteroid object.
        :param x: x coordinate of asteroid (int)
        :param x_speed: x velocity of asteroid (int)
        :param y: y coordinate of asteroid (int)
        :param y_speed: y velocity of asteroid (int)
        :param size: size of asteroid (int)
        """
        super().__init__(x, x_speed, y, y_speed, Asteroid.rad_from_size(size))
        self.__size = size

    def get_size(self):
        """
        :return: size of asteroid (int)
        """
        return self.__size

    def has_intersection(self, obj):
        """
        :param obj: a "space object" of class space_obj or an inheriting
            class such as Ship, Torpedo or Asteroid.
        :return: True if the asteroid intersects with another space object,
            False otherwise.
        """
        return self.dist(obj.get_x(), obj.get_y()) <= \
               self.get_radius() + obj.get_radius()

    # asteroid sizes are fixed - no need of a size setter function
