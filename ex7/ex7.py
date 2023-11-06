
from typing import List, Dict, Tuple, Union, Any

# Custom Typings
CHAR_LIST = List[str]
CHAR_MATRIX = List[CHAR_LIST]

# Operators for the recursive function
ALLOW_REPEATS = True  # To allow repeats
RESTRICT_REPEATS = False  # To disallow repeats

# Fillers for Flood fill Function
FILL = "*"


################################################################
# Part 1
################################################################

def print_to_n(n: int) -> None:
    """The function prints all Natural numbers from 1 to n"""
    if n < 1:
        return None
    print_to_n(n - 1)
    print(n)


def digit_sum(n: int) -> int:
    """This function sums the digits of an integer"""
    if n == 0:
        return 0
    return n % 10 + digit_sum(int(n / 10))


def has_divisor_smaller_than(n: int, i: int) -> bool:
    """If n(Integer), has divisor smaller than i(Integer) returns True,
    Otherwise returns False"""
    # Base Cases
    if n < 2:
        return False
    if n == 2:
        return True
    if n % i == 0:
        return False

    if (i * i) > n:
        return True
    return has_divisor_smaller_than(n, i + 1)


def is_prime(n: int) -> bool:
    """Returns True if n(integer) is a prime number, False if not"""
    if has_divisor_smaller_than(n, 2):
        return True
    return False


################################################################
# Part 2
################################################################

def play_hanoi(hanoi: Any, n: int, src: Any, dst: Any, temp: Any) -> None:
    """The function solves Hanoi Game"""
    if n < 1:  # Extreme Case
        hanoi.move(src, dst)
        return
    if n == 1:  # Base Case
        hanoi.move(src, dst)
    else:  # Recursion Step
        play_hanoi(hanoi, n - 1, src, temp, dst)
        play_hanoi(hanoi, 1, src, dst, temp)
        play_hanoi(hanoi, n - 1, temp, dst, src)


def print_sequences(char_list: CHAR_LIST, n: int) -> None:
    """The Function prints all possible n length combinations from
    a list of chars recursively with repeats"""
    length = len(char_list)
    print_sequences_recursively(char_list, "", length, n, ALLOW_REPEATS)


def print_no_repetition_sequences(char_list: CHAR_LIST, n: int) -> None:
    """The Function prints all possible n length combinations from
    a list of chars recursively without repeats"""
    length = len(char_list)
    print_sequences_recursively(char_list, "", length, n, RESTRICT_REPEATS)


def print_sequences_recursively(char_list: CHAR_LIST, prefix: str, n: int,
                                length: int, reps: int) -> None:
    """The function handles the recursive combination creation of letters"""
    if reps:  # Check if we are allowed to repeat letters, default is True
        if length == 0:  # print prefix
            print(prefix)
            return
        # One by one add all characters from set
        # recursively call for the length equals to length-1
        for i in range(n):  # Next character of input added
            new_prefix = prefix + char_list[i]
            print_sequences_recursively(char_list, new_prefix, n, length - 1,
                                        ALLOW_REPEATS)
    elif not reps:
        if length == 0:  # print prefix
            print(prefix)
            return
        # One by one add all characters from set and recursively call for
        # length equals to length-1
        for i in range(n):  # Next character of input added
            new_prefix = prefix + char_list[i]
            # the string length is decreased, because we have added a new char
            # Checks if any of the letters inside the char_list appears for
            # each Iteration we make on char_list
            if any(char not in prefix for char in char_list[i]):
                print_sequences_recursively(char_list,
                                            new_prefix, n, length - 1,
                                            RESTRICT_REPEATS)


def _parentheses(n: int, chest: Dict) -> CHAR_LIST:
    """The recursive function of Parentheses"""
    if n == 0:  # Base case of 0
        return sorted([''])  # Return a list of the function
    elif n in chest:
        return chest[n]  # Update the memory chest
    else:
        output = set('(' + p + ')' for p in parentheses(n - 1))
        for k in range(1, n):  # Iteration for the index range from 1 to n
            output.update(
                p + q for p in parentheses(k) for q in parentheses(n - k))
        chest[n] = output  # Append the cached memory to output
        return sorted(output)  # Return a list of the function


def parentheses(n: int) -> CHAR_LIST:
    """The function change the parenthesis according to given coordinates"""
    chest = {}  # A chest(Caching) for the parentheses function
    return _parentheses(n, chest)


def flood_fill(image: CHAR_MATRIX, start: Tuple) -> Union[CHAR_MATRIX, None]:
    """Flood Fill Function to replace . with * according to coordinates"""
    x, y = start  # Assign the values of the tuple to x,y coordinates
    if image[x][y] == FILL:  # If the place already filled
        return
    image[x][y] = FILL  # Fill the current cell
    flood_fill(image, (x + 1, y))  # Draw up
    flood_fill(image, (x - 1, y))  # Draw Down
    flood_fill(image, (x, y + 1))  # Draw Right
    flood_fill(image, (x, y - 1))  # Draw left
