from datetime import date, datetime
from typing import NamedTuple
from typing import Optional
from urllib.parse import parse_qs


class Web_App_Names(NamedTuple):
    name: str
    surname: str
    age: int
    year: Optional[str]

    @classmethod
    def get_qs_info(cls, qs: str) -> "Web_App_Names":
        year = "Wrong Input"
        try:
            keys_and_values = parse_qs(qs, strict_parsing=True)
            name_list = keys_and_values.get("name", ["stranger"])
            name = name_list[0]
            surname_list = keys_and_values.get("surname", ["Didn't tell"])
            surname = surname_list[0]
            age_list = keys_and_values.get("age", [0])
            age = age_list[0]
            if isinstance(age, str) and age.isdecimal():
                age = int(age)
                year = f"You was born at {datetime.now().year - age}"
            else:
                age = 0
                year = "Wrong Input"
        except ValueError:
            name = "stranger"
            surname = "Didn't tell"
            age = 0

        return Web_App_Names(name=name, surname=surname, age=age, year=year)

