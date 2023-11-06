

from tkinter import *
import tkinter as tk
from boggle_board_randomizer import *
from ex12_utils import abs_range, is_valid_path

WORDS_TO_IMPORT = "boggle_dict.txt"


class GUI(tk.Frame):
    # constants:
    WELCOME_MESSAGE = "WELCOME TO BOGGLE! "
    START_PLAY = "Start To Play"
    EXIT = 'Exit'
    START_GAME_MESSAGE = "LETS TEST\nYOUR SKILLS!"
    GAME_FINISHED = "GAME FINISHED!"
    INVALID_MOVE = "INVALID MOVE!"
    COMBO_PRINT = "COMBO X "
    WORDS_TO_IMPORT = "boggle_dict.txt"
    START_BY_CLICK = "click here to start"
    RESTART = "RESTART"
    COMBO_MODE_BUTTON = 'Combo Mode'
    COLOR1 = "cornflower blue"
    FONT1 = "Helvetica"
    TIME_IN_GAME = "TIME: "
    TIMER_SET = "3:00"
    SCORE_IN_GAME = "SCORE: "
    POINT_INIT = "00"
    WORD_SHOW = "word: "
    WORDS_FOUND = "words found: "
    WHEN_IS_RIGHT = "CORRECT!"
    SMALL_FONT = 15
    BIG_FONT = 30
    SMALL_SCREEN_SIZE = "550x300"
    BIG_SCREEN_SIZE = "1000x600"

    def __init__(self, parent, board, words_list, *args, **kwargs):
        """
        the constructor for our our board and game object
        """
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.timer = None
        self.word = ""
        self.board = board
        self.words_list = words_list
        self.path = []
        self.word_label = None
        self.buttons_list = [[0] * 4 for _ in range(4)]
        self.words_success = []
        self.words_found = None
        self.score = None
        self.message = None
        self.cur_after = None
        self.combo_counter = 0
        self.combo_mode = False

    def after_game_screen(self):
        """
        this screen is opened when the game is finished
        """
        self.config_grid(self.master, 5, 5)
        self.parent.config(bg=self.COLOR1)

        Label(self.parent, text=self.GAME_FINISHED, font=(self.FONT1, 25, "bold")
              , bg=self.COLOR1).grid(row=1, column=2, columnspan=1)

        button1 = Button(self.parent, text=self.START_PLAY, font="bold"
                         , command=self.start_game, fg="blue", bg="dodger blue")
        button1.grid(row=4, column=0, rowspan=1, columnspan=1, sticky=W + E + N + S)

        button2 = Button(self.parent, text=self.EXIT, font= "bold", command=quit, fg="blue", bg="dodger blue")
        button2.grid(row=4, column=3, rowspan=1, columnspan=2, sticky=W + E + N + S)
        self.parent.geometry(self.SMALL_SCREEN_SIZE)

        self.parent.mainloop()

    def quit(self):
        """
        exiting the program
        """
        self.parent.destroy()

    def open_screen(self):
        """
        this opens when we first run the game
        """
        self.config_grid(self.master, 5, 5)

        self.parent.config(bg=self.COLOR1)

        title_label = Label(self.parent, text=self.WELCOME_MESSAGE, font=(self.FONT1, 24, "bold")
                            , bg=self.COLOR1)
        title_label.grid(row=1, column=1, columnspan=1)

        button1 = Button(self.parent, text=self.START_PLAY, font="bold", command=self.start_game, bg="dodger blue")
        button1.grid(row=4, column=0, rowspan=1, columnspan=1, sticky=W + E + N + S)

        button2 = Button(self.parent, text=self.EXIT, font= "bold", command=quit, bg="dodger blue")
        button2.grid(row=4, column=3, rowspan=1, columnspan=2, sticky=W + E + N + S)
        self.parent.geometry(self.SMALL_SCREEN_SIZE)
        self.parent.mainloop()

    def end_time(self):
        """
        helps open the window when game is finished
        """
        self.restart_screen().after_game_screen()

    def update_timer(self):
        """
        helps make the timer for the game
        """
        text_time = self.timer.cget("text")
        mins = int(text_time.split(":")[0])
        sec = int(text_time.split(":")[1])

        separate = ":"

        if sec > 0:
            sec -= 1
        else:
            mins -= 1
            sec = 59

        if mins <= 0 and sec <= 0:
            self.end_time()
            return

        if sec < 10:
            separate += "0"

        self.timer.config(text=(str(mins) + separate + str(sec)))
        self.cur_after = self.parent.after(1000, self.update_timer)

    def button_pressed(self, x, y):
        """
        main function - decide what to do when click a button on the game screen
        """
        self.message.config(text="")
        self.path.append((x, y))

        if not abs_range(self.board, self.path):
            self.finish_move(False)
            self.message.config(text=self.INVALID_MOVE)
            return

        text_time = self.buttons_list[x][y].cget("text")
        self.buttons_list[x][y].config(state=tk.DISABLED, bg="skyBlue3")

        self.word += text_time

        if len(self.path) == 16 and self.word not in self.words_success:
            self.message.config(text=self.INVALID_MOVE)
            self.reset_all_buttons()
            self.word = ""
            self.path = []
            self.word_label.config(text="")

        self.word_label.config(text=self.word)

        if is_valid_path(self.board, self.path, self.words_list):
            self.finish_move(self.word not in self.words_success, word=self.word)

    def add_combo(self, success):
        """
        option we added!
        when you succeed to guess words in row you get bonus of combo_counter ^ 2
        """
        combo_score = 0
        if success:
            self.combo_counter += 1
            if self.combo_counter > 1:
                combo_score = self.combo_counter ** 2
                self.message.config(text=self.COMBO_PRINT + str(self.combo_counter))
        else:
            self.combo_counter = 0

        return combo_score

    def finish_move(self, success, word=""):
        """
        if success is True, means we want to add the score and
        print message to player
        None otherwise
        """
        scores = int(self.score.cget("text"))

        if not success and word != "":
            return

        if success:
            self.words_success.append(word)
            self.words_found.config(text=self.all_success_words_string())
            self.message.config(text=self.WHEN_IS_RIGHT)
            scores += len(self.path) ** 2

        if self.combo_mode:
            scores += self.add_combo(success)
        # always happens
        self.score.config(text=str(scores))
        self.reset_all_buttons()
        self.word = ""
        self.path = []
        self.word_label.config(text="")

    def all_success_words_string(self):
        """
        updates to screen the words found list
        """
        all_words = ""
        for i, word in enumerate(self.words_success):
            if (i+1) % 3 == 0:
                all_words += word + ",\n"
            else:
                all_words += word + ", "
        return all_words[0:-2]

    def reset_all_buttons(self):
        """
        helps reset all clicked buttons
        """
        for b_list in self.buttons_list:
            for button in b_list:
                button.config(relief=RAISED, state=tk.NORMAL, bg="skyBlue1")

    def init_board(self, Frame2, start_button):
        """
        is used when we initializing the board
        """
        for i in range(1, 21, 5):
            for j in range(1, 21, 5):
                self.buttons_list[i//5][j//5] = (Button(Frame2, height=6, width=3, font=(self.FONT1, 13, "bold")
                                                        , text=self.board[i//5][j//5], bg="skyBlue1"))
                self.buttons_list[i//5][j//5].config(command=lambda x=i//5, y=j//5: self.button_pressed(x, y))
                self.buttons_list[i//5][j//5].grid(rowspan=4, columnspan=4, row=i, column=j, sticky=E + W)
        start_button.grid_forget()
        self.update_timer()

    def restart_screen(self):
        """
        when we want to restart the board, things that are needed o be done
        """
        self.parent.destroy()
        if self.cur_after is not None:
            self.parent.after_cancel(self.cur_after)
        self.parent = Tk()
        self.board = randomize_board()
        return GUI(self.parent, self.board, import_words(self.WORDS_TO_IMPORT))

    def start_game(self):
        """
        restarts the game
        """
        self.restart_screen().game_screen()

    def change_mode(self):
        """
        when we want to change from off to on
        """
        self.combo_mode = not self.combo_mode
        self.combo_counter = 0

    def config_grid(self, obj, r_range, c_range):
        """
        helps for making frames
        """
        for r in range(r_range):
            obj.rowconfigure(r, weight=1)
        for c in range(c_range):
            obj.columnconfigure(c, weight=1)

    def init_game_frames(self):
        """
        Inits the main frames of the game screen
        """
        frame1 = Frame(self.parent, bg="royal blue")
        frame1.grid(row=0, column=0, rowspan=1, columnspan=5, sticky=W + E + N + S)

        Label(frame1, text="boggle", font=(self.FONT1, self.BIG_FONT, "bold"), bg="royal blue").pack()

        frame2 = Frame(self.parent, bg="dodger blue")
        frame2.grid(row=1, column=0, rowspan=5, columnspan=5, sticky=W + E + N + S)

        frame3 = Frame(self.parent, bg=self.COLOR1)
        frame3.grid(row=0, column=5, rowspan=6, columnspan=1, sticky=W + E + N + S)

        self.config_grid(frame3, 4, 20)
        self.config_grid(frame2, 21, 21)

        return frame1, frame2, frame3

    def set_frame_component(self, frame1, frame2, frame3):
        """
        Inits the components in the frames of the game screen
        :param frame1:
        :param frame2:
        :param frame3:
        :return:
        """
        tk.Button(frame3, text=self.EXIT, font=(self.FONT1, self.SMALL_FONT), command=self.end_time
                  , bg=self.COLOR1).grid(row=0, column=3)

        tk.Button(frame3, text=self.RESTART, font=(self.FONT1, self.SMALL_FONT), command=self.start_game
                  , bg=self.COLOR1).grid(row=0, column=2)

        tk.Checkbutton(frame3, text=self.COMBO_MODE_BUTTON, font=(self.FONT1, self.SMALL_FONT), onvalue=True, offvalue=False
                       , bg=self.COLOR1, command=self.change_mode).grid(row=0, column=1)

        self.message = Label(frame3, text="", font=(self.FONT1, self.SMALL_FONT), bg=self.COLOR1)
        self.message.grid(row=0, column=0)

        Label(frame3, text=self.TIME_IN_GAME, font=(self.FONT1, self.BIG_FONT), bg=self.COLOR1).grid(row=1, column=0)
        self.timer = Label(frame3, text=self.TIMER_SET, font=(self.FONT1, self.BIG_FONT), bg=self.COLOR1)
        self.timer.grid(row=1, column=1)

        Label(frame3, text=self.SCORE_IN_GAME, font=(self.FONT1, self.BIG_FONT), bg=self.COLOR1).grid(row=2, column=0)
        self.score = Label(frame3, text=self.POINT_INIT, font=(self.FONT1, self.BIG_FONT), bg=self.COLOR1)
        self.score.grid(row=2, column=1)

        Label(frame3, text=self.WORD_SHOW, font=(self.FONT1, self.SMALL_FONT), bg=self.COLOR1).grid(row=3, column=0)
        self.word_label = Label(frame3, text="", font=(self.FONT1, self.SMALL_FONT), bg=self.COLOR1)
        self.word_label.grid(columnspan=3, rowspan=1, row=3, column=1)

        Label(frame3, text=self.WORDS_FOUND, font=(self.FONT1, self.SMALL_FONT), bg=self.COLOR1).grid(row=4, column=0)
        self.words_found = Label(frame3, text="", font=(self.FONT1, self.SMALL_FONT), bg=self.COLOR1)
        self.words_found.grid(row=5, column=0, rowspan=5, columnspan=3)

        self.message.config(text=self.START_GAME_MESSAGE)
        start_game_button = tk.Button(frame2, text=self.START_BY_CLICK, font=(self.FONT1, self.BIG_FONT), bg=self.COLOR1)
        start_game_button.config(command=lambda: self.init_board(frame2, start_game_button))
        start_game_button.grid(row=10, column=10)

    def game_screen(self):
        """
        Inits the game window with all of its components
        """
        self.config_grid(self.master, 6, 5)

        self.set_frame_component(*self.init_game_frames())

        self.parent.geometry(self.BIG_SCREEN_SIZE)
        self.parent.mainloop()


def import_words(words_path):
    """
    returns the words needed for the game
    """
    with open(words_path) as fp:
        return fp.read().splitlines()


if __name__ == '__main__':
    # here everything is run
    root = Tk()
    gui = GUI(root, randomize_board(), import_words(WORDS_TO_IMPORT))
    gui.open_screen()
