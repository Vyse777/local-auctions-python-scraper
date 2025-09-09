import configparser
from pathlib import Path

config = configparser.ConfigParser()
config.read(Path(__file__).parent.parent / "config.ini")

BASE_URL = config.get("DEFAULT", "BASE_URL")
DB_PATH = config.get("DEFAULT", "DB_PATH")
USE_MULTIPROCESSING = config.getboolean("DEFAULT", "USE_MULTIPROCESSING", fallback=True)
