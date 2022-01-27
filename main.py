from tkinter import *
from functools import partial
from settings import *
from styles import Style


class Calc:
    BUTTONS = [
        ['1', '2', '3', '+'],
        ['4', '5', '6', '-'],
        ['7', '8', '9', '*'],
        ['AC', '0', '/', '=']
    ]

    BUTTONS_TYPE = [
        ['d', 'd', 'd', 's'],
        ['d', 'd', 'd', 's'],
        ['d', 'd', 'd', 's'],
        ['r', 'd', 's', 'e'],
    ]

    ROW_COUNT = len(BUTTONS)
    COLUMN_COUNT = len(BUTTONS[0])

    def __init__(self):
        self.rel_size = (1, 1)
        self.label_size = (1, 0.2)
        self.cell_size = (WIDTH // Calc.COLUMN_COUNT, HEIGHT // Calc.ROW_COUNT)
        self.cell_rel_size = (1 / Calc.COLUMN_COUNT, (1 - self.label_size[1]) / Calc.ROW_COUNT)

        self.buttons = []
        self.style = Style()

        self.__current_sign = None
        self.__value = 0
        self.__current_value = 0

        self.label = Label(text="0", font=32)
        self.render()

    def render(self):
        self.label.place(relwidth=self.label_size[0], relheight=self.label_size[1])
        self.label['bg'] = BACKGROUND_DARK_GRAY
        self.label['fg'] = 'white'
        self.label['anchor'] = 'e'

        for row in range(len(Calc.BUTTONS)):
            for col in range(len(Calc.BUTTONS[row])):
                btn = Button(root, text=Calc.BUTTONS[row][col], command=partial(self.click, row, col))
                btn.place(relx=col * self.cell_rel_size[0], rely=row * self.cell_rel_size[1] + self.label_size[1],
                          relwidth=self.cell_rel_size[0], relheight=self.cell_rel_size[1])
                self.buttons.append(btn)
                self.style.update(btn, Calc.BUTTONS_TYPE[row][col])

    def click(self, row, col):
        if Calc.BUTTONS_TYPE[row][col] == 's':
            self.__sign_event(Calc.BUTTONS[row][col])
        if Calc.BUTTONS_TYPE[row][col] == 'd':
            self.__value_event(int(Calc.BUTTONS[row][col]))
        if Calc.BUTTONS_TYPE[row][col] == 'e':
            self.__equal_event()
        if Calc.BUTTONS_TYPE[row][col] == 'r':
            self.__reset_event()

    def __sign_event(self, sign: str):
        if not (self.__current_sign is None):
            self.__equal_event()
        elif not (self.__current_value is None):
            self.__value = self.__current_value
        self.__current_sign = sign
        self.__current_value = None

    def __value_event(self, value: int):
        if self.__current_value is None:
            self.__current_value = value
        else:
            self.__current_value = int(str(self.__current_value) + str(value))

        self.label['text'] = self.__current_value

    def __equal_event(self):
        if self.__current_value is None:
            return

        match self.__current_sign:
            case '+':
                self.__value += self.__current_value
            case '-':
                self.__value -= self.__current_value
            case '*':
                self.__value = round(self.__value * self.__current_value, 2)
            case '/':
                if self.__current_value != 0:
                    self.__value = round(self.__value / self.__current_value, 2)

        self.__value = int(self.__value) if int(self.__value) == self.__value else self.__value

        self.label['text'] = self.__value
        self.__current_sign = None
        self.__current_value = None

    def __reset_event(self):
        self.__current_value = None
        self.__value = 0
        self.__current_sign = None
        self.label['text'] = 0


root = Tk()
root.configure(bg=BACKGROUND_DARK_GRAY)
root.geometry(f"{WIDTH}x{HEIGHT}")
calc = Calc()
root.mainloop()
