# Standard Libraries
from pathlib import Path

# Third-party Libraries
from decouple import Config, RepositoryEnv

path = Path("./", ".env")
exists = path.is_file()

if not exists:
    print("Could not find .env file.")
    if path.is_dir():
        print("Found .env directory.")
else:
    print("Found .env file.")
    config = Config(RepositoryEnv(path))

__all__ = ["config"]
