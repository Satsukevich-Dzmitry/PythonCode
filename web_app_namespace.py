from typing import NamedTuple
from typing import Optional


class web_app_names(NamedTuple):
    name: str
    surname: str
    age: Optional[str]

    @classmethod
    def get_qs_info(cls, qs: str) -> "web_app_names":
        if not qs:
            return web_app_names(name="stranger", surname="mysteryomagad", age=None)

        pairs = qs.split("&")

        for i in range(len(pairs)):
            key, value = pairs[i].split("=")
            if key == "name":
                name = value
            if key == "surname":
                surname = value
            if key == "age":
                try:
                    age = "You was born at " + str(2020 - int(value))
                except ValueError:
                    age = "Wrong Input"
        return web_app_names(name=name, surname=surname, age=age)
