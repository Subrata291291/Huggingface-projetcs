
from pathlib import Path


def load_css() -> str:
    css_path = Path(__file__).with_name("styles.css")
    return css_path.read_text(encoding="utf-8")
