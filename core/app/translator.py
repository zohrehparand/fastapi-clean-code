from pathlib import Path
import gettext

LOCALES_DIR = Path(__file__).resolve().parent.parent / "locales"


def get_translator(language: str):
    return gettext.translation(
        "messages",
        localedir=str(LOCALES_DIR),
        languages=[language],
        fallback=True,
    )


def translate(message: str, language: str):
    return get_translator(language).gettext(message)
