
import hangman_helper

HIDDEN_LETTER = "_"


def update_word_pattern(word, pattern, letter):
    """The function returns updated pattern according to
     the given word and letter."""
    for ind in range(len(word)):
        if word[ind] == letter:
            pattern = pattern[:ind] + letter + pattern[ind+1:]
    return pattern


def run_single_game(words_lst, score):
    """The function gets a list of words and an initial score,
     and runs a single game of Hangman.
     It returns the updated score at the end of the game."""
    score = game_process(*initialize_game(words_lst), score, words_lst)
    return score


def initialize_game(words_lst):
    """The function gets a list of words, and returns a random word,
    a pattern that fits the word and an empty list of the wrong guesses"""
    rand_word = hangman_helper.get_random_word(words_lst)
    pattern = HIDDEN_LETTER * len(rand_word)
    wrong_guesses = list()
    return rand_word, pattern, wrong_guesses


def game_process(word, pattern, wrong_guesses, score, words_lst):
    """The function runs a single game, and returns the player's
    score at the end of it."""
    while pattern != word and score > 0:
        msg = f"Guess right {pattern.count(HIDDEN_LETTER)} letter/s"
        hangman_helper.display_state(pattern, wrong_guesses, score, msg)
        kind, value = hangman_helper.get_input()
        score, pattern = parse_user_choice(kind, value, word, wrong_guesses,
                                           words_lst, score, pattern)
    print_win_lose_msg(pattern, word, wrong_guesses, score)
    return score


def parse_user_choice(kind, value, word, wrong_guesses, words_lst, score,
                      pattern):
    """The function parses the user's input, and returns an updated
    score and pattern"""
    if kind == hangman_helper.LETTER:
        return handle_letter(value, word, pattern, wrong_guesses, score)
    elif kind == hangman_helper.WORD:
        return handle_word(value, word, pattern, score)
    return handle_hint(pattern, wrong_guesses, score, words_lst), pattern


def handle_letter(letter, word, pattern, wrong_guesses, score):
    """The function proceeds the game according to the given letter.
    It returns an updated score and pattern"""
    if len(letter) > 1 or not letter.isalpha() or letter.isupper():
        print("The input is invalid. Please try again.\n")
    elif letter in pattern or letter in wrong_guesses:
        print("You have already chose this letter. Please try again.\n")
    else:
        score -= 1
        n = word.count(letter)
        if n:
            pattern = update_word_pattern(word, pattern, letter)
            score += n*(n+1) // 2
        else:
            wrong_guesses.append(letter)
    return score, pattern


def handle_word(guessed_word, word, pattern, score):
    """The function proceeds the game according to the given letter
    It returns an updated score and pattern"""
    score -= 1
    if guessed_word == word:
        n = pattern.count(HIDDEN_LETTER)
        score += n*(n+1) // 2
        pattern = word
    return score, pattern


def handle_hint(pattern, wrong_guesses, score, words_lst):
    """The function prints a list of words that the player
    can use as a hint. It returns an updated score."""
    score -= 1
    filtered_words = filter_words_list(words_lst, pattern, wrong_guesses)
    if len(filtered_words) > hangman_helper.HINT_LENGTH:
        sub_lst = list()
        for i in range(hangman_helper.HINT_LENGTH):
            sub_lst.append(filtered_words[i * len(filtered_words)
                                          // hangman_helper.HINT_LENGTH])
        hangman_helper.show_suggestions(sub_lst)
    else:
        hangman_helper.show_suggestions(filtered_words)
    print()
    return score


def filter_words_list(words, pattern, wrong_guess_lst):
    """The function returns a list of words that can fit the
    pattern and the previous guesses."""
    result = list()
    for word in words:
        if len(word) != len(pattern):
            continue
        for letter in wrong_guess_lst:
            if letter in word:
                break
        else:
            for ind, value in enumerate(pattern):
                if pattern[ind] == HIDDEN_LETTER:
                    continue
                elif ind < len(word) and pattern[ind] != word[ind]:
                    break
                elif pattern.count(value) != word.count(value):
                    break
            else:
                result.append(word)
    return result


def print_win_lose_msg(pattern, word, wrong_guesses, score):
    """Prints the current state of the game that includes a message,
    whether the player won or lost."""
    if pattern == word:
        msg = "Congratulations, you have found the correct word.\n"
    else:
        msg = f"Unfortunately, you lost. The correct word is: {word}.\n"
    hangman_helper.display_state(pattern, wrong_guesses, score, msg)


def main():
    """Enables to play multiple games of hangman."""
    words_lst = hangman_helper.load_words()
    score = run_single_game(words_lst, hangman_helper.POINTS_INITIAL)
    games_played = 1
    while True:
        if score:
            msg = f"You played {games_played} game/s so far, and you have" \
                  f" {score} point/s left.\nWould you like to play again?\n"
            if hangman_helper.play_again(msg):
                score = run_single_game(words_lst, score)
                games_played += 1
                continue
            break
        else:
            msg = f"You played {games_played} game/s so far.\n" \
                  f"Would you like to play again?\n"
            if hangman_helper.play_again(msg):
                score = run_single_game(words_lst,
                                        hangman_helper.POINTS_INITIAL)
                games_played = 1
                continue
            break


if __name__ == "__main__":
    main()
