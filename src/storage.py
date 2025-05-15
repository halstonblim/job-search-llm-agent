import pathlib
import json

DATA_DIR = pathlib.Path("data")


def save_raw(posts: list[str], fname: str = "raw.json") -> None:
    DATA_DIR.mkdir(exist_ok=True)
    (DATA_DIR / fname).write_text(json.dumps(posts, indent=2))
