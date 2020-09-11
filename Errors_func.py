from typing import NamedTuple

from User_data import User_name

class Html_colors(NamedTuple):
    text_color: str
    @classmethod
    def html_colors(cls, user: User_name):
        text_color = "black"
        if not user.valid:
            text_color = "red"

        return Html_colors(text_color=text_color)
