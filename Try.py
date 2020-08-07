import os
from pathlib import Path

PORT = int(os.getenv("PORT", 8000))

CACHE_AGE = 60 * 60 * 12


def build_path(self) -> str:
    result = self.path
    if result[-1] != "/":
        result = f"{result}/"
    return result

