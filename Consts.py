import os
from pathlib import Path

PORT = int(os.getenv("PORT", 8000))

CACHE_AGE = 60 * 60 * 12

project_dir = Path(__file__).parent.resolve()  # Для привязки к файлу,затем переход к папке(родитель)и выдача его пути

DEFAULT_THEME = "light"
THEMES = {DEFAULT_THEME, "dark"}