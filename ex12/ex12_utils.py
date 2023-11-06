
FIND_LENGTH_N_PATHS = 0
FIND_LENGTH_N_WORDS = 1
FIND_LENGTH_N_WORDS_AND_PATH = 2
MOVE_DIRECTIONS = [[1, 0], [0, 1], [1, 1], [1, -1], [-1, 0], [-1, 1], [0, -1], [-1, -1]]


def is_valid_path(board, path, words):
    """
    input: the board, path on the board represented by tuples, list of words
    return: None if path is not valid for the board, the word if it is
    """

    if len(set(path)) != len(path):
        return None

    if not abs_range(board, path):
        return None

    word = find_word_with_path(board, path)
    if word in words:
        return word
    return None


def abs_range(board, path):
    """
    helper function to find if distance between 2 "points" of the path
    is valid
    """
    for i in range(len(path) - 1):
        if not abs_distance(path[i:i + 2]) or not in_board_range(board, path[i])\
                or not in_board_range(board, path[i + 1]):
            return False
    return True


def in_board_range(board, location):
    """
    checks if the specific location - tuple - is valid for the board
    """
    if location[0] >= len(board) or location[0] < 0 or location[1] >= len(board[0]) or location[1] < 0:
        return False
    return True


def not_in_path(location, path):
    """
    Checks if specific location already in path
    """
    if location in path:
        return False
    return True


def abs_distance(locations):
    """
    Check the distance between two locations
    """
    for coordinate in range(len(locations[0])):
        if abs(locations[0][coordinate] - locations[1][coordinate]) > 1:
            return False
    return True


def find_word_with_path(board, path):
    """
    helper function in order to return the word required
    """
    word = ""
    for location in path:
        word += board[location[0]][location[1]]
    return word


def find_length_n_words(n, board, words):
    """
    input: n - length of the paths, board- for the game,words- list of words
    return: all paths represents words in in length n
    """
    return recursive_switch_helper(n, board, words, FIND_LENGTH_N_WORDS)


def n_in_range(board, n):
    """
    checks if n can be a path in the board
    """
    return n > len(board) * len(board[0]) or n <= 0


def recursive_switch_helper(n, board, words, switch):
    """
    Get all the needed information foe the recursive function, and flag "switch" to choose what we are looking for.
    All recursive function need to start the helper function from all board locations, so
    we can do this with one function.
    """
    all_paths = []
    path = []
    if n_in_range(board, n):
        return all_paths
    for i in range(len(board)):
        for j in range(len(board[0])):
            move_helper(n, path[:], i, j, board, all_paths, words, switch=switch)
    return all_paths


def find_length_n_words_and_path(n, board, words):
    """
    input: n - length of the paths, board- for the game,words- list of words
    return: list of tuples, with all paths represents words in in length n, and the corresponding words
    in this pattern: [(path, word)....].
    """
    return recursive_switch_helper(n, board, words, FIND_LENGTH_N_WORDS_AND_PATH)


def move_helper(n, path, i, j, board, all_paths, words, word="", switch=0):
    """
    The recursive function helper, move every direction every time to check all the paths
    """
    if not in_board_range(board, (i, j)):
        return

    path.append((i, j))
    word = add_word(word, board[i][j])

    if switch == FIND_LENGTH_N_PATHS and len(path) == n:
        if is_valid_path(board, path, words):
            all_paths.append(path)
        return

    if switch != FIND_LENGTH_N_PATHS and len(word) == n:
        if is_valid_path(board, path, words):
            if switch == FIND_LENGTH_N_WORDS:
                all_paths.append(path)
            elif switch == FIND_LENGTH_N_WORDS_AND_PATH:
                all_paths.append((path, word))
        return

    new_words = list(filter(lambda one_word: one_word[:len(word)] == word, words))
    if not new_words:
        return

    for move in MOVE_DIRECTIONS:
        move_helper(n, path[:], i + move[0], j + move[1], board, all_paths, new_words, word, switch)


def add_word(word, add):
    """
    add char to the old word
    """
    new_word = word + add
    return new_word


def find_length_n_paths(n, board, words):
    """
    input: n - length of the paths, board- for the game,words- list of words
    return: list of all paths in length n
    """
    return recursive_switch_helper(n, board, words, FIND_LENGTH_N_PATHS)


def max_score_paths(board, words):
    """
    Function founds all the paths of words in the board, and return the longest path if there are two path for the
    same word.
    :param board: game board
    :param words: all words
    :return: longest paths for all words in board from words list
    """
    dic = {}
    all_sorted_paths = []
    for n in range(1, max_word_length(words) + 1):
        all_paths = find_length_n_words_and_path(n, board, words)
        for path in all_paths:
            if path[1] in dic:
                if len(path[0]) < len(dic[path[1]]):
                    continue
            dic[path[1]] = path[0]
    for path in dic:
        all_sorted_paths.append(dic[path])
    return all_sorted_paths


def max_word_length(words):
    """
    Finds the longest word length we need to check.
    :param words: all the words
    :return: the longest length
    """
    return len(max(words, key=len))
