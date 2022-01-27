from settings import *
from tkinter import *


class Style:
    styles = ('d', 'e', 's', 'r')

    def __init__(self):
        self.digit = {
            'bg': GREY,
            'activebackground': DARK_GREY,
            'fg': 'white',
            'activeforeground': 'white',
            'font': 24
        }

        self.equal = {
            'bg': BLUE,
            'activebackground': DARK_BLUE,
            'activeforeground': 'black',
            'fg': 'black'
        }

        self.sign = {
            'bg': DARK_GREY,
            'activebackground': GREY,
            'activeforeground': 'white',
            'fg': 'white'
        }

        self.reset = {
            'bg': DARK_GREY,
            'activebackground': GREY,
            'activeforeground': 'white',
            'fg': 'white'
        }

        self.styles = {
            's': self.sign,
            'e': self.equal,
            'd': self.digit,
            'r': self.reset
        }

    def update(self, button: Button, style: str):
        if not (style in Style.styles):
            raise ValueError(f'Wrong style given. Must be one of {Style.styles} get {style}')

        style_dict = self.styles[style]
        button.config(**style_dict)