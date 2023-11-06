

from screen import Screen
from ship import Ship
from asteroid import Asteroid
from torpedo import Torpedo
from node import Node
from linked_list import SimpleDoublyLinkedList
import sys
import random
import math

DEFAULT_ASTEROIDS_NUM = 5
MAX_TORPEDO_NUM = 10
DEFAULT_ASTEROID_SIZE = 3
DEFAULT_ASTEROID_RAD = Asteroid.rad_from_size(DEFAULT_ASTEROID_SIZE)
INIT_SHIP_VX = 0
INIT_SHIP_VY = 0
INIT_SHIP_DIR = 0
MIN_INIT_AST_VX = 1
MAX_INIT_AST_VX = 4
MIN_INIT_AST_VY = 1
MAX_INIT_AST_VY = 4
POINTS_BY_SIZE = {1: 100, 2: 50, 3: 20}


class GameRunner:
    """
    Class of Asteroidsgame running objects.
    """

    def __init__(self, asteroids_num):
        """
        Constructor of a GameRunner object for running an Asteroids game.
        Initializes the game, createing a ship and some asteroids.
        :param asteroids_num: number of initial asteroids
        """
        self.__screen = Screen()
        ship_x = random.randint(Screen.SCREEN_MIN_X, Screen.SCREEN_MAX_X)
        ship_y = random.randint(Screen.SCREEN_MIN_Y, Screen.SCREEN_MAX_Y)
        self.__ship = Ship(ship_x, INIT_SHIP_VX, ship_y, INIT_SHIP_VY,
                           INIT_SHIP_DIR)
        self.__asteroids_linked = SimpleDoublyLinkedList()
        self.__ast_num = 0  # next loop will increase it as necessary
        for i in range(asteroids_num):
            self.generate_asteroid()
        self.__torpedos_linked = SimpleDoublyLinkedList()
        self.__tor_num = 0
        self.__score = 0

    def add_asteroid(self, ast):
        """
        Adds an asteroid to the game (by adding it to the asteroid linked list,
        registering it to the screen and updatong the number of asteroids)
        :pasram ast: asteroid object to add
        """
        self.__screen.register_asteroid(ast, ast.get_size())
        self.__asteroids_linked.add(Node(ast))
        self.__ast_num += 1

    def remove_asteroid(self, ast_node):
        """
        Removes an asteroid from the game (by removing it from the asteroids
        linked list, unregistering it from the screen and updatong the number
        of asteroids).
        :pasram ast_node: The Node of the asteroid to remove
        """
        self.__screen.unregister_asteroid(ast_node.get_data())
        self.__asteroids_linked.remove(ast_node)
        self.__ast_num -= 1

    def generate_asteroid(self):
        """
        Creates an asteroid object at a random place on the screen that does
        not intersect with the ship and links it to the asteroid list.
        """
        ship = self.__ship  # for readability
        while True:
            ast_x = random.randint(Screen.SCREEN_MIN_X, Screen.SCREEN_MAX_X)
            ast_y = random.randint(Screen.SCREEN_MIN_Y, Screen.SCREEN_MAX_Y)
            if ship.dist(ast_x,
                         ast_y) > ship.get_radius() + DEFAULT_ASTEROID_RAD:
                break
        ast = Asteroid(ast_x, random.randint(MIN_INIT_AST_VX, MAX_INIT_AST_VX),
                       ast_y, random.randint(MIN_INIT_AST_VY, MAX_INIT_AST_VY),
                       DEFAULT_ASTEROID_SIZE)
        self.add_asteroid(ast)

    def add_torpedo(self, tor):
        """
        Adds a torpedo to the game (by adding it to the torpedos linked list,
        registering it to the screen and updatong the number of torpedos)
        :pasram tor: Torpedo object to add
        """
        self.__screen.register_torpedo(tor)
        self.__torpedos_linked.add(Node(tor))
        self.__tor_num += 1

    def remove_torpedo(self, tor_node):
        """
        Removes a torpedo from the game (by removing it from the torpedos
        linked list, unregistering it from the screen and updatong the number
        of torpedos).
        :pasram tor_node: The Node of the torpedo to remove
        """
        self.__screen.unregister_torpedo(tor_node.get_data())
        self.__torpedos_linked.remove(tor_node)
        self.__tor_num -= 1

    def run(self):
        self._do_loop()
        self.__screen.start_screen()

    def _do_loop(self):
        # You should not change this method!
        self._game_loop()
        # Set the timer to go off again
        self.__screen.update()
        self.__screen.ontimer(self._do_loop, 5)

    def _game_loop(self):
        """
        The main game loop. Updates the display, moves the objects, reacts
        to input (key presses) and checks for collisions and game end,
        handling them as needed.
        """
        self.__screen.set_score(self.__score)
        self.navigate_ship()
        if self.__screen.is_space_pressed() and \
                self.__tor_num < MAX_TORPEDO_NUM:
            self.launch_torpedo()
        self.move_draw_all()
        self.check_and_handle_collisions()
        self.routine_end_check()

    def check_and_handle_collisions(self):
        """
        Checks and handles collisions of asteroids with the ship or with
        torpedos.
        """
        ast_node = self.__asteroids_linked.get_head()
        while ast_node:
            ast = ast_node.get_data()

            # collision with ship:
            if ast.has_intersection(self.__ship):
                self.ship_collision(ast_node)
                ast_node = ast_node.get_next()
                continue  # no need to check for collisions with torpedos

            # collision with torpedo:
            tor_node = self.__torpedos_linked.get_head()
            while tor_node:
                tor = tor_node.get_data()
                if ast.has_intersection(tor):
                    self.torpedo_hit(tor_node, ast_node)
                    break  # no need to check for more collisions with torpedos
                tor_node = tor_node.get_next()
            ast_node = ast_node.get_next()

    def routine_end_check(self):
        """
        Checks if the game should end (axcluding losses by collision with 3rd
        asteroid). If it does, displays an appropriate message and quits.
        """
        if self.__ast_num == 0:
            self.game_over("You won! your score is: " + str(self.__score))
        if self.__screen.should_end():
            self.game_over("See you next time!")

    def move_draw_all(self):
        """
        Moves all Space objects according to their velocity and draws them
        in their new places. Removes old torpedos.
        """
        # Ship:
        self.move(self.__ship)
        self.__screen.draw_ship(self.__ship.get_x(), self.__ship.get_y(),
                                self.__ship.get_direction())
        # Asteroids:
        ast_node = self.__asteroids_linked.get_head()
        while ast_node != None:
            ast = ast_node.get_data()
            self.move(ast)
            self.__screen.draw_asteroid(ast, ast.get_x(), ast.get_y())
            ast_node = ast_node.get_next()

        # Torpedos
        tor_node = self.__torpedos_linked.get_head()
        while tor_node != None:
            tor = tor_node.get_data()
            if tor.get_life() == 0:
                self.remove_torpedo(tor_node)
            else:
                tor.deduct_life()
                self.move(tor)
                self.__screen.draw_torpedo(tor, tor.get_x(), tor.get_y(),
                                           tor.get_direction())
            tor_node = tor_node.get_next()

    def move(self, obj):
        """
        Moves obj according to its velocity.
        :param obj: an object of type SpaceObj or of an inheriting class
        (asteroid, torpedo or spaceship) to move.
        """
        new_x = Screen.SCREEN_MIN_X + (
                    obj.get_x() + obj.get_x_speed() - Screen.SCREEN_MIN_X) \
                % (Screen.SCREEN_MAX_X - Screen.SCREEN_MIN_X)
        obj.set_x(new_x)
        new_y = Screen.SCREEN_MIN_Y + (
                    obj.get_y() + obj.get_y_speed() - Screen.SCREEN_MIN_Y) \
                % (Screen.SCREEN_MAX_Y - Screen.SCREEN_MIN_Y)
        obj.set_y(new_y)

    def navigate_ship(self):
        """
        If a move key (up, right or left arrows) has been pressed, rotates and
        accelerates the ship as necessary.
        """
        if self.__screen.is_right_pressed():
            self.__ship.set_direction(-7)
        if self.__screen.is_left_pressed():
            self.__ship.set_direction(7)
        if self.__screen.is_up_pressed():
            rad_direction = math.pi / 180 * self.__ship.get_direction()
            self.__ship.set_x_speed(
                self.__ship.get_x_speed() + math.cos(rad_direction))
            self.__ship.set_y_speed(
                self.__ship.get_y_speed() + math.sin(rad_direction))

    def ship_collision(self, aster_node):
        """
        Handles collision of the ship with an asteroid, by reducing health,
        checking if the player lost (ends the game approriately if they did)
        and removes the asteroid.
        :param aster_node: The node of the asteroid which collided with
                           the ship.
        """
        self.__ship.deduct_ship_hp()
        self.__screen.remove_life()
        if self.__ship.get_ship_hp() == 0:
            self.game_over('Your ship was destroyed!')
        self.__screen.show_message('!', "Your ship collided with an asteroid!")
        self.remove_asteroid(aster_node)

    def launch_torpedo(self):
        """
        Creates a new torpedo according to the ship's position & velocity and
        adds it to the GameRunner object's  torpedo list.
        """
        rad_direction = math.pi / 180 * self.__ship.get_direction()
        torpedo_vx = self.__ship.get_x_speed() + 2 * math.cos(rad_direction)
        torpedo_vy = self.__ship.get_y_speed() + 2 * math.sin(rad_direction)
        torpedo = Torpedo(self.__ship.get_x(), torpedo_vx, self.__ship.get_y(),
                          torpedo_vy, self.__ship.get_direction())
        self.add_torpedo(torpedo)

    def torpedo_hit(self, tor_node, ast_node):
        """
        Handles collisions of torpedos with asteroids by removing both and
        adding points to the score as necessasry.
        :param tor_node: node of colliding torpedo
        :param ast_node: node of colliding asteroid
        """
        tor = tor_node.get_data()
        ast = ast_node.get_data()
        ast_size = ast.get_size()
        self.__score += POINTS_BY_SIZE[ast_size]

        if ast_size > 1:
            new_vx = (tor.get_x_speed() + ast.get_x_speed()) \
                     / math.sqrt(
                ast.get_x_speed() ** 2 + ast.get_y_speed() ** 2)
            new_vy = (tor.get_y_speed() + ast.get_y_speed()) \
                     / math.sqrt(
                ast.get_x_speed() ** 2 + ast.get_y_speed() ** 2)
            self.add_asteroid(Asteroid(ast.get_x(), new_vx,
                                       ast.get_y(), new_vy, ast_size - 1))
            self.add_asteroid(Asteroid(ast.get_x(), -new_vx,
                                       ast.get_y(), -new_vy, ast_size - 1))
        self.remove_asteroid(ast_node)
        self.remove_torpedo(tor_node)

    def game_over(self, msg):
        """
        Displays a message and ends the games.
        :param msg: message to display (string)
        """
        self.__screen.show_message("Game Over", msg)
        self.__screen.end_game()
        sys.exit()


def main(amount):
    """
    Creates a game running object and activates it.
    :param amount: number of initial asteroids
    """
    runner = GameRunner(amount)
    runner.run()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(int(sys.argv[1]))
    else:
        main(DEFAULT_ASTEROIDS_NUM)
