from typing import NamedTuple, Optional
from urllib.parse import parse_qs

from User_data import User_name

class Html_colors(NamedTuple):
    text_color: Optional[str]
    input_color: Optional[str]
    @classmethod
    def html_colors(cls, user: User_name):
        text_color = "White"
        input_color = "Black"
        if not user.valid:
            text_color = "Red"
            input_color = "LimeGreen"

        return Html_colors(text_color=text_color, input_color=input_color)