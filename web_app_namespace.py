from typing import NamedTuple
from typing import Optional


class Web_app_names(NamedTuple):
    name: str
    surname: str
    age: int
    year: Optional[str]

    @classmethod
    def get_qs_info(cls, qs: str) -> "Web_app_names":
        if not qs:
            return Web_app_names(name="stranger", surname="mysteryomagad", age=None, year=None)

        pairs = qs.split("&")

        for i in range(len(pairs)):
            key, value = pairs[i].split("=")
            if key == "name":
                name = value
            if key == "surname":
                surname = value
            if key == "age":
                try:
                    age = int(value)
                    year_of_birth = 2020 - int(value)
                    year = f"You was born at  {year_of_birth}"
                except ValueError:
                    age = None
                    year = "Wrong Input"
        return Web_app_names(name=name, surname=surname, age=age, year=year)
