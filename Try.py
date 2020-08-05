import os
from pathlib import Path

PORT = int(os.getenv("PORT", 8000))

CACHE_AGE = 60 * 60 * 12
