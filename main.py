from tkinter import *
from functools import partial
from settings import *
from styles import Style


class Calc:
    BUTTONS = [
        ['⅟x', '√x', 'x²', '/'],
        ['1', '2', '3', '+'],
        ['4', '5', '6', '-'],
        ['7', '8', '9', '*'],
        ['AC', '0', '.', '=']
    ]

    BUTTONS_TYPE = [
        ['s', 's', 's', 's'],
        ['d', 'd', 'd', 's'],
        ['d', 'd', 'd', 's'],
        ['d', 'd', 'd', 's'],
        ['rd', 'd', 'sd', 'e'],
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
        self.__current_value = None
        self.__accuracy = 4
        self.__point = False

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
                self.style.update(btn, Calc.BUTTONS_TYPE[row][col][-1])

    def click(self, row, col):
        if Calc.BUTTONS_TYPE[row][col][0] == 's':
            self.__sign_event(Calc.BUTTONS[row][col])
        if Calc.BUTTONS_TYPE[row][col][0] == 'd':
            self.__value_event(Calc.BUTTONS[row][col])
        if Calc.BUTTONS_TYPE[row][col][0] == 'e':
            self.__equal_event()
        if Calc.BUTTONS_TYPE[row][col][0] == 'r':
            self.__reset_event()

    def __sign_event(self, sign: str):
        if sign == '.':
            if self.__current_value is not None:
                self.__current_value = float(self.__current_value)
                self.__point = True
            return

        if not (self.__current_sign is None):
            self.__equal_event()
        elif not (self.__current_value is None):
            self.__value = self.__current_value

        match sign:
            case '⅟x':
                if self.__value != 0:
                    self.__value **= -1
                    self.__current_value = 0
                    self.__equal_event()
                    self.__current_value = self.__value
            case '√x':
                self.__value **= 0.5
                self.__current_value = 0
                self.__equal_event()
                self.__current_value = self.__value
            case 'x²':
                self.__value **= 2
                self.__current_value = 0
                self.__equal_event()
                self.__current_value = self.__value
            case _:
                self.__current_sign = sign
                self.__current_value = None

    def __value_event(self, value: int | str):
        if self.__current_value is None:
            self.__current_value = int(value)
        else:
            if isinstance(self.__current_value, int):
                self.__current_value = int(str(self.__current_value) + str(value))
            if isinstance(self.__current_value, float) and\
                    len(str(self.__current_value).split('.')[1]) <= self.__accuracy:
                if str(self.__current_value).split('.')[1] == '0' and self.__point:
                    self.__current_value = float(str(self.__current_value)[:-1] + str(value))
                else:
                    self.__current_value = float(str(self.__current_value) + str(value))
                self.__point = False

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
                self.__value *= self.__current_value
            case '/':
                if self.__current_value != 0:
                    self.__value /= self.__current_value

        self.__value = round(self.__value, self.__accuracy)
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
