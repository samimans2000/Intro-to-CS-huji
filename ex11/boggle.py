
import sys

from ex11_utils import create_words_dict
from controller import BoggleController

def start_game(word_dict_path: str) -> None:
    """
    Starting the game, with GUI.

    :param word_dict_path: Path on filesystem for the
        words dictionary to work by (e.g. acceptable words)
    """
    # Reading the file and removing all whitespaces etc.
    filedata = ""
    with open(word_dict_path, "r") as dict_file:
        filedata = dict_file.read().split()

    # Creating the words dict, and the controlling, and let the games begin
    wordsdict = create_words_dict(filedata)
    controller = BoggleController(wordsdict)
    controller.run_game()

if __name__ == "__main__":
    # Expecting a single command-line argument - Path to the words dict
    if 2 == len(sys.argv):
        start_game(sys.argv[1])
    else:
        start_game("boggle_dict.txt")